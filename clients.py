import sqlite3
db_name = "hotel.db"
def get_connection():
    return sqlite3.connect(db_name)

def ajouter_client(nom, prenom, telephone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO clients (nom, prenom, telephone) VALUES (?, ?, ?)""",
                   (nom, prenom, telephone))
    conn.commit()
    conn.close()
    print(" Client ajouté !")

def modifier_client(id_client, nom=None, prenom=None, telephone=None):
    conn = get_connection()
    cursor = conn.cursor()
    if nom:
        cursor.execute("UPDATE clients SET nom=? WHERE id_client=?", (nom, id_client))
    if prenom:
        cursor.execute("UPDATE clients SET prenom=? WHERE id_client=?", (prenom, id_client))
    if telephone:
        cursor.execute("UPDATE clients SET telephone=? WHERE id_client=?", (telephone, id_client))
    conn.commit()
    conn.close()
    print(" Client modifié !")
    
def supprimer_client(id_client):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM CLIENTS WHERE ID_CLIENT=?", (id_client,))
    conn.commit()
    conn.close()
    print(" Client supprimé !")
    
def chercher_client(id_clients):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM CLIENTS WHERE ID_CLIENT=?", (id_clients,))
    result=cursor.fetchone()
    if result:
        print(" Client trouvé :", result)
        return result 
    else:
        print(" Client non trouvé.")
        return None
    conn.close()
   
