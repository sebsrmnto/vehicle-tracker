import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

def get_db_connection():
    # Use environment variables if available (for production), otherwise use defaults (for local development)
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'Mibashishe87551_'),
        database=os.getenv('DB_NAME', 'vehicle_tracker_db')
    )
