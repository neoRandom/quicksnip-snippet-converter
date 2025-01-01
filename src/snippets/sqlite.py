# =============================================================
# Create SQLite Database Table

import sqlite3

def create_table(db_name, table_name, schema):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    schema_string = ', '.join([f'{col} {dtype}' for col, dtype in schema.items()])
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {schema_string}
        )''')
    conn.commit()
    conn.close()

# Usage:
db_name = 'example.db'
table_name = 'users'
schema = {
    'id': 'INTEGER PRIMARY KEY',
    'name': 'TEXT',
    'age': 'INTEGER',
    'email': 'TEXT'
}
create_table(db_name, table_name, schema)

# =============================================================
# Insert Data into Sqlite Table

import sqlite3

def insert_into_table(db_path, table_name, data):
    with sqlite3.connect(db_path) as conn:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        conn.execute(sql, tuple(data.values()))
        conn.commit()

# Usage:
db_path = 'example.db'
table_name = 'users'
data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
}
insert_into_table(db_path, table_name, data)

# =============================================================
# Query Data from the SQLite Table

import sqlite3

def query_table(db_path, table_name, columns=["*"], condition=None):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        sql = f"SELECT {', '.join(columns)} FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        cursor.execute(sql)
        return cursor.fetchall()

# Usage:
db_path = 'example.db'
table_name = 'users'
columns = ['id', 'name', 'email']  # Specify columns or leave blank for all
condition = "age > 25"  # Optional, leave as None to fetch all rows
result = query_table(db_path, table_name, columns, condition)
for row in result:
    print(row)

# =============================================================
# Update Data from the SQLite Table

import sqlite3

def update_table(db_path, table_name, updates, condition):
    with sqlite3.connect(db_path) as conn:
        set_clause = ', '.join([f"{col} = ?" for col in updates.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        conn.execute(sql, tuple(updates.values()))
        conn.commit()

# Usage:
db_path = 'example.db'
table_name = 'users'
updates = {
    'name': 'Jane Doe',
    'age': 32
}
condition = "email = 'john@example.com'"
update_table(db_path, table_name, updates, condition)

# =============================================================
# Delete Data from the SQLite Table

import sqlite3

def delete_from_table(db_path, table_name, condition):
    with sqlite3.connect(db_path) as conn:
        sql = f"DELETE FROM {table_name} WHERE {condition}"
        conn.execute(sql)
        conn.commit()

# Usage:
db_path = 'example.db'
table_name = 'users'
condition = "age < 20"  # Delete rows where age is less than 20
delete_from_table(db_path, table_name, condition)

# =============================================================
# Bulk Insert

import sqlite3

def bulk_insert(db_path, table_name, data_list):
    """
    Bulk inserts multiple rows of data into the table.
    
    Parameters:
    - db_path: Path to the SQLite database.
    - table_name: Name of the table.
    - data_list: A list of dictionaries where each dictionary represents a row of data.
    """
    if not data_list:
        return  # If no data is provided, exit function

    with sqlite3.connect(db_path) as conn:
        # Extract column names from the first dictionary
        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['?'] * len(data_list[0]))

        # Prepare the SQL statement
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Execute the bulk insert
        values = [tuple(row.values()) for row in data_list]
        conn.executemany(sql, values)
        conn.commit()

# Usage:
db_path = 'example.db'
table_name = 'users'
data_list = [
    {'name': 'Alice', 'email': 'alice@example.com', 'age': 25},
    {'name': 'Bob', 'email': 'bob@example.com', 'age': 28},
    {'name': 'Charlie', 'email': 'charlie@example.com', 'age': 22}
]
bulk_insert(db_path, table_name, data_list)

# =============================================================
# Fetch One Record

import sqlite3

def fetch_one(db_path, table_name, columns="*", condition=None):
    """
    Fetches a single record from the table.

    Parameters:
    - db_path: Path to the SQLite database.
    - table_name: Name of the table.
    - columns: Columns to select (default is all "*").
    - condition: SQL condition to filter the record (default is None).
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        sql = f"SELECT {columns} FROM {table_name}"
        if condition:
            sql += f" WHERE {condition} LIMIT 1"  # Limit to one record
        cursor.execute(sql)
        return cursor.fetchone()  # Fetch a single row

# Usage:
db_path = 'example.db'
table_name = 'users'
columns = 'name, age'
condition = "email = 'alice@example.com'"
record = fetch_one(db_path, table_name, columns, condition)
print(record)

# =============================================================
# Check if a Record Exists

import sqlite3

def record_exists(db_path, table_name, condition):
    """
    Checks if a record exists in the table based on a condition.

    Parameters:
    - db_path: Path to the SQLite database.
    - table_name: Name of the table.
    - condition: SQL condition to check.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        sql = f"SELECT 1 FROM {table_name} WHERE {condition} LIMIT 1"
        cursor.execute(sql)
        return cursor.fetchone() is not None  # Returns True if a record exists

# Usage:
db_path = 'example.db'
table_name = 'users'
condition = "email = 'alice@example.com'"
exists = record_exists(db_path, table_name, condition)
print(f"Record exists: {exists}")

# =============================================================
# Get Table Schema

import sqlite3

def get_table_schema(db_path, table_name):
    """
    Retrieves the schema (column names and types) of a table.

    Parameters:
    - db_path: Path to the SQLite database.
    - table_name: Name of the table.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        sql = f"PRAGMA table_info({table_name})"
        cursor.execute(sql)
        return cursor.fetchall()  # Returns a list of tuples: (cid, name, type, notnull, default_value, pk)

# Usage:
db_path = 'example.db'
table_name = 'users'
schema = get_table_schema(db_path, table_name)
for column in schema:
    print(column)  # Each column contains detailed info

# =============================================================
# Delete All Data from a Table

import sqlite3

def clear_table(db_path, table_name):
    """
    Deletes all rows from a table without dropping the table.

    Parameters:
    - db_path: Path to the SQLite database.
    - table_name: Name of the table.
    """
    with sqlite3.connect(db_path) as conn:
        sql = f"DELETE FROM {table_name}"
        conn.execute(sql)
        conn.commit()

# Usage:
db_path = 'example.db'
table_name = 'users'
clear_table(db_path, table_name)

