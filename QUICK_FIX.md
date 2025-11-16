# ⚡ Quick Fix Guide: Login/Signup Not Working

## 🎯 Most Common Issues (90% of cases)

### Issue #1: Database Tables Don't Exist ⚠️ **MOST COMMON**

**Symptom:** Login/signup shows error or redirects back to login

**Fix:**
1. Go to Railway Dashboard → MySQL service
2. Click "Connect" tab → "MySQL CLI"
3. Run this SQL:
   ```sql
   CREATE TABLE IF NOT EXISTS users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       email VARCHAR(255) NOT NULL UNIQUE,
       password_hash VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```
4. Or run the full `setup_database.sql` file

---

### Issue #2: Environment Variables Not Set

**Symptom:** "Database connection error" or "An error occurred"

**Fix:**
1. Go to Railway Dashboard → Your Web Service → "Variables" tab
2. Make sure these are set:
   ```
   DB_HOST=<from MySQL service>
   DB_USER=<from MySQL service>
   DB_PASSWORD=<from MySQL service>
   DB_NAME=<from MySQL service>
   SECRET_KEY=<any random string>
   ```
3. Get values from: MySQL service → Variables tab

---

### Issue #3: SECRET_KEY Not Set

**Symptom:** Login works but you get logged out immediately

**Fix:**
1. Go to Railway → Web Service → Variables
2. Add: `SECRET_KEY=your-random-string-here`
3. Generate random string: https://randomkeygen.com/
4. Railway will auto-redeploy

---

## 🔍 Diagnostic Tool

**Visit this URL on your deployed app:**
```
https://your-app.railway.app/test-db
```

This will show you:
- ✅ Database connection status
- ✅ Which tables exist
- ✅ Environment variables status
- ✅ Specific errors

---

## 📋 2-Minute Checklist

1. [ ] Visit `/test-db` endpoint - check what's wrong
2. [ ] Check Railway logs (Deployments → View logs)
3. [ ] Verify `users` table exists in database
4. [ ] Verify all environment variables are set
5. [ ] Verify `SECRET_KEY` is set
6. [ ] Try creating a new account (signup)
7. [ ] Clear browser cookies and try again

---

## 🆘 Still Not Working?

1. **Check Railway Logs:**
   - Go to Railway Dashboard
   - Web Service → Deployments → View logs
   - Try to login/signup
   - Copy the error message

2. **Test Database Connection:**
   - Visit `/test-db` endpoint
   - See what errors it shows

3. **Common Error Messages:**
   - `Table 'users' doesn't exist` → Run `setup_database.sql`
   - `Access denied` → Check DB credentials in Variables
   - `Can't connect` → Check DB_HOST and DB_PORT
   - No error but redirects → Check SECRET_KEY is set

---

## 💡 Pro Tips

- **Always check `/test-db` first** - it tells you exactly what's wrong
- **Check logs in real-time** - try login while watching logs
- **Test signup before login** - if signup fails, login will too
- **Use incognito window** - rules out browser cookie issues

---

For detailed troubleshooting, see `TROUBLESHOOTING.md`

