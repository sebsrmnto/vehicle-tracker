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

### Option A: Using Railway MySQL Console (Easiest)
1. Go to your **MySQL service** in Railway
2. Click **"Data"** or **"Connect"** tab
3. Open the MySQL console
4. Copy the contents of `setup_database.sql` from your project
5. Paste and run it in the console

### Option B: Run Setup Script Locally
1. Get database credentials from Railway MySQL service Variables
2. Temporarily update `db_config.py` with Railway's credentials
3. Run: `python setup_database.py`
4. Restore your local `db_config.py` (or use `.env` file)

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

