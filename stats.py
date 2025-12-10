import sqlite3
db_name="hotel.db"
def get_connection():
    return sqlite3.connect(db_name)
def afficher_nb_chambre():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM chambres")
    result=cursor.fetchall()
    conn.commit()
    conn.close()
    return result