#  Vehicle Maintenance Tracker

A full-stack web application for tracking vehicles and their maintenance records, built with Flask and MySQL.

## ✨ Features

- **Vehicle Management**
  - Add, view, edit, and delete vehicles
  - Search vehicles by brand, model, or plate number
  - View fleet statistics

- **Maintenance Tracking**
  - Record maintenance history for each vehicle
  - Track maintenance type, date, cost, and description
  - View complete maintenance history per vehicle
  - Delete maintenance records

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, Jinja2 Templates

## 📋 Prerequisites

- Python 3.x
- MySQL Server
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/vehicle-tracker.git
   cd vehicle-tracker
   ```

2. **Install dependencies:**
   ```bash
   pip install flask mysql-connector-python
   ```

3. **Configure database:**
   - Update `db_config.py` with your MySQL credentials
   - Or create a `.env` file (see `db_config.example.py`)

4. **Set up database:**
   ```bash
   python setup_database.py
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open in browser:**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
vehicle-tracker/
├── app.py                 # Main Flask application
├── db_config.py           # Database configuration
├── setup_database.py      # Database setup script
├── setup_database.sql     # SQL schema
├── static/
│   └── style.css         # CSS styles
├── templates/
│   ├── index.html        # Home page
│   ├── add_vehicles.html # Add vehicle form
│   ├── edit_vehicle.html # Edit vehicle form
│   ├── view_log.html     # Vehicle details
│   └── add_maintenance.html # Add maintenance form
├── GUIDE.md              # Code organization guide
├── NOTES.md              # Learning notes
└── HOW_TO_USE.md         # Usage guide
```

## 📚 Documentation

- **GUIDE.md** - Code structure and organization
- **NOTES.md** - Learning explanations and concepts
- **HOW_TO_USE.md** - Step-by-step usage guide
- **GITHUB_SETUP.md** - GitHub setup instructions

## 🔒 Security Note

⚠️ **Important:** The `db_config.py` file contains database credentials. For production:
- Use environment variables (see `db_config.example.py`)
- Never commit passwords to public repositories
- Use `.env` files (already in `.gitignore`)

## 🎯 Usage

1. **Add a vehicle:** Click "+ Add New Vehicle" on home page
2. **View vehicle:** Click "View" button on any vehicle card
3. **Add maintenance:** On vehicle details page, click "🔧 Add Maintenance"
4. **Search:** Use the search box on home page
5. **Edit/Delete:** Use buttons on vehicle cards or details page

## 🤝 Contributing

This is a learning project. Feel free to fork, modify, and learn from it!

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

- Sebastian S. Sarmiento

---


