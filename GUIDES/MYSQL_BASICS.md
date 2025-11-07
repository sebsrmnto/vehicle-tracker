# 🗄️ MySQL Basics for Your Vehicle Tracker

## 🎯 Understanding MySQL in Your App

This guide explains the MySQL/SQL concepts used in your vehicle tracker app.

---

## 📚 What is SQL?

**SQL** = Structured Query Language
- It's the language you use to talk to MySQL
- Think of it like giving commands to your database

---

## 🔍 SQL Commands Used in Your App

### 1️⃣ **SELECT - Read Data**

**What it does:** Gets data from the database

```sql
SELECT * FROM vehicles;
```

**Breakdown:**
- `SELECT` = "Get me"
- `*` = "everything" (all columns)
- `FROM vehicles` = "from the vehicles table"

**In your app:**
```python
cursor.execute("SELECT * FROM vehicles")
vehicles = cursor.fetchall()  # Get all results
```

**Other SELECT examples:**
```sql
SELECT brand, model FROM vehicles;           -- Get only brand and model
SELECT * FROM vehicles WHERE id = 1;         -- Get vehicle with id = 1
SELECT * FROM vehicles WHERE brand = 'Toyota'; -- Get all Toyotas
```

---

### 2️⃣ **INSERT - Add New Data**

**What it does:** Adds a new record to the database

```sql
INSERT INTO vehicles (brand, model, year, plate_number) 
VALUES ('Toyota', 'Camry', 2020, 'ABC-1234');
```

**Breakdown:**
- `INSERT INTO vehicles` = "Add to vehicles table"
- `(brand, model, year, plate_number)` = "These columns"
- `VALUES (...)` = "With these values"

**In your app:**
```python
cursor.execute(
    "INSERT INTO vehicles (brand, model, year, plate_number) VALUES (%s, %s, %s, %s)",
    (brand, model, year, plate)
)
```

**Why `%s`?**
- `%s` = placeholder (prevents SQL injection attacks!)
- Python fills in the actual values
- `(brand, model, year, plate)` = the actual values

---

### 3️⃣ **UPDATE - Change Existing Data**

**What it does:** Modifies an existing record

```sql
UPDATE vehicles 
SET brand = 'Honda', year = 2021 
WHERE id = 1;
```

**Breakdown:**
- `UPDATE vehicles` = "Change the vehicles table"
- `SET brand = 'Honda'` = "Set brand to Honda"
- `WHERE id = 1` = "Only for the vehicle with id = 1"

**⚠️ CRITICAL: Always use WHERE!**
```sql
-- DANGEROUS - Updates ALL vehicles!
UPDATE vehicles SET brand = 'Honda';

-- SAFE - Updates only one vehicle
UPDATE vehicles SET brand = 'Honda' WHERE id = 1;
```

**In your app:**
```python
cursor.execute(
    "UPDATE vehicles SET brand = %s, model = %s, year = %s, plate_number = %s WHERE id = %s",
    (brand, model, year, plate, vehicle_id)
)
```

---

### 4️⃣ **DELETE - Remove Data**

**What it does:** Removes a record from the database

```sql
DELETE FROM vehicles WHERE id = 1;
```

**Breakdown:**
- `DELETE FROM vehicles` = "Remove from vehicles table"
- `WHERE id = 1` = "Only the vehicle with id = 1"

**⚠️ CRITICAL: Always use WHERE!**
```sql
-- DANGEROUS - Deletes ALL vehicles!
DELETE FROM vehicles;

-- SAFE - Deletes only one vehicle
DELETE FROM vehicles WHERE id = 1;
```

**In your app:**
```python
cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
```

---

## 🗂️ Understanding Your Database Structure

### **Table: vehicles**

Your `vehicles` table has these columns:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INT | Auto-incrementing number (1, 2, 3...) |
| `brand` | VARCHAR(100) | Car brand (Toyota, Honda, etc.) |
| `model` | VARCHAR(100) | Car model (Camry, Civic, etc.) |
| `year` | INT | Year (2020, 2021, etc.) |
| `plate_number` | VARCHAR(50) | License plate |
| `created_at` | TIMESTAMP | When it was added |

### **What Each Type Means:**

- **INT** = Integer (whole numbers: 1, 2, 2020)
- **VARCHAR(100)** = Text up to 100 characters
- **TIMESTAMP** = Date and time

---

## 🔐 Important SQL Concepts

### **1. WHERE Clause**

**Always use WHERE to target specific records!**

```sql
-- Get vehicle with id = 1
SELECT * FROM vehicles WHERE id = 1;

-- Get all Toyotas
SELECT * FROM vehicles WHERE brand = 'Toyota';

-- Get vehicles from 2020 or newer
SELECT * FROM vehicles WHERE year >= 2020;
```

**Comparison operators:**
- `=` equals
- `!=` not equals
- `>` greater than
- `<` less than
- `>=` greater than or equal
- `<=` less than or equal

