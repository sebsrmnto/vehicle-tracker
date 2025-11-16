# 🎯 How to Create the Users Table

## Method 1: Railway CLI (Easiest) ⭐

### Step 1: Install Railway CLI (if not installed)

**Windows PowerShell:**
```powershell
iwr https://railway.app/install.ps1 | iex
```

**Or using npm:**
```bash
npm i -g @railway/cli
```

### Step 2: Login and Connect

1. **Open your terminal/command prompt**

2. **Login to Railway:**
   ```bash
   railway login
   ```
   - This will open a browser window
   - Click "Authorize" in the browser

3. **Link to your project:**
   ```bash
   railway link
   ```
   - Select your workspace
   - Select "rare-charisma" project
   - Select "production" environment
   - **IMPORTANT:** Select **"MySQL"** service (not "web")

4. **Connect to MySQL:**
   ```bash
   railway connect MySQL
   ```
   - This opens a MySQL command prompt

5. **Run the SQL command:**
   ```sql
   CREATE TABLE IF NOT EXISTS users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       email VARCHAR(255) NOT NULL UNIQUE,
       password_hash VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

6. **Verify it worked:**
   ```sql
   SHOW TABLES;
   ```
   - You should see: `users`, `vehicles`, `maintenance_logs`

7. **Exit MySQL:**
   ```sql
   exit;
   ```

---

## Method 2: Using MySQL Workbench (Visual Tool)

### Step 1: Get Connection Details from Railway

1. Go to Railway Dashboard → MySQL service → **"Variables"** tab
2. Click the eye icon to reveal these values:
   - `MYSQLHOST` (hostname)
   - `MYSQLPORT` (port number)
   - `MYSQLUSER` (username)
   - `MYSQLPASSWORD` (password)
   - `MYSQLDATABASE` (database name)

### Step 2: Connect with MySQL Workbench

1. **Open MySQL Workbench**

2. **Create a new connection:**
   - Click "+" next to "MySQL Connections"
   - Fill in:
     - **Connection Name:** Railway MySQL
     - **Hostname:** (paste `MYSQLHOST` value)
     - **Port:** (paste `MYSQLPORT` value, usually 3306)
     - **Username:** (paste `MYSQLUSER` value)
     - **Password:** (click "Store in Keychain" and paste `MYSQLPASSWORD` value)

3. **Click "Test Connection"** - should say "Successfully made the MySQL connection"

4. **Click "OK"** to save

5. **Double-click** the connection to connect

### Step 3: Run SQL Command

1. **Click on the database** in the left sidebar (the one matching `MYSQLDATABASE`)

2. **Open a new query tab:**
   - Click "File" → "New Query Tab"
   - Or press `Ctrl+T`

3. **Paste this SQL:**
   ```sql
   CREATE TABLE IF NOT EXISTS users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       email VARCHAR(255) NOT NULL UNIQUE,
       password_hash VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

4. **Execute the query:**
   - Click the lightning bolt icon ⚡
   - Or press `Ctrl+Enter`

5. **Verify:**
   - In the left sidebar, expand your database
   - Expand "Tables"
   - You should see: `users`, `vehicles`, `maintenance_logs`

---

## Method 3: Using Command Line MySQL Client

### Step 1: Get Connection Details

From Railway MySQL service → Variables tab, get:
- `MYSQLHOST`
- `MYSQLPORT`
- `MYSQLUSER`
- `MYSQLPASSWORD`
- `MYSQLDATABASE`

### Step 2: Connect and Run SQL

**Windows (if you have MySQL installed):**
```bash
mysql -h <MYSQLHOST> -P <MYSQLPORT> -u <MYSQLUSER> -p<MYSQLPASSWORD> <MYSQLDATABASE>
```

Then paste the CREATE TABLE command.

---

## ✅ After Creating the Table

1. **Go back to Railway Dashboard**
2. **Click MySQL service → Database tab**
3. **Refresh the page**
4. **You should now see 3 tables:** `users`, `vehicles`, `maintenance_logs`

Then continue with Step 2: Setting up environment variables in your web service!

