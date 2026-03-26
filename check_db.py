import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
DB_PATH = os.getenv('DB_PATH', 'hotel_mediterranee.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check chambres table
cursor.execute("PRAGMA table_info(chambres)")
print("=== CHAMBRES ===")
for row in cursor.fetchall():
    print(row)

# Check demandes_maintenance table
cursor.execute("PRAGMA table_info(demandes_maintenance)")
print("\n=== DEMANDES_MAINTENANCE ===")
for row in cursor.fetchall():
    print(row)

conn.close()
</parameter>
</create_file>
