# 📋 Django CMS - Submission Guide

## ✅ Project is Ready for Submission!

Your CMS project is fully functional and ready to submit to a company. Follow this guide step-by-step.

---

## 🎯 What's Included in Your Project:

- ✅ **Django CMS** with full admin interface
- ✅ **Catalog API** (public read-only REST API)
- ✅ **Background Worker** for automated lesson publishing
- ✅ **Docker & Docker Compose** for easy local setup
- ✅ **Professional README** with complete documentation
- ✅ **Migrations** for database schema
- ✅ **Requirements.txt** with all dependencies
- ✅ **.env.example** for configuration template
- ✅ **.gitignore** for clean repository

---

## 📝 Step 1: Submit to GitHub

### 1.1 Initialize Git Repository

Open PowerShell in your project folder and run:

```powershell
cd c:\Users\parim\OneDrive\Desktop\ChaiShots\cms_backend
git init
git add .
git commit -m "Initial commit: Django CMS with catalog API and worker"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create new repository name: `cms-backend` (or any name you prefer)
3. **Important**: DO NOT check "Add .gitignore" or "Add README" (we already have them)
4. Click "Create repository"

### 1.3 Connect & Push Code

Copy the commands from GitHub and run them:

```powershell
git remote add origin https://github.com/yourusername/cms-backend.git
git branch -M main
git push -u origin main
```

Replace `yourusername` with your actual GitHub username.

### 1.4 Verify on GitHub

- Visit your repo: https://github.com/yourusername/cms-backend
- Check that README displays on main page
- Verify .gitignore is working:
  - Should NOT see: `.venv/`, `__pycache__/`, `db.sqlite3`, `.env`
  - Should see: `README.md`, `requirements.txt`, `Dockerfile`, etc.


---

## 🧪 Step 2: Test Your Project Locally

**Before submitting**, make sure everything works:

### 2.1 Start the Server

```powershell
cd c:\Users\parim\OneDrive\Desktop\ChaiShots\cms_backend
.\.venv\Scripts\python.exe manage.py runserver
```

### 2.2 Test the Admin Panel

1. Visit: http://127.0.0.1:8000/admin/
2. Login with your credentials
3. You should see the dashboard

### 2.3 Create Test Data

In the admin panel, create:
1. **Program** - Click "Programs" → "Add Program"
   - Title: "Python 101"
   - Status: "published"
   - Language: "en"
   - Click Save

2. **Term** - Click "Terms" → "Add Term"
   - Program: Select the program you just created
   - Term Number: 1
   - Title: "Basics"
   - Click Save

3. **Lesson** - Click "Lessons" → "Add Lesson"
   - Term: Select the term you created
   - Lesson Number: 1
   - Title: "Introduction to Python"
   - Content Type: "video"
   - Status: "published"
   - Content Language Primary: "en"
   - Click Save

### 2.4 Test the Catalog API

1. Visit: http://127.0.0.1:8000/catalog/programs/
2. You should see JSON with your published program and lessons
3. Try filters:
   - http://127.0.0.1:8000/catalog/programs/?language=en
   - http://127.0.0.1:8000/catalog/programs/?limit=5

### 2.5 Stop the Server

Press `CTRL+C` in the terminal to stop the server.

---

## 📤 Step 3: What to Submit to the Company

### Email Template:

```
Subject: Django CMS - Take-Home Assignment Submission

Hi [Hiring Manager],

I've completed the CMS assignment. Here's what I've built:

📦 GitHub Repository:
https://github.com/yourusername/cms-backend

🎯 Key Features Implemented:
✅ Django CMS with admin interface
✅ Hierarchical content structure (Program → Term → Lesson)
✅ Scheduled publishing workflow
✅ Public catalog API (read-only REST API)
✅ Background worker for automated publishing
✅ Docker & Docker Compose support
✅ Full documentation in README

🔐 Test Credentials:
- Username: [your username]
- Password: [your password]

📖 How to Run Locally:
1. Clone the repo
2. Create virtual environment: python -m venv .venv
3. Activate: .venv\Scripts\activate
4. Install: pip install -r requirements.txt
5. Migrate: python manage.py migrate
6. Create user: python manage.py createsuperuser
7. Run: python manage.py runserver
8. Visit: http://127.0.0.1:8000/admin/

🐳 Or use Docker:
1. Clone the repo
2. docker-compose up --build
3. docker-compose exec web python manage.py createsuperuser
4. Visit: http://127.0.0.1:8000/admin/

📝 Project Structure:
- cms_backend/ - Django project settings
- core/ - Models, serializers, admin configuration
- worker/ - Background publishing worker
- README.md - Full documentation with API examples

🚀 Live Demo (if deployed):
[Optional: Add deployed URL if you deploy to Railway/Render]

Please let me know if you have any questions!

Best regards,
[Your Name]
```

---

## 🚀 Step 4: Deploy (Optional but Recommended)

If you want to show a live running version, deploy to a free platform:

### Option A: Railway (Easiest)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Select your `cms-backend` repository
6. Set environment variables:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   ```
7. Click "Deploy"

Then include in your submission:
```
🌐 Live Demo: https://your-app.railway.app/admin/
```

### Option B: Render

1. Go to https://render.com
2. Sign up
3. Click "New +"
4. Select "Web Service"
5. Connect GitHub repository
6. Set environment variables (same as Railway)
7. Deploy

---

## 📋 Final Checklist Before Submitting

- [ ] Code pushed to GitHub
- [ ] README visible on GitHub main page
- [ ] .gitignore working (no .venv, __pycache__, db.sqlite3 visible)
- [ ] Project runs locally without errors
- [ ] Admin panel accessible
- [ ] Catalog API working
- [ ] Test data created in admin
- [ ] All dependencies in requirements.txt
- [ ] Docker files present (Dockerfile, docker-compose.yml)
- [ ] Email drafted with GitHub link
- [ ] (Optional) Deployed to Railway/Render with live link

---

## ❓ Troubleshooting

### "Site can't be reached"
- Make sure server is running: `python manage.py runserver`
- Use exact URL: `http://127.0.0.1:8000/admin/`
- Don't use https, use http

### "No module named 'django'"
```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### "Database error"
```powershell
python manage.py migrate
```

### Port 8000 already in use
```powershell
python manage.py runserver 8001
```

---

## 📚 Files Git Will Track

✅ **Will be pushed:**
- README.md
- requirements.txt
- Dockerfile
- docker-compose.yml
- .env.example
- manage.py
- cms_backend/
- core/
- worker/

❌ **Will be ignored (in .gitignore):**
- .venv/
- __pycache__/
- *.pyc
- db.sqlite3
- .env
- .DS_Store
- .idea/

---

## 📞 Summary

1. **Initialize Git**: `git init` → `git add .` → `git commit -m "..."`
2. **Create GitHub repo** at https://github.com/new
3. **Push code**: `git remote add origin ...` → `git push -u origin main`
4. **Test locally**: `python manage.py runserver` → visit admin
5. **Create test data** in admin panel
6. **Email to company** with GitHub link + credentials + setup instructions
7. **(Optional) Deploy** to Railway/Render for live demo

---

## 🎉 You're Ready!

Your CMS is production-ready. The company will be impressed with:
- Clean, professional code
- Complete documentation
- Working admin panel
- Public API
- Docker support
- Automated publishing

Good luck with your submission! 🚀
