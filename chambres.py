import sqlite3

def ajouter_chambre(num_chambre, type_chambre, prix_nuit, statut="libre"):
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO chambres VALUES (?, ?, ?, ?)""",
                   (num_chambre, type_chambre, prix_nuit, statut))

    conn.commit()
    conn.close()
    print(" Chambre ajoutée !")


def modifier_chambre(num_chambre, type_chambre=None, prix_nuit=None, statut=None):
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    if type_chambre:
        cursor.execute("UPDATE chambres SET type=? WHERE num_chambre=?", (type_chambre, num_chambre))
    if prix_nuit:
        cursor.execute("UPDATE chambres SET prix_nuit=? WHERE num_chambre=?", (prix_nuit, num_chambre))
    if statut:
        cursor.execute("UPDATE chambres SET statut=? WHERE num_chambre=?", (statut, num_chambre))

    conn.commit()
    conn.close()
    print(" Chambre modifiée !")


def supprimer_chambre(num_chambre):
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chambres WHERE num_chambre=?", (num_chambre,))
    conn.commit()
    conn.close()
    print(" Chambre supprimée !")


def afficher_chambres_libres():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chambres WHERE statut='libre'")
    result = cursor.fetchall()
    conn.close()
    return result


def afficher_chambres_occupees():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chambres WHERE statut='occupée'")
    result = cursor.fetchall()
    conn.close()
    return result
