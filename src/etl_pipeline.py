import sqlite3
import logging
import os

class ETLPipeline:
    def __init__(self):
        os.makedirs("data", exist_ok=True)  # Ensure data directory exists
        self.db_file = "data/oil_prices.db"
        self._init_db()
        self.logger = logging.getLogger(__name__)
        
    def _init_db(self):
        """Initialize database with schema migration support"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create table if not exists (original schema)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS oil_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                price REAL,
                is_anomaly INTEGER,
                analysis TEXT
            )
        """)
        
        # Check if source column exists
        cursor.execute("PRAGMA table_info(oil_prices)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'source' not in columns:
            try:
                cursor.execute("ALTER TABLE oil_prices ADD COLUMN source TEXT DEFAULT 'unknown'")
                self.logger.info("Added source column to database")
            except Exception as e:
                self.logger.error(f"Failed to add source column: {e}")
        
        conn.commit()
        conn.close()
        
    def store_data(self, price_data, is_anomaly=False, analysis=None):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Use the correct column count based on what's available
            cursor.execute("PRAGMA table_info(oil_prices)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'source' in columns:
                cursor.execute("""
                    INSERT INTO oil_prices 
                    (timestamp, price, is_anomaly, analysis, source)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    str(price_data['timestamp']),
                    price_data['price'],
                    int(is_anomaly),
                    analysis,
                    price_data.get('source', 'unknown')
                ))
            else:
                cursor.execute("""
                    INSERT INTO oil_prices 
                    (timestamp, price, is_anomaly, analysis)
                    VALUES (?, ?, ?, ?)
                """, (
                    str(price_data['timestamp']),
                    price_data['price'],
                    int(is_anomaly),
                    analysis
                ))
            
            conn.commit()
            self.logger.info("Data stored successfully")
        except Exception as e:
            self.logger.error(f"Error storing data: {e}")
        finally:
            conn.close()