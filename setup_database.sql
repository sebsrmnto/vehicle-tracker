-- Vehicle Tracker Database Setup
-- Run this script to create the database and table

-- Create the database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS vehicle_tracker_db;

-- Use the database
USE vehicle_tracker_db;

-- Create the vehicles table
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    plate_number VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the maintenance_logs table
CREATE TABLE IF NOT EXISTS maintenance_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    maintenance_type VARCHAR(100) NOT NULL,
    description TEXT,
    cost DECIMAL(10, 2),
    maintenance_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);

-- Show the table structure (optional - to verify)
DESCRIBE vehicles;
DESCRIBE maintenance_logs;

-- Show message
SELECT 'Database and table created successfully!' AS message;

