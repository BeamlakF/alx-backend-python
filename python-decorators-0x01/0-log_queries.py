import sqlite3
import functools
from datetime import datetime  # ✅ required import

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract the query
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            print(f"[{timestamp}] Executing SQL query: {query}")
        else:
            print(f"[{timestamp}] No SQL query provided.")
        
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
