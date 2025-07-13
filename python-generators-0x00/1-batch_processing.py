import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields users in batches of given size.
    Efficient for large datasets – avoids loading everything into memory.
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password_here',  # 🔒 Replace with your actual MySQL password
        database='ALX_prodev'
    )
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    
    batch = []
    for row in cursor:  # Looping through the result set one row at a time
        batch.append(row)
        if len(batch) == batch_size:
            yield batch  # 🔁 Yield batch to caller
            batch = []   # Reset batch for the next group
    
    if batch:
        yield batch  # Yield remaining users if any
    
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Process each batch from the generator and print users where age > 25.
    """
    for batch in stream_users_in_batches(batch_size):     # 🔁 Loop 1: over batches
        for user in batch:                                # 🔁 Loop 2: over users in batch
            if float(user['age']) > 25:                   # ✅ Filter condition
                print(user)
