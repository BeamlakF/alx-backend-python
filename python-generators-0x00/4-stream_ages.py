import seed  # Import DB connection functions from seed.py

def stream_user_ages():
    """Generator that yields user ages one at a time"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    
    for (age,) in cursor:  # Only 1 column returned, so unpack the tuple
        yield float(age)   # Convert to float to ensure decimal division

    cursor.close()
    connection.close()

def average_age():
    """Compute average age without loading all data into memory"""
    total = 0
    count = 0
    for age in stream_user_ages():  # ✅ First and only loop
        total += age
        count += 1

    if count > 0:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")
    else:
        print("No users found.")
