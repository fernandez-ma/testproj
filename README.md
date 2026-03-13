# 🏁 RaceDay — Running Registration Website
### Flask + MongoDB Atlas

---

## 📁 Project Structure

```
running_reg/
├── app.py                  ← Flask backend (routes, MongoDB logic)
├── requirements.txt        ← Python dependencies
├── templates/
│   ├── index.html          ← Landing page with race info & live stats
│   ├── register.html       ← Registration form
│   ├── success.html        ← Printable confirmation receipt
│   └── admin.html          ← Admin dashboard with search & table
└── static/
    └── css/
        └── style.css       ← Full dark-themed stylesheet
```

> No schema.sql needed — MongoDB Atlas creates collections automatically on first insert.

---

## ☁️ Setting Up MongoDB Atlas (Free)

1. Go to https://www.mongodb.com/cloud/atlas and create a free account
2. Create a **free M0 cluster** (512MB, always free)
3. Under **Database Access** → Add a database user with a username and password
4. Under **Network Access** → Add IP Address → Allow access from anywhere (0.0.0.0/0)
5. Click **Connect** on your cluster → **Connect your application**
6. Copy the connection string — it looks like:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
7. Replace username and password with your actual credentials

---

## ⚙️ Setup in VS Code

### 1. Install dependencies
Open the terminal in VS Code (Ctrl + backtick) and run:
```bash
pip install flask pymongo dnspython
```

### 2. Set your MongoDB URI

Option A — Edit directly in app.py:
```python
MONGO_URI = "mongodb+srv://youruser:yourpassword@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

Option B — Use a .env file (recommended):
Create a .env file in the project root:
```
MONGO_URI=mongodb+srv://youruser:yourpassword@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```
Then install and load dotenv:
```bash
pip install python-dotenv
```
Add to the top of app.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 3. Run the app
```bash
python app.py
```
Open your browser at: http://127.0.0.1:5000

---

## 🌐 Pages

| URL             | Description                          |
|-----------------|--------------------------------------|
| /               | Landing page with race categories    |
| /register       | Registration form                    |
| /success/<id>   | Confirmation receipt (printable)     |
| /admin          | Admin dashboard — all registrants    |

---

## 🆓 Free Hosting Options

### Option 1 — Render (Best with MongoDB Atlas)
- URL: https://render.com
- Free tier: 1 web service (sleeps after 15 min inactivity)
- Steps:
  1. Push project to GitHub
  2. Connect repo on Render, set Start Command: gunicorn app:app
  3. Add environment variable: MONGO_URI = your Atlas URI
- Add gunicorn to requirements.txt

### Option 2 — Railway
- URL: https://railway.app
- Free tier: $5 credit/month
- Set MONGO_URI as an environment variable in the dashboard
- Auto-deploys from GitHub

### Option 3 — PythonAnywhere
- URL: https://www.pythonanywhere.com
- Free tier: 1 web app, subdomain yourname.pythonanywhere.com
- Works great with Flask + MongoDB Atlas (Atlas is cloud, no local DB needed)
- Upload files manually or via Git

### Option 4 — Free Domain via Freenom
- URL: https://www.freenom.com
- Get a free .tk, .ml, or .ga domain
- Point it to your Render/Railway/PythonAnywhere app URL

---

## 📝 Notes
- Email is indexed as unique in MongoDB — duplicate registrations are rejected automatically
- No schema.sql needed — MongoDB creates the database and collection on first insert
- The /admin page has no password — consider adding Flask-Login before going public
- Receipt IDs show the last 6 characters of the MongoDB ObjectId
