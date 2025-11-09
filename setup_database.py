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
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("[OK] Table 'users' created/verified")
        
        # Create vehicles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                brand VARCHAR(100) NOT NULL,
                model VARCHAR(100) NOT NULL,
                year INT NOT NULL,
                plate_number VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        print("[OK] Table 'vehicles' created/verified")
        
        # Check if user_id column exists, if not add it (for migration)
        cursor.execute("SHOW COLUMNS FROM vehicles LIKE 'user_id'")
        if not cursor.fetchone():
            print("[INFO] Adding user_id column to vehicles table...")
            # First, we need to handle existing data - set a default user or allow NULL temporarily
            # For safety, we'll allow NULL initially
            cursor.execute("ALTER TABLE vehicles ADD COLUMN user_id INT NULL")
            # Create a default user for existing data
            cursor.execute("SELECT id FROM users WHERE email = 'migrated@autotrack.local'")
            default_user = cursor.fetchone()
            if not default_user:
                cursor.execute("INSERT INTO users (email, password_hash) VALUES ('migrated@autotrack.local', 'migration_placeholder')")
                conn.commit()
                cursor.execute("SELECT id FROM users WHERE email = 'migrated@autotrack.local'")
                default_user_id = cursor.fetchone()[0]
            else:
                default_user_id = default_user[0]
            # Update existing vehicles with default user
            cursor.execute("UPDATE vehicles SET user_id = %s WHERE user_id IS NULL", (default_user_id,))
            # Now make it NOT NULL and add foreign key
            cursor.execute("ALTER TABLE vehicles MODIFY COLUMN user_id INT NOT NULL")
            cursor.execute("ALTER TABLE vehicles ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE")
            conn.commit()
            print("[OK] Migration: Added user_id to vehicles table")
        
        # Create maintenance_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS maintenance_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT NOT NULL,
                user_id INT NOT NULL,
                maintenance_type VARCHAR(100) NOT NULL,
                description TEXT,
                cost DECIMAL(10, 2),
                maintenance_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        print("[OK] Table 'maintenance_logs' created/verified")
        
        # Check if user_id column exists in maintenance_logs, if not add it (for migration)
        cursor.execute("SHOW COLUMNS FROM maintenance_logs LIKE 'user_id'")
        if not cursor.fetchone():
            print("[INFO] Adding user_id column to maintenance_logs table...")
            cursor.execute("ALTER TABLE maintenance_logs ADD COLUMN user_id INT NULL")
            # Get user_id from associated vehicle
            cursor.execute("""
                UPDATE maintenance_logs ml
                JOIN vehicles v ON ml.vehicle_id = v.id
                SET ml.user_id = v.user_id
                WHERE ml.user_id IS NULL
            """)
            # Now make it NOT NULL and add foreign key
            cursor.execute("ALTER TABLE maintenance_logs MODIFY COLUMN user_id INT NOT NULL")
            cursor.execute("ALTER TABLE maintenance_logs ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE")
            conn.commit()
            print("[OK] Migration: Added user_id to maintenance_logs table")
        
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