---

### **2. Placeholders (%s)**

**Why use `%s` instead of direct values?**

**❌ BAD (SQL Injection risk):**
```python
cursor.execute(f"INSERT INTO vehicles (brand) VALUES ('{user_input}')")
# If user_input = "'; DROP TABLE vehicles; --"
# This could delete your table!
```

**✅ GOOD (Safe):**
```python
cursor.execute("INSERT INTO vehicles (brand) VALUES (%s)", (user_input,))
# Python safely handles the value
```

**Always use `%s` placeholders!**

---

### **3. Transactions (commit/rollback)**

**What they do:**
- `commit()` = Save the changes permanently
- `rollback()` = Undo the changes

**In your app:**
```python
try:
    cursor.execute("INSERT INTO...")
    conn.commit()      # Save it!
except Exception as e:
    conn.rollback()    # Undo if error!
```

**Why this matters:**
- If something goes wrong, changes are undone
- Prevents partial/corrupted data

---

## 📊 Common SQL Patterns in Your App

### **Pattern 1: Get All Records**

```python
cursor.execute("SELECT * FROM vehicles")
vehicles = cursor.fetchall()
```

**What happens:**
1. Execute SQL query
2. `fetchall()` gets all results
3. Returns list of dictionaries

---

### **Pattern 2: Get One Record**

```python
cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
vehicle = cursor.fetchone()
```

**What happens:**
1. Execute SQL with WHERE clause
2. `fetchone()` gets first result
3. Returns one dictionary (or None if not found)

---

### **Pattern 3: Insert New Record**

```python
cursor.execute(
    "INSERT INTO vehicles (brand, model, year, plate_number) VALUES (%s, %s, %s, %s)",
    (brand, model, year, plate)
)
conn.commit()
```

**What happens:**
1. Execute INSERT with placeholders
2. Python fills in values safely
3. Commit saves to database

---

## 🎓 SQL Practice Exercises

### **Exercise 1: Write a SELECT query**

**Task:** Get all vehicles from 2020 or newer

**Answer:**
```sql
SELECT * FROM vehicles WHERE year >= 2020;
```

---

### **Exercise 2: Write an UPDATE query**

**Task:** Change the plate number of vehicle with id = 1 to "NEW-1234"

**Answer:**
```sql
UPDATE vehicles SET plate_number = 'NEW-1234' WHERE id = 1;
```

---

### **Exercise 3: Write a DELETE query**

**Task:** Delete all vehicles from 2010 or older

**Answer:**
```sql
DELETE FROM vehicles WHERE year <= 2010;
```

---

## 🚨 Common Mistakes to Avoid

### **Mistake 1: Forgetting WHERE clause**

```sql
-- ❌ BAD - Updates ALL vehicles!
UPDATE vehicles SET brand = 'Toyota';

-- ✅ GOOD - Updates only one
UPDATE vehicles SET brand = 'Toyota' WHERE id = 1;
```

### **Mistake 2: SQL Injection**

```python
# ❌ BAD - Dangerous!
cursor.execute(f"INSERT INTO vehicles (brand) VALUES ('{user_input}')")

# ✅ GOOD - Safe!
cursor.execute("INSERT INTO vehicles (brand) VALUES (%s)", (user_input,))
```

### **Mistake 3: Forgetting to commit**

```python
# ❌ BAD - Changes not saved!
cursor.execute("INSERT INTO...")
# Missing conn.commit()

# ✅ GOOD - Changes saved!
cursor.execute("INSERT INTO...")
conn.commit()
```

---

## 📖 SQL Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `SELECT` | Read data | `SELECT * FROM vehicles;` |
| `INSERT` | Add data | `INSERT INTO vehicles (brand) VALUES ('Toyota');` |
| `UPDATE` | Change data | `UPDATE vehicles SET brand = 'Honda' WHERE id = 1;` |
| `DELETE` | Remove data | `DELETE FROM vehicles WHERE id = 1;` |
| `WHERE` | Filter records | `SELECT * FROM vehicles WHERE brand = 'Toyota';` |

---

## ✅ Key Takeaways

1. **SELECT** - Read data from database
2. **INSERT** - Add new records
3. **UPDATE** - Modify existing records (always use WHERE!)
4. **DELETE** - Remove records (always use WHERE!)
5. **WHERE** - Critical for targeting specific records
6. **%s placeholders** - Always use for safety
7. **commit()** - Save changes permanently
8. **rollback()** - Undo changes if error

---

## 🚀 Next Steps

1. **Try SQL in MySQL Workbench** - Practice the commands
2. **Understand your app's queries** - Look at each `cursor.execute()`
3. **Experiment safely** - Try SELECT queries first (they don't change data)
4. **Learn more SQL** - COUNT, ORDER BY, LIMIT, etc.

**Remember:** SQL is powerful! Always test queries, especially UPDATE and DELETE! 🎯

