import sqlite3
from datetime import datetime

DB_NAME = "hotel.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

# ================= ADD =================
def ajouter_reservation(id_client, num_chambre, date_debut, date_fin):
    if date_fin < date_debut:
        return False, "Date fin invalide"

    conn = get_connection()
    cursor = conn.cursor()

    # Check client
    if not cursor.execute(
        "SELECT 1 FROM clients WHERE id_client=?", (id_client,)
    ).fetchone():
        conn.close()
        return False, "Client inexistant"

    # Check room
    room = cursor.execute(
        "SELECT statut FROM chambres WHERE num_chambre=?", (num_chambre,)
    ).fetchone()

    if not room:
        conn.close()
        return False, "Chambre inexistante"

    if room[0] == "occupée":
        conn.close()
        return False, "Chambre déjà occupée"

    cursor.execute("""
        INSERT INTO reservations (id_client, num_chambre, date_debut, date_fin)
        VALUES (?, ?, ?, ?)
    """, (id_client, num_chambre, date_debut, date_fin))

    cursor.execute(
        "UPDATE chambres SET statut='occupée' WHERE num_chambre=?",
        (num_chambre,)
    )

    conn.commit()
    conn.close()
    return True, "Réservation ajoutée"


# ================= LIST =================
def afficher_reservations():
    conn = get_connection()
    cursor = conn.cursor()
    data = cursor.execute("""
        SELECT id_res, id_client, num_chambre, date_debut, date_fin
        FROM reservations
        ORDER BY date_debut
    """).fetchall()
    conn.close()
    return data


# ================= UPDATE =================
def modifier_reservation(id_res, id_client=None, num_chambre=None, date_debut=None, date_fin=None):
    conn = get_connection()
    cursor = conn.cursor()

    old_room = cursor.execute(
        "SELECT num_chambre FROM reservations WHERE id_res=?", (id_res,)
    ).fetchone()

    if not old_room:
        conn.close()
        return False

    if num_chambre is not None and num_chambre != old_room[0]:
        status = cursor.execute(
            "SELECT statut FROM chambres WHERE num_chambre=?", (num_chambre,)
        ).fetchone()

        if not status or status[0] == "occupée":
            conn.close()
            return False

        cursor.execute(
            "UPDATE chambres SET statut='libre' WHERE num_chambre=?",
            (old_room[0],)
        )
        cursor.execute(
            "UPDATE chambres SET statut='occupée' WHERE num_chambre=?",
            (num_chambre,)
        )

        cursor.execute(
            "UPDATE reservations SET num_chambre=? WHERE id_res=?",
            (num_chambre, id_res)
        )

    if id_client is not None:
        cursor.execute(
            "UPDATE reservations SET id_client=? WHERE id_res=?",
            (id_client, id_res)
        )
    if date_debut is not None:
        cursor.execute(
            "UPDATE reservations SET date_debut=? WHERE id_res=?",
            (date_debut, id_res)
        )
    if date_fin is not None:
        cursor.execute(
            "UPDATE reservations SET date_fin=? WHERE id_res=?",
            (date_fin, id_res)
        )

    conn.commit()
    conn.close()
    return True


# ================= DELETE =================
def supprimer_reservation(id_res):
    conn = get_connection()
    cursor = conn.cursor()

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
