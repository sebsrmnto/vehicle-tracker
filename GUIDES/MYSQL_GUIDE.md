# MySQL Guide for Vehicle Tracker

## 🎯 Where to See Your Vehicles

**Your vehicles are stored in MySQL and displayed on the HOME PAGE!**

1. **In the Web App (Easiest):**
   - Go to: `http://localhost:5000/` (the home page)
   - After adding a vehicle, you'll be redirected here automatically
   - You'll see a table showing all your vehicles with:
     - ID, Brand, Model, Year, Plate Number
     - A "View" link to see details

2. **In MySQL Directly (Advanced):**
   - Open MySQL Command Line or MySQL Workbench
   - Connect using:
     - Host: `localhost`
     - User: `root`
     - Password: `Mibashishe87551_`
     - Database: `vehicle_tracker_db`
   - Run: `SELECT * FROM vehicles;`

---

## 📚 What is MySQL?

**MySQL is a database** - think of it like a digital filing cabinet:

- **Database** (`vehicle_tracker_db`) = The filing cabinet
- **Table** (`vehicles`) = A drawer in the cabinet
- **Rows** = Individual records (each vehicle you add)
- **Columns** = Fields (brand, model, year, plate_number)

### How Your App Uses MySQL:

1. **When you ADD a vehicle:**
   ```
   Form → Flask App → MySQL Database
   ```
   - You fill out the form on `/add_vehicle`
   - Flask takes your data
   - MySQL stores it in the `vehicles` table

2. **When you VIEW vehicles:**
   ```
   MySQL Database → Flask App → Web Page
   ```
   - You visit the home page (`/`)
   - Flask asks MySQL: "Give me all vehicles"
   - MySQL returns the data
   - Flask shows it in a table on the webpage

---

## 🔧 Setting Up the Database (If Not Done Yet)

If you get errors about the table not existing, run the SQL script:

1. **Option 1: MySQL Command Line**
   ```bash
   mysql -u root -p
   # Enter password: Mibashishe87551_
   ```
   Then:
   ```sql
   CREATE DATABASE IF NOT EXISTS vehicle_tracker_db;
   USE vehicle_tracker_db;
   SOURCE setup_database.sql;
   ```

2. **Option 2: MySQL Workbench**
   - Open MySQL Workbench
   - Connect to your server
   - Open and run `setup_database.sql`

3. **Option 3: Python Script**
   - Run: `python setup_database.py`

---

## 📊 Understanding the Vehicles Table

The `vehicles` table has these columns:
- `id` - Auto-incrementing number (1, 2, 3...)
- `brand` - Car brand (Toyota, Honda, etc.)
- `model` - Car model (Camry, Civic, etc.)
- `year` - Year (2020, 2021, etc.)
- `plate_number` - License plate

---

## 🚀 Quick Test

1. Make sure your Flask app is running: `python app.py`
2. Visit: `http://localhost:5000/add_vehicle`
3. Add a test vehicle
4. You'll be redirected to `http://localhost:5000/` 
5. **You should see your vehicle in the table!**

---

## ❓ Troubleshooting

**Problem: "Table doesn't exist"**
- Solution: Run `setup_database.py` (see above)

**Problem: "Can't connect to MySQL"**
- Make sure MySQL server is running
- Check your password in `db_config.py`

**Problem: "No vehicles showing"**
- Check if you actually added one (look for success message)
- Check MySQL directly: `SELECT * FROM vehicles;`
- Make sure you're on the home page (`/`), not `/add_vehicle`

