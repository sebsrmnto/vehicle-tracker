import mysql.connector
import os
import time
import logging
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

def get_db_connection(max_retries=3, retry_delay=1):
    """
    Get database connection with retry logic.
    
    Args:
        max_retries: Maximum number of connection attempts
        retry_delay: Delay between retries in seconds
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
    
    Raises:
        mysql.connector.Error: If connection fails after all retries
    """
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', 'Mibashishe87551_')
    database = os.getenv('DB_NAME', 'vehicle_tracker_db')
    port = os.getenv('DB_PORT', '3306')
    
    # Convert port to int if it's a string
    try:
        port = int(port)
    except (ValueError, TypeError):
        port = 3306
    
    last_error = None
    
    for attempt in range(1, max_retries + 1):
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                autocommit=False,  # Explicit transaction management
                connect_timeout=10,  # Connection timeout in seconds
                use_unicode=True,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            
            # Test the connection
            if connection.is_connected():
                logger.info(f"Successfully connected to database (attempt {attempt}/{max_retries})")
                return connection
                
        except mysql.connector.Error as e:
            last_error = e
            error_msg = str(e)
            logger.warning(f"Database connection attempt {attempt}/{max_retries} failed: {error_msg}")
            
            if attempt < max_retries:
                time.sleep(retry_delay * attempt)  # Exponential backoff
            else:
                logger.error(f"Failed to connect to database after {max_retries} attempts: {error_msg}")
                
        except Exception as e:
            last_error = e
            error_msg = str(e)
            logger.error(f"Unexpected error during database connection (attempt {attempt}/{max_retries}): {error_msg}")
            
            if attempt < max_retries:
                time.sleep(retry_delay * attempt)
    
    # If we get here, all retries failed
    if last_error:
        raise last_error
    else:
        raise ConnectionError(f"Unable to connect to database after {max_retries} attempts")
