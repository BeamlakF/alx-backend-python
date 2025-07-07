import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields users in batches of given size"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password_here',  # Replace with your actual password
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    
    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []
    
    if batch:
        yield batch  # yield any remaining users
    
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Process each batch and print users with age > 25"""
    for batch in stream_users_in_batches(batch_size):     # Loop 1
        for user in batch:                                # Loop 2
            if float(user['age']) > 25:                   # No loop here
                print(user)
