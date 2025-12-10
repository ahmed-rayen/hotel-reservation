import sqlite3
db_name = "hotel.db"
def get_connection():
    return sqlite3.connect(db_name)
def ajouter_reservation(id_client, num_chambre, date_debut, date_fin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO reservations (id_client, num_chambre, date_debut, date_fin) 
                      VALUES (?, ?, ?, ?)""",
                   (id_client, num_chambre, date_debut, date_fin))
    occupied = cursor.execute("SELECT statut FROM chambres WHERE num_chambre=?", (num_chambre,)).fetchone()
    if occupied and occupied[0] == 'occupée':
        print(" La chambre est déjà occupée.")
        conn.close()
        return
    else: 
        cursor.execute("UPDATE chambres SET statut='occupée' WHERE num_chambre=?", (num_chambre,))
        conn.commit()
        conn.close()
        print(" Réservation ajoutée !")
    
def modifier_reservation(id_res, id_client=None, num_chambre=None, date_debut=None, date_fin=None):
    conn = get_connection()
    cursor = conn.cursor()
    if id_client:
        cursor.execute("UPDATE reservations SET id_client=? WHERE id_res=?", (id_client, id_res))
    if num_chambre:
        cursor.execute("UPDATE reservations SET num_chambre=? WHERE id_res=?", (num_chambre, id_res))
    if date_debut:
        cursor.execute("UPDATE reservations SET date_debut=? WHERE id_res=?", (date_debut, id_res))
    if date_fin:
        cursor.execute("UPDATE reservations SET date_fin=? WHERE id_res=?", (date_fin, id_res))
    conn.commit()
    conn.close()
    print(" Réservation modifiée !")

def supprimer_reservation(id_res):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservations WHERE id_res=?", (id_res,))
    conn.commit()
    conn.close()
    print(" Réservation supprimée !")