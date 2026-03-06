import sqlite3
conn = sqlite3.connect('hotel_mediterranee.db')
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
