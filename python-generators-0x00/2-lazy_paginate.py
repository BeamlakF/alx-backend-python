import seed  # Reuse connection utility from seed.py

def paginate_users(page_size, offset):
    """Fetch one page of users from the user_data table"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """Generator that lazily fetches pages of users one at a time"""
    offset = 0
    while True:  # ✅ Single loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
