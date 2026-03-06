"""
Hotel Mediterranee - Script d'initialisation de la base de donnees SQLite
Cree la base de donnees avec la structure correcte
"""
import sqlite3

DB_FILE = "hotel_mediterranee.db"

def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Creer les tables
    print("Creation des tables...")
    
    # Table ailes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ailes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)
    
    # Table chambres - avec la colonne 'numero' comme specifie
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chambres (
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
        CREATE TABLE IF NOT EXISTS demandes_maintenance (
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
        CREATE TABLE IF NOT EXISTS utilisateurs (
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
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT (datetime('now')),
            action TEXT NOT NULL,
            details TEXT,
            status TEXT DEFAULT 'info'
        )
    """)
    
    # Inserer les ailes
    print("Insertion des ailes...")
    cursor.execute("INSERT OR IGNORE INTO ailes (nom, description) VALUES ('A', 'Aile Appartements')")
    cursor.execute("INSERT OR IGNORE INTO ailes (nom, description) VALUES ('B', 'Aile Chambres')")
    
    # Inserer les chambres - Aile B (id=2)
    print("Insertion des chambres Aile B...")
    cursor.execute("INSERT OR IGNORE INTO chambres (numero, type, aile_id, statut, description) VALUES ('A1', 'appartement', 2, 'disponible', 'Appartement Luxe Aile B')")
    cursor.execute("INSERT OR IGNORE INTO chambres (numero, type, aile_id, statut, description) VALUES ('A2', 'appartement', 2, 'disponible', 'Appartement Standard Aile B')")
    
    # Chambres 1001-1067
    for i in range(1, 68):
        num = f"100{i:02d}" if i < 10 else f"10{i:02d}"
        cursor.execute(f"INSERT OR IGNORE INTO chambres (numero, type, aile_id, statut) VALUES ('{num}', 'chambre', 2, 'disponible')")
    
    # Chambres 2001-2044
    for i in range(1, 45):
        num = f"200{i:03d}"
        cursor.execute(f"INSERT OR IGNORE INTO chambres (numero, type, aile_id, statut) VALUES ('{num}', 'chambre', 2, 'disponible')")
    
    # Chambres 3002-3065
    for i in range(2, 66):
        num = f"30{i:02d}"
        cursor.execute(f"INSERT OR IGNORE INTO chambres (numero, type, aile_id, statut) VALUES ('{num}', 'chambre', 2, 'disponible')")
    
    # Inserer les chambres - Aile A (id=1)
    print("Insertion des chambres Aile A...")
    cursor.execute("INSERT OR IGNORE INTO chambres (numero, type, aile_id, statut, description) VALUES ('A3', 'appartement', 1, 'occupée', 'Appartement Familial Aile A')")
    cursor.execute("INSERT OR IGNORE INTO chambres (numero, type, aile_id, statut, description) VALUES ('A4', 'appartement', 1, 'disponible', 'Appartement Deluxe Aile A')")
    
    # Inserer les utilisateurs
    print("Insertion des utilisateurs...")
    cursor.execute("INSERT OR IGNORE INTO utilisateurs (nom, rôle, username, mot_de_passe) VALUES ('Admin', 'admin', 'admin', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO utilisateurs (nom, rôle, username, mot_de_passe) VALUES ('Chef Maintenance', 'chef_maintenance', 'chef', 'chef123')")
    cursor.execute("INSERT OR IGNORE INTO utilisateurs (nom, rôle, username, mot_de_passe) VALUES ('Receptionniste', 'réceptionniste', 'reception', 'reception123')")
    
    conn.commit()
    
    # Verifier les donnees
    cursor.execute("SELECT COUNT(*) FROM chambres")
    print(f"Nombre de chambres: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM ailes")
    print(f"Nombre d' ailes: {cursor.fetchone()[0]}")
    
    conn.close()
    print("\n✅ Base de donnees initialisee avec succes!")

if __name__ == "__main__":
    init_database()
