# database.py
import sqlite3

def setup_clipboard():
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agency TEXT,
            topic TEXT,
            status TEXT,
            extracted_text TEXT,
            due_date TEXT,
            summary TEXT 
        )
    """)
    conn.commit()
    conn.close()