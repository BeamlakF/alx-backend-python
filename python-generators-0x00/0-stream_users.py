import mysql.connector

def stream_users():
    """Generator function to stream rows from user_data one at a time"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password_here',  # Replace with your actual password
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()
