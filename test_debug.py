import pandas as pd
import os

MAINTENANCE_FILE = "maintenance_tasks.csv"

# Load the file
tasks = pd.read_csv(MAINTENANCE_FILE)
print("=== COLUMNS ===")
print(tasks.columns.tolist())
print("\n=== DTYPES ===")
print(tasks.dtypes)
print("\n=== DATA ===")
print(tasks)
print("\n=== CHAMBRE 1001 (string) ===")
room_tasks = tasks[tasks["chambre"] == "1001"]
print(room_tasks)
print(f"\n=== COUNT: {len(room_tasks)} ===")

print("\n=== CHAMBRE 1001 (int) ===")
room_tasks2 = tasks[tasks["chambre"] == 1001]
print(room_tasks2)
print(f"\n=== COUNT: {len(room_tasks2)} ===")

