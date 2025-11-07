# 🚗 How to Use Your Vehicle Tracker App

## ✅ Database Setup (DONE!)
The `maintenance_logs` table has been created! You can now use all features.

---

## 🎯 Step-by-Step: How to Access ALL Features

### **1. Start Your App**
```bash
python app.py
```
Then open: `http://localhost:5000` in your browser

---

### **2. Home Page Features**

**What you'll see:**
- List of all your vehicles (in cards)
- Search box at the top
- "+ Add New Vehicle" button
- Statistics at the bottom

**What you can do:**
- ✅ **Search:** Type in the search box to find vehicles by brand, model, or plate number
- ✅ **Add Vehicle:** Click "+ Add New Vehicle" button
- ✅ **View Vehicle:** Click "View" button on any vehicle card
- ✅ **Edit Vehicle:** Click "Edit" button on any vehicle card
- ✅ **Delete Vehicle:** Click "Delete" button on any vehicle card

---

### **3. View Vehicle Details (THIS IS WHERE MAINTENANCE IS!)**

**How to get there:**
1. On home page, click **"View"** button on any vehicle card
2. OR go directly to: `http://localhost:5000/vehicle/4` (replace 4 with your vehicle ID)

**What you'll see:**
- Vehicle information (brand, model, year, plate)
- **Three buttons:**
  - ✏️ **Edit Vehicle** - Change vehicle info
  - 🔧 **Add Maintenance** - THIS IS THE MAINTENANCE FEATURE!
  - 🗑️ **Delete Vehicle** - Remove vehicle
- **Maintenance History section** (below vehicle info)
  - Shows all maintenance records for this vehicle
  - Each record shows: type, date, cost, description
  - Can delete individual maintenance records

---

### **4. Add Maintenance Log**

**How to get there:**
1. Click "View" on a vehicle
2. Click **"🔧 Add Maintenance"** button
3. OR go to: `http://localhost:5000/add_maintenance/4` (replace 4 with vehicle ID)

**What to fill:**
- **Maintenance Type** (required) - Dropdown menu:
  - Oil Change
  - Tire Rotation
  - Brake Service
  - Battery Replacement
  - Engine Repair
  - Transmission Service
  - Inspection
  - Other
- **Date** (required) - Use the date picker
- **Cost** (optional) - Enter amount like: 150.00
- **Description** (optional) - Add notes

**After submitting:**
- You'll be redirected back to the vehicle details page
- Your new maintenance log will appear in the "Maintenance History" section

---

### **5. Edit Vehicle**

**How to get there:**
- Click "Edit" button on home page
- OR click "✏️ Edit Vehicle" on vehicle details page

**What you can change:**
- Brand
- Model
- Year
- Plate Number

---

## 🔍 Quick Navigation Guide

```
Home Page (/)
    ├── View Vehicle → Vehicle Details Page
    │       ├── Add Maintenance → Add Maintenance Form
    │       ├── Edit Vehicle → Edit Vehicle Form
    │       └── Delete Vehicle → Back to Home
    ├── Edit Vehicle → Edit Vehicle Form
    ├── Delete Vehicle → Back to Home
    └── Add New Vehicle → Add Vehicle Form
```

---

## ❓ Common Questions

### **Q: Where is the maintenance feature?**
**A:** Click "View" on any vehicle, then you'll see:
- "🔧 Add Maintenance" button
- "Maintenance History" section below

### **Q: I can only add vehicles, nothing else works?**
**A:** After adding a vehicle:
1. You'll see it on the home page
2. Click the **"View"** button on the vehicle card
3. On the vehicle details page, you'll see all features including maintenance

### **Q: Why don't I see maintenance features?**
**A:** Make sure you:
1. Ran `python setup_database.py` (already done!)
2. Click "View" on a vehicle (not just the home page)
3. The maintenance section is on the vehicle details page

### **Q: How do I add maintenance?**
**A:** 
1. Go to home page
2. Click "View" on a vehicle
3. Click "🔧 Add Maintenance" button
4. Fill the form and submit

---

## 🎯 Feature Checklist

- [x] Add vehicles
- [x] View vehicles (home page)
- [x] Search vehicles
- [x] View vehicle details
- [x] Edit vehicles
- [x] Delete vehicles
- [x] **Add maintenance logs** ← This is the new feature!
- [x] **View maintenance history** ← On vehicle details page
- [x] **Delete maintenance logs** ← On vehicle details page

---

## 💡 Pro Tips

1. **Always click "View" first** - This is where all the maintenance features are!
2. **Maintenance is per vehicle** - Each vehicle has its own maintenance history
3. **Search works everywhere** - Use the search box on home page to find vehicles quickly
4. **Statistics update automatically** - Check the bottom of home page for fleet stats

---

## 🚨 Troubleshooting

**Error: Table doesn't exist**
- Run: `python setup_database.py`

**Can't see maintenance button**
- Make sure you clicked "View" on a vehicle first
- The button is on the vehicle details page, not home page

**Maintenance history is empty**
- That's normal! Add your first maintenance log using "Add Maintenance" button

---

**Need help? Check GUIDE.md for code structure or NOTES.md for learning explanations!**

