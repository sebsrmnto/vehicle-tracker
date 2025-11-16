# 🔧 Troubleshooting: Login/Signup Not Working in Production

If login and signup work locally but not in production (Railway), follow these steps:

## 🔍 Step 1: Check Railway Logs

**This is the most important step!**

1. Go to **Railway Dashboard** → Your Project
2. Click on your **web service** (not MySQL)
3. Go to **"Deployments"** tab
4. Click **"View logs"** on the latest deployment
5. Look for error messages when you try to login/signup

**Common errors you might see:**
- `Table 'users' doesn't exist` → Database tables not created (see Step 3)
- `Access denied for user` → Database credentials wrong (see Step 2)
- `Can't connect to MySQL server` → Database connection issue (see Step 2)
- `Unknown column 'password_hash'` → Database schema mismatch

---

## ⚙️ Step 2: Verify Environment Variables

**Go to Railway Dashboard → Your Web Service → "Variables" tab**

### Required Variables (must be set):

```
DB_HOST=<from MySQL service MYSQLHOST>
DB_USER=<from MySQL service MYSQLUSER>
DB_PASSWORD=<from MySQL service MYSQLPASSWORD>
DB_NAME=<from MySQL service MYSQLDATABASE>
SECRET_KEY=<any random string>
FLASK_DEBUG=False
PORT=5000
```

### How to get database variables:

1. Go to your **MySQL service** in Railway
2. Click **"Variables"** tab
3. Copy these values:
   - `MYSQLHOST` → use as `DB_HOST` in web service
   - `MYSQLUSER` → use as `DB_USER` in web service
   - `MYSQLPASSWORD` → use as `DB_PASSWORD` in web service
   - `MYSQLDATABASE` → use as `DB_NAME` in web service

### Important Notes:

- ✅ Variable names are **case-sensitive** - must be exactly `DB_HOST`, `DB_USER`, etc.
- ✅ No spaces around the `=` sign
- ✅ `SECRET_KEY` must be set (use a random string generator)
- ✅ After changing variables, Railway will auto-redeploy (wait 1-2 minutes)

---

## 🗄️ Step 3: Verify Database Tables Exist

**The `users` table MUST exist for login/signup to work!**

### Check if tables exist:

1. Go to Railway Dashboard → MySQL service
2. Click **"Connect"** tab
3. Use **"MySQL CLI"** or connect via external client
4. Run this SQL query:
   ```sql
   SHOW TABLES;
   ```
5. You should see: `users`, `vehicles`, `maintenance_logs`

### If tables don't exist:

**Option A: Using Railway CLI (Easiest)**

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Link project: `railway link` (select MySQL service)
4. Run setup:
   ```bash
   railway connect mysql < setup_database.sql
   ```

**Option B: Using MySQL Workbench or DBeaver**

1. Get connection details from Railway MySQL service → Variables tab
2. Connect using:
   - Host: `MYSQLHOST` value
   - Port: `MYSQLPORT` (usually 3306)
   - Username: `MYSQLUSER` value
   - Password: `MYSQLPASSWORD` value
   - Database: `MYSQLDATABASE` value
3. Open `setup_database.sql` from your project
4. Copy and paste all SQL commands
5. Execute

**Option C: Using Railway Web Console**

1. Go to MySQL service → "Connect" tab
2. Click "MySQL CLI"
3. Copy contents of `setup_database.sql`
4. Paste and execute line by line

---

## 🍪 Step 4: Check Session/Cookie Configuration

**If login works but you get logged out immediately:**

This might be a session cookie issue. Check:

1. **SECRET_KEY is set** in Railway variables (required!)
2. **HTTPS is enabled** - Railway uses HTTPS by default
3. **Browser console** - Check for cookie errors (F12 → Console)

### Test Session:

1. Try logging in
2. After successful login, check browser DevTools:
   - F12 → Application/Storage → Cookies
   - Look for `session` cookie
   - Should be present and not expired

---

## 🧪 Step 5: Test Database Connection

**Create a test endpoint to verify database connection:**

Visit: `https://your-app.railway.app/test-db`

This will show:
- ✅ Database connection status
- ✅ Tables that exist
- ✅ Environment variables (masked)

*(This endpoint will be added to your app)*

---

## 🐛 Common Issues & Solutions

### Issue 1: "An error occurred while logging in"

**Cause:** Database connection failed or table doesn't exist

**Solution:**
1. Check Railway logs (Step 1)
2. Verify environment variables (Step 2)
3. Verify tables exist (Step 3)

---

### Issue 2: Login succeeds but redirects back to login

**Cause:** Session cookie not being set/saved

**Solution:**
1. Check `SECRET_KEY` is set in Railway
2. Clear browser cookies and try again
3. Check browser console for cookie errors
4. Try in incognito/private window

---

### Issue 3: "Invalid email or password" for correct credentials

**Cause:** 
- User doesn't exist in production database
- Password hash mismatch (different SECRET_KEY used during signup)

**Solution:**
1. Create a new account via signup
2. If signup also fails, check database connection
3. Verify `users` table exists and has data

---

### Issue 4: Signup works but login doesn't

**Cause:** 
- User was created but password hash is wrong
- Database transaction didn't commit

**Solution:**
1. Check Railway logs for errors during signup
2. Verify database connection is stable
3. Try creating account again

---

### Issue 5: Works in one browser but not another

**Cause:** Cookie/session storage issue

**Solution:**
1. Clear cookies for the site
2. Disable browser extensions
3. Try incognito/private window
4. Check browser cookie settings

---

## 📋 Quick Diagnostic Checklist

Run through this checklist:

- [ ] Railway logs show no errors
- [ ] All environment variables are set correctly
- [ ] `users` table exists in database
- [ ] `SECRET_KEY` is set in Railway
- [ ] Database connection works (test endpoint)
- [ ] Browser allows cookies
- [ ] Tried in incognito/private window
- [ ] Cleared browser cache/cookies

---

## 🔍 How to Get More Information

### Enable Detailed Logging:

The app already logs errors. To see them:

1. Go to Railway Dashboard
2. Web service → Deployments → View logs
3. Try to login/signup
4. Watch the logs in real-time

### Check Database Directly:

1. Connect to Railway MySQL database
2. Run: `SELECT * FROM users;`
3. Verify users exist
4. Check if password_hash column exists

---

## 🆘 Still Not Working?

If none of the above works:

1. **Share Railway logs** - Copy error messages from logs
2. **Check database connection** - Verify you can connect to MySQL
3. **Test locally with production DB** - Temporarily point local app to Railway DB
4. **Verify deployment** - Make sure latest code is deployed

---

## 💡 Prevention Tips

1. **Always set environment variables** before first deployment
2. **Run database setup script** immediately after creating MySQL service
3. **Use different SECRET_KEY** for production (never use dev key)
4. **Test signup first** - Create account, then try login
5. **Check logs regularly** - Railway logs show what's happening

---

## 📞 Next Steps

After fixing the issue:

1. Test signup → should create account
2. Test login → should log in successfully
3. Test "Remember me" → should persist session
4. Test logout → should clear session

If all work, you're good to go! 🎉

