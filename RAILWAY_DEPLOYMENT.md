# 🚂 Railway Deployment Guide

## ✅ Your App is Deployed!

Your app is live on Railway. If it's not working, follow these steps:

---

## 🔍 Step 1: Check if You Have a Database

**Go to Railway Dashboard → Your Project → Check if you see a MySQL service**

### If NO database exists:
1. Click **"+ New"** button
2. Select **"Database"** → **"MySQL"**
3. Wait 1-2 minutes for it to be created

### If database EXISTS:
Continue to Step 2.

---

## ⚙️ Step 2: Set Environment Variables

**Go to your "vehicle-tracker" service → "Variables" tab**

### Required Variables:

1. **Database Variables** (get these from your MySQL service):
   - Click on your MySQL service
   - Go to "Variables" tab
   - Copy these values:
     - `MYSQLHOST` → use as `DB_HOST`
     - `MYSQLUSER` → use as `DB_USER`
     - `MYSQLPASSWORD` → use as `DB_PASSWORD`
     - `MYSQLDATABASE` → use as `DB_NAME`

2. **Add to your web service Variables:**
   ```
   DB_HOST=<paste MYSQLHOST value>
   DB_USER=<paste MYSQLUSER value>
   DB_PASSWORD=<paste MYSQLPASSWORD value>
   DB_NAME=<paste MYSQLDATABASE value>
   FLASK_DEBUG=False
   SECRET_KEY=<any random string, use a password generator>
   PORT=5000
   ```

3. **Save** - Railway will automatically redeploy

---

## 🗄️ Step 3: Set Up Database Tables

You need to create the database tables. Choose one method:

### Option A: Using Railway CLI (Recommended - Easiest)

1. **Install Railway CLI** (if not already installed):
   - Visit: https://docs.railway.app/develop/cli
   - Or run: `npm i -g @railway/cli` (requires Node.js)

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Link to your project**:
   ```bash
   railway link
   ```
   - Select your workspace
   - Select your project
   - Select environment (usually "production")
   - **Select the "MySQL" service** (not "web") - you need to connect to the database

4. **Connect to MySQL and run the setup script**:
   ```bash
   railway connect mysql < setup_database.sql
   ```
   
   Or connect interactively:
   ```bash
   railway connect mysql
   ```
   Then paste the contents of `setup_database.sql` line by line.

### Option B: Using External MySQL Client (MySQL Workbench, DBeaver, etc.)

1. **Get connection details from Railway**:
   - Go to your **MySQL service** in Railway
   - Click **"Variables"** tab
   - Note these values:
     - `MYSQLHOST` (hostname)
     - `MYSQLPORT` (usually 3306)
     - `MYSQLUSER` (username)
     - `MYSQLPASSWORD` (password)
     - `MYSQLDATABASE` (database name)

2. **Connect using MySQL Workbench or another client**:
   - Host: `MYSQLHOST` value
   - Port: `MYSQLPORT` value (usually 3306)
   - Username: `MYSQLUSER` value
   - Password: `MYSQLPASSWORD` value
   - Database: `MYSQLDATABASE` value

3. **Run the SQL script**:
   - Open `setup_database.sql` from your project
   - Copy all contents
   - Paste and execute in your MySQL client

### Option C: Using Command Line (if you have MySQL client installed)

1. **Get connection details** from Railway MySQL service Variables tab

2. **Connect from your terminal**:
   ```bash
   mysql -h <MYSQLHOST> -P <MYSQLPORT> -u <MYSQLUSER> -p<MYSQLPASSWORD> <MYSQLDATABASE> < setup_database.sql
   ```
   
   Replace the placeholders with actual values from Railway Variables.

### Option D: Run Setup Script Locally (Python)

1. **Get database credentials** from Railway MySQL service Variables tab

2. **Temporarily update `db_config.py`** with Railway's credentials:
   ```python
   DB_HOST = "<MYSQLHOST value>"
   DB_USER = "<MYSQLUSER value>"
   DB_PASSWORD = "<MYSQLPASSWORD value>"
   DB_NAME = "<MYSQLDATABASE value>"
   ```

3. **Run the setup script**:
   ```bash
   python setup_database.py
   ```

4. **Restore your local `db_config.py`** (or use `.env` file for local development)

---

## 🔗 Step 4: Make Your App Public (Optional)

**If your app shows "Unexposed service":**
1. Go to your "vehicle-tracker" service
2. Click **"Settings"** tab
3. Click **"Generate Domain"** button
4. Your app will be accessible at the generated URL

---

## 🐛 Troubleshooting

### App Shows Error Page:
1. Go to **"Deployments"** tab
2. Click **"View logs"** on the latest deployment
3. Look for error messages

### Common Errors:

**"Database connection failed"**
- Check that environment variables are set correctly
- Make sure MySQL service is running
- Verify variable names match exactly (case-sensitive)

**"Table doesn't exist"**
- Run `setup_database.sql` in MySQL console (Step 3)

**"Module not found"**
- Check that `requirements.txt` exists in your GitHub repo
- Railway should install dependencies automatically

---

## 📋 Quick Checklist

- [ ] MySQL database service created
- [ ] Environment variables set in web service
- [ ] Database tables created (run setup_database.sql)
- [ ] App is exposed/public (if needed)
- [ ] Check logs for any errors

---

## 🎯 What Happens Next?

After completing these steps:
1. Railway will automatically redeploy your app
2. Wait 1-2 minutes for deployment to complete
3. Visit your app URL
4. Try adding a vehicle to test if everything works

---

## 📞 Need Help?

1. **Check the logs** in Railway Dashboard → Deployments → View logs
2. **Verify all variables** are set correctly
3. **Make sure database tables exist** (run setup_database.sql)

Your app should work after completing these steps! 🎉

