# init_db.py
import sqlite3
from datetime import datetime, timedelta
import random

def init_database():
    conn = sqlite3.connect('data/oil_prices.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS oil_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        price REAL,
        is_anomaly BOOLEAN DEFAULT 0,
        analysis TEXT
    )
    """)
    
    # Add sample data (optional)
    for i in range(10):
        cursor.execute("""
        INSERT INTO oil_prices (timestamp, price)
        VALUES (?, ?)
        """, (
            datetime.now() - timedelta(hours=i),
            70 + random.random() * 5  # Random price between 70-75
        ))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

if __name__ == "__main__":
    init_database()