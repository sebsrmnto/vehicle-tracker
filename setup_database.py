"""
Database Setup Script
Run this to create the database and vehicles table automatically
"""
import mysql.connector
from db_config import get_db_connection

def setup_database():
    """Create the database and vehicles table if they don't exist"""
    try:
        # First, connect without specifying database (to create it)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mibashishe87551_"
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS vehicle_tracker_db")
        print("[OK] Database 'vehicle_tracker_db' ready")
        
        cursor.close()
        conn.close()
        
        # Now connect to the database and create table
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create vehicles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                brand VARCHAR(100) NOT NULL,
                model VARCHAR(100) NOT NULL,
                year INT NOT NULL,
                plate_number VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("[OK] Table 'vehicles' created/verified")
        
        # Create maintenance_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS maintenance_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT NOT NULL,
                maintenance_type VARCHAR(100) NOT NULL,
                description TEXT,
                cost DECIMAL(10, 2),
                maintenance_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
            )
        """)
        print("[OK] Table 'maintenance_logs' created/verified")
        
        # Check if table has any data
        cursor.execute("SELECT COUNT(*) FROM vehicles")
        count = cursor.fetchone()[0]
        print(f"[OK] Found {count} vehicle(s) in the database")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n[SUCCESS] Database setup complete! You can now use the app.")
        
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
        print("\nMake sure:")
        print("1. MySQL server is running")
        print("2. Your password in db_config.py is correct")
        print("3. You have permission to create databases")

if __name__ == "__main__":
    print("Setting up database...\n")
    setup_database()

