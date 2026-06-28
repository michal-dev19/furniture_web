import sqlite3
from fastapi import HTTPException


# accessing database
def get_db():

    conn = sqlite3.connect("furniture.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    yield conn, cursor
    conn.close()


# initialise database
def init_db():

    conn = sqlite3.connect("furniture.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS categories
            (id INTEGER PRIMARY KEY,
            type TEXT)"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS items 
            (id INTEGER PRIMARY KEY, 
            category_id INT,
            item_name TEXT, 
            description TEXT, 
            colour TEXT, 
            price INT, 
            created_at INT,
            FOREIGN KEY (category_id) REFERENCES categories(id))"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS enquiries
            (id INTEGER PRIMARY KEY,
            item_id INT,
            customer_name TEXT,
            customer_email TEXT,
            customer_phone TEXT,
            status TEXT,
            created_at INT,
            order_id INT,
            item_cost INT,
            shipping_cost INT,
            miscellaneous_cost INT,
            FOREIGN KEY (item_id) REFERENCES items(id))"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS photos
            (id INTEGER PRIMARY KEY,
            item_id INT,
            file_path TEXT,
            photo_order INT,
            FOREIGN KEY (item_id) REFERENCES items(id))"""
        )
        conn.commit()
        conn.close()
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal Server Error")
