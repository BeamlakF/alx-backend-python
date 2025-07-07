import mysql.connector
import csv
import uuid

def connect_db():
    """Connect to MySQL server (no database selected yet)"""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here'  # Replace with your actual MySQL password
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here',  # Replace with your actual MySQL password
            database='ALX_prodev'
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Create user_data table"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5, 2) NOT NULL,
                INDEX(user_id)
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def insert_data(connection, csv_file):
    """Insert CSV data into user_data table if not exists"""
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    SELECT COUNT(*) FROM user_data WHERE email = %s
                """, (row['email'],))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        str(uuid.uuid4()),
                        row['name'],
                        row['email'],
                        row['age']
                    ))
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Insert error: {e}")

def stream_users(connection):
    """Generator: Stream users row by row"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()
