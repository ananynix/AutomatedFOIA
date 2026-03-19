# database.py
import sqlite3

def setup_clipboard():
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    
    # Existing Requests Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agency TEXT,
            topic TEXT,
            status TEXT,
            extracted_text TEXT,
            due_date TEXT,
            summary TEXT,
            filepath TEXT 
        )
    """)
    
    # NEW: Secure Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)
    
    # Inject default secure accounts (For portfolio demonstration)
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('investigator_1', 'cipher123', 'investigator')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('nsa_agent_alpha', 'redact456', 'government')")
    
    conn.commit()
    conn.close()