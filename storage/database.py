"""
Module de connexion et sauvegarde dans PostgreSQL
Ce fichier gere la connexion a la base de donnees et la sauvegarde
automatique des detections de drones
"""

import psycopg2
from psycopg2 import sql
from datetime import datetime
import os
from pathlib import Path

# ===================================================================
# CHARGEMENT DE LA CONFIGURATION DEPUIS LE FICHIER .env
# ===================================================================

# On cherche le fichier .env dans le dossier parent
env_file = Path(__file__).parent.parent / '.env'

# Si le fichier .env existe, on lit les parametres de connexion
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()  # Enlever les espaces
            # Ignorer les lignes vides et les commentaires
            if line and not line.startswith('#') and '=' in line:
                # Separer la cle et la valeur (ex: DB_NAME=drone_detection)
                key, value = line.split('=', 1)
                os.environ[key] = value

# ===================================================================
# CONFIGURATION DE LA CONNEXION POSTGRESQL
# ===================================================================

# Ces parametres sont lus depuis le fichier .env
# Si .env n'existe pas, on utilise les valeurs par defaut
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'localisation_dronesdb'),  # Nom de la base
    'user': os.getenv('DB_USER', 'admin'),                   # Nom d'utilisateur
    'password': os.getenv('DB_PASSWORD', 'admin'),           # Mot de passe
    'host': os.getenv('DB_HOST', 'localhost'),               # Adresse IP
    'port': os.getenv('DB_PORT', '5432')                     # Port PostgreSQL
}

# Variable globale pour savoir si la base est disponible
DB_AVAILABLE = None


# ===================================================================
# FONCTION DE CONNEXION
# ===================================================================

def get_connection():
    """
    Essaie de se connecter a la base PostgreSQL
    Retourne une connexion si OK, sinon None
    """
    global DB_AVAILABLE

    if DB_AVAILABLE is False:
        return None

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        DB_AVAILABLE = True
        return conn
    except psycopg2.Error as e:
        DB_AVAILABLE = False
        print("Base de donnees non disponible :", e)
        return None


# ===================================================================
# INITIALISATION DES TABLES
# ===================================================================

def init_database():
    """
    Cree les tables si elles n'existent pas encore
    """
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()

        # Table des drones detectes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Drones (
                ID SERIAL PRIMARY KEY,
                drone_type TEXT NOT NULL,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Table des evenements RF
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Signal_events (
                ID SERIAL PRIMARY KEY,
                ID_Drones INT REFERENCES Drones(ID),
                signal_strength INT,
                approx_distance INT,
                relative_power REAL,
                bandwidth REAL,
                score INT,
                detection_time REAL
            );
        """)

        # Table des alertes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alerts (
                ID SERIAL PRIMARY KEY,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Base de donnees initialisee avec succes")
        return True

    except psycopg2.Error as e:
        print("Erreur lors de l'initialisation :", e)
        conn.rollback()
        conn.close()
        return False


# ===================================================================
# SAUVEGARDE D'UN DRONE
# ===================================================================

def save_drone_detection(drone_type="Unknown"):
    """
    Enregistre un drone detecte
    """
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Drones (drone_type) VALUES (%s) RETURNING ID;",
            (drone_type,)
        )
        drone_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return drone_id

    except psycopg2.Error as e:
        print("Erreur sauvegarde drone :", e)
        conn.rollback()
        conn.close()
        return None


# ===================================================================
# SAUVEGARDE D'UN EVENEMENT RF
# ===================================================================

def save_signal_event(drone_id, signal_strength, approx_distance,
                      relative_power, bandwidth, score, detection_time):
    """
    Enregistre un evenement RF associe a un drone
    """
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Signal_events
            (ID_Drones, signal_strength, approx_distance,
             relative_power, bandwidth, score, detection_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING ID;
        """, (
            drone_id,
            signal_strength,
            approx_distance,
            relative_power,
            bandwidth,
            score,
            detection_time
        ))

        event_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return event_id

    except psycopg2.Error as e:
        print("Erreur sauvegarde signal :", e)
        conn.rollback()
        conn.close()
        return None


# ===================================================================
# FONCTION PRINCIPALE UTILISÉE PAR main.py
# ===================================================================

def save_detection(timestamp, rssi, bandwidth, score,
                   distance=None, drone_type="Unknown"):
    """
    Sauvegarde complete :
    - un drone
    - un evenement RF
    """
    conn = get_connection()
    if not conn:
        return None, None

    try:
        drone_id = save_drone_detection(drone_type)

        if not drone_id:
            return None, None

        event_id = save_signal_event(
            drone_id=drone_id,
            signal_strength=int(rssi),
            approx_distance=int(distance) if distance else None,
            relative_power=float(rssi),
            bandwidth=float(bandwidth),
            score=int(score * 100),
            detection_time=timestamp.timestamp()
        )

        return drone_id, event_id

    except Exception as e:
        print("Erreur sauvegarde detection :", e)
        return None, None


# ===================================================================
# LECTURE DES DETECTIONS
# ===================================================================

def get_recent_detections(limit=10):
    """
    Recupere les dernieres detections depuis la base
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.ID, d.drone_type, d.detected_at,
                   s.signal_strength, s.approx_distance,
                   s.relative_power, s.bandwidth, s.score
            FROM Drones d
            LEFT JOIN Signal_events s ON d.ID = s.ID_Drones
            ORDER BY d.detected_at DESC
            LIMIT %s;
        """, (limit,))

        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    except psycopg2.Error as e:
        print("Erreur lecture detections :", e)
        conn.close()
        return []
