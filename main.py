"""
Programme principal de detection de drones
Ce programme analyse les signaux radio pour detecter des drones
et sauvegarde les donnees dans une base PostgreSQL
"""

import sys
import os

# Ajouter le chemin du projet pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime

# Import des modules pour lire les signaux

# === IMPORTS POUR LES SOURCES DE SIGNAL ===
from rf_input.mock import generate_iq_samples
from rf_input.reader import read_iq_file
from rf_input.adapter import read_from_sdr

# Import des modules pour detecter les drones
from detection.features import extract_features
from detection.detector import is_drone

# Import des modules pour estimer la position
from localization.estimator import estimate_position
from localization.tracker import DistanceTracker

# Import du module pour sauvegarder dans la base de donnees
from storage.database import save_detection, get_connection

# Au demarrage, on verifie si on peut se connecter a la base de donnees
print("Verification de la connexion a la base de donnees...")
db_conn = get_connection()
if db_conn:
    print("Connecte a la base de donnees PostgreSQL")
    db_conn.close()
else:
    print("Base de donnees non disponible - mode test seulement")
print()


# =============================
# CHOIX DE LA SOURCE DU SIGNAL
# =============================
# Option 1 : Simulation (mock)
USE_MOCK = True  # True = donnees simulees, False = utiliser fichier IQ ou SDR
# Option 2 : Fichier IQ (mettre le chemin du fichier IQ)
IQ_FILE_PATH = "signal.iq"  # Remplacer par le nom du fichier reçu
# Option 3 : SDR reel (HackRF, RTL-SDR...)
# La fonction read_from_sdr() doit être complétée si tu utilises un SDR

fs = 20e6  # Frequence d'echantillonnage (20 MHz)

# Position du recepteur (coordonnees GPS)
receiver_position = {
    "lat": 46.5191,  # Latitude
    "lon": 6.5668    # Longitude
}

# Objet pour suivre les tendances de distance
distance_tracker = DistanceTracker()

# Boucle principale du programme
try:
    import time
    while True:
        # Recuperer l'heure actuelle
        timestamp = datetime.now()


        # =============================
        # CHOISIR LA SOURCE DU SIGNAL :
        # =============================
        # Décommente UNE SEULE des 3 options ci-dessous selon le cas :

        if USE_MOCK:
            # Option 1 : Simulation (mock)
            iq_samples = generate_iq_samples()
        # elif ... :
        #     # Option 2 : Fichier IQ
        #     iq_samples = read_iq_file(IQ_FILE_PATH)
        # else:
        #     # Option 3 : SDR reel
        #     iq_samples = read_from_sdr()

        # Etape 2 : Extraire les caracteristiques du signal
        # (RSSI, bande passante, duree, etc.)
        features = extract_features(iq_samples, fs)
        
        # Etape 3 : Determiner si c'est un drone ou pas
        detected, score = is_drone(features)

        # Etape 4 : Estimer la position du drone
        position = estimate_position(receiver_position, features["rssi"])
        
        # Etape 5 : Suivre l'evolution de la distance
        trend = distance_tracker.update(position["distance_relative"])

        # Afficher les resultats
        print("-" * 60)
        print(f"Heure : {timestamp.strftime('%Hh%M')}")
        print(f"RSSI moyen (relatif) : {features['rssi']:.2f} dB")
        print(f"Bande passante : {features['bandwidth'] / 1e6:.2f} MHz")
        print(f"Duree du signal : {features['duration']:.3f} s")
        print(f"Score de detection : {score:.2f}")

        print(f"Distance estimee (relative) : {position['distance_relative']:.2f}")
        print(f"Zone : {position['zone']}")
        print(f"Tendance : {trend}")

        # Si un drone est detecte, sauvegarder dans la base de donnees
        if detected:
            print("Drone probable detecte")
            
            # Etape 6 : Sauvegarder les donnees dans PostgreSQL
            # Cette fonction envoie automatiquement les donnees a la base
            drone_id, event_id = save_detection(
                timestamp=timestamp,
                rssi=features['rssi'],
                bandwidth=features['bandwidth'],
                score=score,
                distance=position['distance_relative'],
                drone_type="Unknown"  # Type inconnu pour l'instant
            )
            
            # Afficher confirmation si sauvegarde reussie
            if drone_id and event_id:
                print(f"  Sauvegarde en DB (Drone #{drone_id}, Event #{event_id})")
        else:
            print("Aucun drone detecte")

        # Pause d'1 seconde pour ralentir la boucle
        time.sleep(1)

# Gestion de l'arret du programme (Ctrl+C)
except KeyboardInterrupt:
    print("Arret demande par l'utilisateur")
