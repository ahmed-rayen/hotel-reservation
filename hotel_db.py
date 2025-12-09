import sqlite3

def create_database():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chambres (
        num_chambre INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        prix_nuit REAL NOT NULL,
        statut TEXT NOT NULL CHECK(statut IN ('libre', 'occupée'))
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id_client INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        telephone TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id_res INTEGER PRIMARY KEY AUTOINCREMENT,
        id_client INTEGER,
        num_chambre INTEGER,
        date_debut TEXT,
        date_fin TEXT,
        FOREIGN KEY(id_client) REFERENCES clients(id_client),
        FOREIGN KEY(num_chambre) REFERENCES chambres(num_chambre)
    )
    """)

    conn.commit()
    conn.close()
