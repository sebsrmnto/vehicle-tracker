# 🚀 Deployment Guide - Vehicle Maintenance Tracker

This guide will help you deploy your Flask application to various platforms.

## 📋 Prerequisites

1. ✅ All code pushed to GitHub
2. ✅ `requirements.txt` created (✅ Done!)
3. ✅ Environment variables configured
4. ✅ Database set up on hosting platform

---

## 🎯 Deployment Options

### Option 1: Railway (Recommended - Easy & Free)

**Railway** is one of the easiest platforms to deploy Flask apps with MySQL.

#### Steps:

1. **Sign up at Railway.app** (use GitHub login)

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `vehicle-tracker` repository

3. **Add MySQL Database**
   - In your project, click "+ New"
   - Select "Database" → "MySQL"
   - Railway will create a MySQL database automatically

4. **Configure Environment Variables**
   - Go to your project settings
   - Add these variables:
     ```
     DB_HOST=<provided by Railway>
     DB_USER=<provided by Railway>
     DB_PASSWORD=<provided by Railway>
     DB_NAME=<provided by Railway>
     FLASK_DEBUG=False
     PORT=5000
     SECRET_KEY=<generate a random string>
     ```

5. **Set Build Command** (if needed)
   - Railway usually auto-detects Flask apps
   - Build command: `pip install -r requirements.txt`
   - Start command: `python app.py` (or Railway will auto-detect)

6. **Initialize Database**
   - Go to your MySQL database in Railway
   - Copy the connection details
   - Run `setup_database.py` locally with those credentials, OR
   - Connect to the database and run `setup_database.sql`

7. **Deploy!**
   - Railway will automatically deploy on every push to main
   - Your app will be live at `https://your-app-name.railway.app`

---

### Option 2: Render (Free Tier Available)

**Render** offers free hosting with some limitations.

#### Steps:

1. **Sign up at render.com** (use GitHub login)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `vehicle-tracker` repo

3. **Configure Settings:**
   - **Name:** vehicle-tracker (or your choice)
   - **Region:** Choose closest to you
   - **Branch:** main
   - **Root Directory:** (leave empty - root is fine)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

4. **Add PostgreSQL Database** (Render uses PostgreSQL, not MySQL)
   - Click "New +" → "PostgreSQL"
   - Create a new database
   - **Note:** You'll need to modify your code to use PostgreSQL instead of MySQL
   - Or use a MySQL service like **PlanetScale** (free tier)

5. **Add Environment Variables:**
   ```
   DB_HOST=<from database>
   DB_USER=<from database>
   DB_PASSWORD=<from database>
   DB_NAME=<from database>
   FLASK_DEBUG=False
   SECRET_KEY=<random string>
   ```

6. **Deploy!**
   - Render will build and deploy your app
   - Free tier apps spin down after 15 minutes of inactivity

---

### Option 3: Heroku (Requires Credit Card for MySQL)

**Heroku** is popular but requires a credit card for MySQL add-ons.

#### Steps:

1. **Install Heroku CLI** from heroku.com

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create App:**
   ```bash
   heroku create your-app-name
   ```

4. **Add MySQL Database:**
   ```bash
   heroku addons:create cleardb:ignite
   ```

5. **Get Database URL:**
   ```bash
   heroku config:get CLEARDB_DATABASE_URL
   ```

6. **Set Environment Variables:**
   ```bash
   heroku config:set FLASK_DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key-here
   ```

7. **Deploy:**
   ```bash
   git push heroku main
   ```

8. **Initialize Database:**
   ```bash
   heroku run python setup_database.py
   ```

---

### Option 4: PythonAnywhere (Free Tier Available)

**PythonAnywhere** is great for Python web apps.

#### Steps:

1. **Sign up at pythonanywhere.com** (free account)

2. **Create New Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Flask, Python 3.10

3. **Upload Your Code:**
   - Go to "Files" tab
   - Upload your project files
   - Or clone from GitHub

4. **Configure WSGI file:**
   - Edit the WSGI file to point to your `app.py`

5. **Set up MySQL:**
   - PythonAnywhere provides MySQL database
   - Get credentials from "Databases" tab
   - Update your `db_config.py` or use environment variables

6. **Install Dependencies:**
   - Go to "Consoles" tab
   - Open a Bash console
   - Run: `pip3.10 install --user flask mysql-connector-python python-dotenv`

7. **Initialize Database:**
   - Run `setup_database.py` in the console

8. **Reload Web App:**
   - Go back to "Web" tab
   - Click "Reload" button

---

## 🔧 Common Deployment Issues & Solutions

### Issue 1: Database Connection Failed
**Solution:**
- Make sure environment variables are set correctly
- Check that database host allows connections from your deployment platform
- Some platforms require specific database URLs

### Issue 2: Module Not Found Error
**Solution:**
- Make sure `requirements.txt` includes all dependencies
- Check that build command runs `pip install -r requirements.txt`

### Issue 3: App Crashes on Start
**Solution:**
- Check logs in your deployment platform
- Make sure `PORT` environment variable is set (some platforms use `PORT`, others auto-detect)
- Verify database is accessible

### Issue 4: Static Files Not Loading
**Solution:**
- Flask should serve static files automatically
- Check that `static/` folder is in the root directory
- Verify file paths in templates use `url_for('static', ...)`

---

## 📝 Important Notes

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use environment variables** for all sensitive data (passwords, keys)
3. **Set `FLASK_DEBUG=False`** in production
4. **Generate a strong `SECRET_KEY`** for production
5. **Database must be accessible** from your hosting platform

---

## 🆘 Need Help?

If deployment fails:
1. Check the logs in your hosting platform
2. Verify all environment variables are set
3. Make sure database is initialized
4. Check that `requirements.txt` is correct
5. Ensure your code is pushed to GitHub main branch

---

## ✅ Quick Checklist

- [ ] Code pushed to GitHub
- [ ] `requirements.txt` created
- [ ] Environment variables configured
- [ ] Database created on hosting platform
- [ ] Database initialized (tables created)
- [ ] `FLASK_DEBUG=False` in production
- [ ] `SECRET_KEY` set to a random string
- [ ] App deployed and accessible

---

**Good luck with your deployment! 🚀**

