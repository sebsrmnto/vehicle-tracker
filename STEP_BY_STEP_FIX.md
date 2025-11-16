# 🎯 Step-by-Step Fix: Login/Signup Not Working

## ✅ Step 1: Create the Missing `users` Table

**Problem:** Your database is missing the `users` table (you only see `vehicles` and `maintenance_logs`)

**Fix:**

1. **In Railway Dashboard:**
   - You should be on the **MySQL** service (left sidebar)
   - Click the **"Connect"** button (top right corner)

2. **Select "MySQL CLI"** from the dropdown

3. **Copy and paste this SQL command:**
   ```sql
   CREATE TABLE IF NOT EXISTS users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       email VARCHAR(255) NOT NULL UNIQUE,
       password_hash VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

4. **Press Enter** to run it

5. **Verify it worked:**
   - Type: `SHOW TABLES;`
   - Press Enter
   - You should now see: `users`, `vehicles`, `maintenance_logs`

6. **Close the MySQL CLI** (you can close the terminal/connection)

---

## ✅ Step 2: Set Up Database Connection Variables

**Problem:** Your web service doesn't know how to connect to the database

**Fix:**

1. **In Railway Dashboard:**
   - Click on **"web"** service in the left sidebar (the one with GitHub icon)
   - Click the **"Variables"** tab at the top

2. **Add these 5 variables one by one:**

   Click **"+ New Variable"** and add each of these:

   **Variable 1:**
   - Name: `DB_HOST`
   - Value: `${{ MySQL.MYSQLHOST }}`
   - Click Save

   **Variable 2:**
   - Name: `DB_USER`
   - Value: `${{ MySQL.MYSQLUSER }}`
   - Click Save

   **Variable 3:**
   - Name: `DB_PASSWORD`
   - Value: `${{ MySQL.MYSQLPASSWORD }}`
   - Click Save

   **Variable 4:**
   - Name: `DB_NAME`
   - Value: `${{ MySQL.MYSQLDATABASE }}`
   - Click Save

   **Variable 5:**
   - Name: `SECRET_KEY`
   - Value: `your-random-secret-key-here-12345` (use any random string)
   - Click Save

3. **Wait 1-2 minutes** - Railway will automatically redeploy your app

---

## ✅ Step 3: Test It!

1. **Visit your deployed app URL** (the one Railway gave you)

2. **Try to sign up:**
   - Click "Sign up"
   - Enter email and password
   - Click "Sign In" button
   - Should work! ✅

3. **Or test the diagnostic page:**
   - Visit: `https://your-app-url.railway.app/test-db`
   - Should show all tables exist ✅

---

## 🎉 That's It!

After these 3 steps, login and signup should work!

---

## ❓ Troubleshooting

**If Step 1 doesn't work:**
- Make sure you're in the MySQL CLI
- Copy the SQL exactly as shown
- Check for any error messages

**If Step 2 doesn't work:**
- Make sure you're adding variables to the **"web"** service (not MySQL)
- Variable names must be exact: `DB_HOST`, `DB_USER`, etc.
- Values must use the exact syntax: `${{ MySQL.MYSQLHOST }}`

**If it still doesn't work:**
- Visit `/test-db` endpoint to see what's wrong
- Check Railway logs: Web service → Deployments → View logs

