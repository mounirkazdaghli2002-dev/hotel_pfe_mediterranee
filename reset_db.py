"""
Script pour reinitialiser la base de donnees
"""
import sqlite3
import os

DB_FILE = "hotel_mediterranee.db"

# Supprimer l'ancienne base
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("Ancienne base supprimee")

# Creer la nouvelle base
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Table ailes
cursor.execute("""
    CREATE TABLE ailes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE,
        description TEXT
    )
""")

# Table chambres
cursor.execute("""
    CREATE TABLE chambres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL CHECK(type IN ('chambre', 'appartement')),
        aile_id INTEGER,
        statut TEXT DEFAULT 'disponible' CHECK(statut IN ('disponible', 'occupée', 'maintenance', 'nettoyage')),
        description TEXT,
        derniere_sync TEXT,
        FOREIGN KEY (aile_id) REFERENCES ailes(id)
    )
""")

# Table demandes_maintenance
cursor.execute("""
    CREATE TABLE demandes_maintenance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chambre_id INTEGER NOT NULL,
        type_probleme TEXT NOT NULL,
        description TEXT,
        priorite TEXT DEFAULT 'moyenne' CHECK(priorite IN ('basse', 'moyenne', 'haute', 'urgente')),
        date_signalement TEXT DEFAULT (datetime('now')),
        date_resolution TEXT,
        resolu INTEGER DEFAULT 0,
        agent_assigné TEXT,
        FOREIGN KEY (chambre_id) REFERENCES chambres(id)
    )
""")

# Table utilisateurs
cursor.execute("""
    CREATE TABLE utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        rôle TEXT NOT NULL,
        username TEXT UNIQUE,
        mot_de_passe TEXT,
        actif INTEGER DEFAULT 1
    )
""")

# Table logs
cursor.execute("""
    CREATE TABLE logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT DEFAULT (datetime('now')),
        action TEXT NOT NULL,
        details TEXT,
        status TEXT DEFAULT 'info'
    )
""")

# Inserer les ailes
cursor.execute("INSERT INTO ailes (nom, description) VALUES ('A', 'Aile Appartements')")
cursor.execute("INSERT INTO ailes (nom, description) VALUES ('B', 'Aile Chambres')")

# Appartements Aile B (id=2)
cursor.execute("INSERT INTO chambres (numero, type, aile_id, statut, description) VALUES ('A1', 'appartement', 2, 'disponible', 'Appartement Luxe Aile B')")
cursor.execute("INSERT INTO chambres (numero, type, aile_id, statut, description) VALUES ('A2', 'appartement', 2, 'disponible', 'Appartement Standard Aile B')")

# Chambres Aile B: 1001-1067
for i in range(1, 68):
    num = f"100{i:02d}"
    cursor.execute(f"INSERT INTO chambres (numero, type, aile_id, statut) VALUES ('{num}', 'chambre', 2, 'disponible')")

# Chambres Aile B: 2001-2044
for i in range(1, 45):
    num = f"200{i:03d}"
    cursor.execute(f"INSERT INTO chambres (numero, type, aile_id, statut) VALUES ('{num}', 'chambre', 2, 'disponible')")

# Chambres Aile B: 3002-3065
for i in range(2, 66):
    num = f"30{i:02d}"
    cursor.execute(f"INSERT INTO chambres (numero, type, aile_id, statut) VALUES ('{num}', 'chambre', 2, 'disponible')")

# Appartements Aile A (id=1)
cursor.execute("INSERT INTO chambres (numero, type, aile_id, statut, description) VALUES ('A3', 'appartement', 1, 'occupée', 'Appartement Familial Aile A')")
cursor.execute("INSERT INTO chambres (numero, type, aile_id, statut, description) VALUES ('A4', 'appartement', 1, 'disponible', 'Appartement Deluxe Aile A')")

# Utilisateurs
cursor.execute("INSERT INTO utilisateurs (nom, rôle, username, mot_de_passe) VALUES ('Admin', 'admin', 'admin', 'admin123')")
cursor.execute("INSERT INTO utilisateurs (nom, rôle, username, mot_de_passe) VALUES ('Chef Maintenance', 'chef_maintenance', 'chef', 'chef123')")
cursor.execute("INSERT INTO utilisateurs (nom, rôle, username, mot_de_passe) VALUES ('Receptionniste', 'réceptionniste', 'reception', 'reception123')")

conn.commit()

# Verifier
cursor.execute("SELECT COUNT(*) FROM chambres")
print(f"Chambres: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM ailes")
print(f"Ailes: {cursor.fetchone()[0]}")

conn.close()
print("Base recreee avec succes!")
