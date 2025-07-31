import sqlite3

# Connect to your database
conn = sqlite3.connect("data/oil_prices.db")
cursor = conn.cursor()

# Run your query
cursor.execute("SELECT * FROM oil_prices ORDER BY timestamp DESC LIMIT 1")
row = cursor.fetchone()

# Print the result
print(row)

conn.close()
