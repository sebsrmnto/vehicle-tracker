# 📚 Code Guide - Vehicle Tracker App

This guide organizes all code by feature and file, making it easy to understand the project structure.

---

## 🗂️ Project Structure

```
vehicle-tracker/
├── app.py                 # Main Flask application (routes & logic)
├── db_config.py           # Database connection configuration
├── setup_database.py      # Database setup script
├── setup_database.sql     # SQL schema file
├── static/
│   └── style.css         # CSS styling
├── templates/
│   ├── index.html        # Home page (vehicle list)
│   ├── add_vehicles.html # Add vehicle form
│   ├── edit_vehicle.html # Edit vehicle form
│   ├── view_log.html     # Vehicle details page
│   └── add_maintenance.html # Add maintenance form
└── GUIDE.md              # This file (code organization)
└── NOTES.md              # Learning explanations
```

---

## 📁 File-by-File Breakdown

### **app.py** - Main Application
**Purpose:** Handles all web routes and business logic

**Routes:**
- `GET /` - Home page (list all vehicles, search, statistics)
- `GET/POST /add_vehicle` - Add new vehicle form
- `GET /vehicle/<id>` - View vehicle details (with maintenance logs)
- `GET/POST /edit_vehicle/<id>` - Edit vehicle form
- `POST /delete_vehicle/<id>` - Delete vehicle
- `GET/POST /add_maintenance/<vehicle_id>` - Add maintenance log
- `POST /delete_maintenance/<maintenance_id>` - Delete maintenance log

**Key Functions:**
- `index()` - Displays vehicles with search and stats
- `add_vehicle()` - Handles vehicle creation
- `view_vehicle()` - Shows vehicle details and maintenance logs
- `edit_vehicle()` - Handles vehicle updates
- `delete_vehicle()` - Handles vehicle deletion
- `add_maintenance()` - Handles maintenance log creation
- `delete_maintenance()` - Handles maintenance log deletion

---

### **db_config.py** - Database Configuration
**Purpose:** Manages MySQL database connection

**Functions:**
- `get_db_connection()` - Returns database connection object

**Configuration:**
- Host: localhost
- Database: vehicle_tracker_db
- User credentials stored here

---

### **setup_database.py** - Database Setup
**Purpose:** Creates database and tables automatically

**Functions:**
- `setup_database()` - Creates database and tables

**What it does:**
1. Connects to MySQL server
2. Creates `vehicle_tracker_db` database
3. Creates `vehicles` table with columns
4. Creates `maintenance_logs` table with columns
5. Verifies setup

---

### **templates/index.html** - Home Page
**Purpose:** Main page showing all vehicles

**Features:**
- Vehicle cards grid
- Search functionality
- Statistics display
- Add vehicle button
- Action buttons (View/Edit/Delete)

---

### **templates/add_vehicles.html** - Add Vehicle Form
**Purpose:** Form to add new vehicles

**Fields:**
- Brand
- Model
- Year
- Plate Number

---

### **templates/edit_vehicle.html** - Edit Vehicle Form
**Purpose:** Form to edit existing vehicles

**Features:**
- Pre-filled form with current data
- Updates vehicle in database

---

### **templates/view_log.html** - Vehicle Details
**Purpose:** Shows detailed information about a vehicle

**Features:**
- Vehicle information display
- Edit/Delete buttons
- Add Maintenance button
- Maintenance history section
- List of all maintenance logs
- Delete individual maintenance logs
- Back to home link

---

### **templates/add_maintenance.html** - Add Maintenance Form
**Purpose:** Form to add maintenance records for a vehicle

**Fields:**
- Maintenance Type (dropdown: Oil Change, Tire Rotation, etc.)
- Date (required)
- Cost (optional, decimal)
- Description (optional, text area)

---

### **static/style.css** - Styling
**Purpose:** All CSS styles for the application

**Styles:**
- Container layouts
- Card designs
- Button styles
- Form styling
- Responsive design

---

## 🔧 Features by Category

### **Vehicle Management**
- ✅ Add vehicles
- ✅ View vehicles
- ✅ Edit vehicles
- ✅ Delete vehicles
- ✅ Search vehicles

### **Statistics**
- ✅ Total vehicle count
- ✅ Oldest vehicle year
- ✅ Newest vehicle year

### **Maintenance Log**
- ✅ Add maintenance records
- ✅ View maintenance history
- ✅ Delete maintenance records
- ✅ Track maintenance type, date, cost, and description

---

## 🔄 Data Flow

1. **User Action** → HTML form/template
2. **Form Submit** → Flask route in `app.py`
3. **Route Handler** → Database query via `db_config.py`
4. **Database** → MySQL returns data
5. **Route Handler** → Renders template with data
6. **Template** → User sees result

---

## 📝 Last Updated
- **Date:** Maintenance Log Feature Added
- **Features:** Basic CRUD operations, search, statistics, maintenance log tracking

---

## 🗄️ Database Tables

### **vehicles** Table
- `id` - Primary key
- `brand` - Vehicle brand
- `model` - Vehicle model
- `year` - Manufacturing year
- `plate_number` - License plate
- `created_at` - Timestamp

### **maintenance_logs** Table
- `id` - Primary key
- `vehicle_id` - Foreign key to vehicles table
- `maintenance_type` - Type of maintenance (Oil Change, etc.)
- `description` - Optional description
- `cost` - Optional cost (decimal)
- `maintenance_date` - Date of maintenance
- `created_at` - Timestamp
- **Foreign Key:** Links to vehicles table (CASCADE delete)

