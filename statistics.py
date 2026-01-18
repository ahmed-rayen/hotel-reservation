import sqlite3

DB_NAME = "hotel.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def total_chambres():
    conn = get_connection()
    cur = conn.cursor()
    total = cur.execute("SELECT COUNT(*) FROM chambres").fetchone()[0]
    conn.close()
    return total

def chambres_libres():
    conn = get_connection()
    cur = conn.cursor()
    libres = cur.execute(
        "SELECT COUNT(*) FROM chambres WHERE statut='libre'"
    ).fetchone()[0]
    conn.close()
    return libres

def chambres_occupees():
    conn = get_connection()
    cur = conn.cursor()
    occ = cur.execute(
        "SELECT COUNT(*) FROM chambres WHERE statut='occupée'"
    ).fetchone()[0]
    conn.close()
    return occ

def taux_occupation():
    total = total_chambres()
    if total == 0:
        return 0
    occ = chambres_occupees()
    return round((occ / total) * 100, 2)
