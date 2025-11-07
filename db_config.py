import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mibashishe87551_",  # change this!
        database="vehicle_tracker_db"
    )
