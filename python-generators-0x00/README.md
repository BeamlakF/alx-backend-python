
# 📦 seed.py – MySQL Seeder and Row Generator

This script automates the setup of a MySQL database called **`ALX_prodev`**, creates a table named **`user_data`**, populates it with data from a CSV file, and provides a **Python generator** to stream rows one-by-one from the database.

---

## 📋 Features

- Connects to MySQL server
- Creates a database `ALX_prodev` if it doesn't exist
- Creates a table `user_data` with the following fields:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Inserts data from `user_data.csv` only if not already present (no duplicates by email)
- Streams rows from the `user_data` table using a Python generator

---

## 📁 File Structure

```

.
├── seed.py
├── 0-main.py
├── user\_data.csv
├── README.md

````

---

## ⚙️ Setup Instructions

1. **Update Credentials**  
   Open `seed.py` and replace:
   ```python
   password='your_password_here'
````

with your actual MySQL root password.

2. **Ensure CSV File Exists**
   Place `user_data.csv` in the project root with columns: `name,email,age`.

3. **Run Seeder Script**

   ```bash
   ./0-main.py
   ```

   Output should include:

   ```
   connection successful
   Table user_data created successfully
   Database ALX_prodev is present 
   [...first 5 rows printed...]
   ```

---

## 🔁 Generator Usage

To stream rows one by one from the `user_data` table:

```python
for user in seed.stream_users(connection):
    print(user)
```

Useful for processing large datasets without loading everything into memory at once.

---

## 📌 Function Prototypes

```python
def connect_db()
def create_database(connection)
def connect_to_prodev()
def create_table(connection)
def insert_data(connection, data)
def stream_users(connection)
```

---

## 🧪 Example Test File: `0-main.py`

```python
#!/usr/bin/python3
seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()

    connection = seed.connect_to_prodev()
    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        for row in seed.stream_users(connection):
            print(row)
```

---

## 🧰 Dependencies

* `mysql-connector-python`

Install via pip:

```bash
pip install mysql-connector-python
```

---


