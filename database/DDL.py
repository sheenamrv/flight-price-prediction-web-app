# this script to create the database and tables for the project

import mysql.connector
import os 

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Database configuration
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = 'localhost'
DB_NAME = 'flights'

# Connect to MySQL server (without specifying database — it may not exist yet)
try:
    cnx = mysql.connector.connect(user=DB_USER,
                                  password=DB_PASSWORD,
                                  host=DB_HOST)
    cursor = cnx.cursor()
    print("Connected to MySQL server successfully.")

except mysql.connector.Error as err:
    print('Error connecting to MySQL server:', err)
    exit(1)


# Create database
try:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"Database '{DB_NAME}' created or already exists.")

except mysql.connector.Error as err:
    print(f"Error creating database '{DB_NAME}':", err)
    cursor.close()
    cnx.close()
    exit(1)

# Switch to the target database
cursor.execute(f"USE {DB_NAME}")

# create tables

sql = """
CREATE TABLE IF NOT EXISTS flight_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    origin VARCHAR(20),
    destination VARCHAR(20),
    departure_date DATE,
    predicted_price DECIMAL(10, 2),
    average_price DECIMAL(10, 2)
)
"""
try:
    cursor.execute(sql)
    print("Table 'flight_data' created or already exists.")
except mysql.connector.Error as err:
    print(f"Error creating table 'flight_data':", err)

# Close the connection
cursor.close()
cnx.close()
