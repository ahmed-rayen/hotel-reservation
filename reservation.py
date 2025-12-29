import sqlite3

db_name = "hotel.db"

def get_connection():
    return sqlite3.connect(db_name)

# ================= ADD =================
def ajouter_reservation(id_client, num_chambre, date_debut, date_fin):
    conn = get_connection()
    cursor = conn.cursor()

    # Check room status FIRST
    statut = cursor.execute(
        "SELECT statut FROM chambres WHERE num_chambre=?",
        (num_chambre,)
    ).fetchone()

    if not statut:
        conn.close()
        return False, "Chambre inexistante"

    if statut[0] == "occupée":
        conn.close()
        return False, "Chambre déjà occupée"

    # Insert reservation
    cursor.execute("""
        INSERT INTO reservations (id_client, num_chambre, date_debut, date_fin)
        VALUES (?, ?, ?, ?)
    """, (id_client, num_chambre, date_debut, date_fin))

    # Update room status
    cursor.execute(
        "UPDATE chambres SET statut='occupée' WHERE num_chambre=?",
        (num_chambre,)
    )

    conn.commit()
    conn.close()
    return True, "Réservation ajoutée"

# ================= UPDATE =================
def modifier_reservation(id_res, id_client=None, num_chambre=None, date_debut=None, date_fin=None):
    conn = get_connection()
    cursor = conn.cursor()

    if id_client is not None:
        cursor.execute("UPDATE reservations SET id_client=? WHERE id_res=?", (id_client, id_res))
    if num_chambre is not None:
        cursor.execute("UPDATE reservations SET num_chambre=? WHERE id_res=?", (num_chambre, id_res))
    if date_debut is not None:
        cursor.execute("UPDATE reservations SET date_debut=? WHERE id_res=?", (date_debut, id_res))
    if date_fin is not None:
        cursor.execute("UPDATE reservations SET date_fin=? WHERE id_res=?", (date_fin, id_res))

    conn.commit()
    conn.close()

# ================= DELETE =================
def supprimer_reservation(id_res):
    conn = get_connection()
    cursor = conn.cursor()

    # Free the room
    room = cursor.execute(
        "SELECT num_chambre FROM reservations WHERE id_res=?",
        (id_res,)
    ).fetchone()

    if room:
        cursor.execute(
            "UPDATE chambres SET statut='libre' WHERE num_chambre=?",
            (room[0],)
        )

    cursor.execute("DELETE FROM reservations WHERE id_res=?", (id_res,))
    conn.commit()
    conn.close()
