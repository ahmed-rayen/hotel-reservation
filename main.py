from hotel_db import *
from chambres import *
from clients import *
from reservation import *

create_database()

ajouter_chambre(1, "simple", 80.0)
ajouter_chambre(2, "double", 120.0)

modifier_chambre(1, statut="occupée")

print("Chambres libres :", afficher_chambres_libres())
print("Chambres occupées :", afficher_chambres_occupees())

supprimer_chambre(2)
supprimer_chambre(1)

ajouter_client("ahmed","barkallah","14524587")
supprimer_client(4)
chercher_client(5)