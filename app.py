from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient, DESCENDING
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "raceday_secret_key_2024"

# ── Paste your MongoDB Atlas connection string here ───────────────────────────
MONGO_URI = "mongodb+srv://mshinoctan3204val_db_user:yhuewhyduihg@cluster0.q5k12gw.mongodb.net/?appName=Cluster0"
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://mshinoctan3204val_db_user:yhuewhyduihg@cluster0.q5k12gw.mongodb.net/?retryWrites=true&w=majority")

client = MongoClient(MONGO_URI)
db     = client["running_registration"]
col    = db["registrations"]

# Ensure email uniqueness
col.create_index("email", unique=True)

# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    try:
        total  = col.count_documents({})
        by_cat = list(col.aggregate([
            {"$group": {"_id": "$category", "cnt": {"$sum": 1}}},
            {"$project": {"category": "$_id", "cnt": 1, "_id": 0}}
        ]))
    except:
        total  = 0
        by_cat = []
    return render_template("index.html", total=total, by_cat=by_cat)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        d = request.form
        doc = {
            "first_name":      d["first_name"],
            "last_name":       d["last_name"],
            "age":             int(d["age"]),
            "gender":          d["gender"],
            "email":           d["email"],
            "phone":           d["phone"],
            "category":        d["category"],
            "tshirt_size":     d["tshirt_size"],
            "emergency_name":  d["emergency_name"],
            "emergency_phone": d["emergency_phone"],
            "registered_at":   datetime.now()
        }
        try:
            result = col.insert_one(doc)
            return redirect(url_for("success", reg_id=str(result.inserted_id)))
        except DuplicateKeyError:
            flash("That email is already registered.", "error")
        except Exception as e:
            flash(f"Registration failed: {e}", "error")
    return render_template("register.html")


@app.route("/success/<reg_id>")
def success(reg_id):
    try:
        reg = col.find_one({"_id": ObjectId(reg_id)})
        if not reg:
            return "Registration not found.", 404
        reg["id"] = str(reg["_id"])
        return render_template("success.html", reg=reg)
    except Exception as e:
        return f"Error: {e}", 500


@app.route("/admin")
def admin():
    try:
        rows = list(col.find().sort("registered_at", DESCENDING))
        for r in rows:
            r["id"] = str(r["_id"])
        total  = col.count_documents({})
        by_cat = list(col.aggregate([
            {"$group": {"_id": "$category", "cnt": {"$sum": 1}}},
            {"$project": {"category": "$_id", "cnt": 1, "_id": 0}}
        ]))
        return render_template("admin.html", rows=rows, total=total, by_cat=by_cat)
    except Exception as e:
        return f"Error loading admin: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)
