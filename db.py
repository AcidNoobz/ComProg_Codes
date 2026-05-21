import sqlite3

# connect database
conn = sqlite3.connect("sales.db")

cursor = conn.cursor()

# create table
def setup_database():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        total REAL NOT NULL,
        date TEXT NOT NULL
    )
    """)

    conn.commit()