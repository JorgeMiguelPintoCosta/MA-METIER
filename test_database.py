"""
Script de test pour la base de données PostgreSQL
Permet de vérifier la connexion et d'initialiser les tables
"""

from storage.database import (
    get_connection, 
    init_database,
    save_drone_detection,
    save_signal_event,
    save_alert,
    save_detection,
    get_recent_detections,
    get_alerts
)
from datetime import datetime


def test_connection():
    """Test la connexion à la base de données"""
    print("Test de connexion à PostgreSQL ignoré (mode sans base de données)")
    return True


def test_init_database():
    """Test l'initialisation de la base de données"""
    print("Initialisation de la base de données ignorée (mode sans base de données)")
    return True


def test_insert_data():
    """Test l'insertion de données"""
    print("\nTest d'insertion de données...")
    
    # Test 1: Enregistrer un drone
    print("  - Insertion d'un drone...")
    drone_id = save_drone_detection("DJI Phantom 4")
    if drone_id:
        print(f"    ✓ Drone enregistré avec ID: {drone_id}")
    else:
        print("    ✗ Échec d'enregistrement du drone")
        return False
    
    # Test 2: Enregistrer un événement de signal
    print("  - Insertion d'un événement de signal...")
    event_id = save_signal_event(
        drone_id=drone_id,
        signal_strength=40,
        approx_distance=100,
        relative_power=40.5,
        bandwidth=2.14,
        score=60,
        detection_time=datetime.now().timestamp()
    )
    if event_id:
        print(f"    ✓ Événement enregistré avec ID: {event_id}")
    else:
        print("    ✗ Échec d'enregistrement de l'événement")
        return False
    
    # Test 3: Enregistrer une alerte
    print("  - Insertion d'une alerte...")
    alert_id = save_alert("WARNING", "Test d'alerte - Drone détecté")
    if alert_id:
        print(f"    ✓ Alerte enregistrée avec ID: {alert_id}")
    else:
        print("    ✗ Échec d'enregistrement de l'alerte")
        return False
    
    # Test 4: Utiliser la fonction combinée save_detection
    print("  - Test de save_detection (fonction combinée)...")
    drone_id2, event_id2 = save_detection(
        timestamp=datetime.now(),
        rssi=42.3,
        bandwidth=2.5e6,
        score=0.75,
        distance=150,
        drone_type="Parrot Anafi"
    )
    if drone_id2 and event_id2:
        print(f"    ✓ Détection complète enregistrée (Drone ID: {drone_id2}, Event ID: {event_id2})")
    else:
        print("    ✗ Échec de save_detection")
        return False
    
    return True


def test_read_data():
    """Test la lecture des données"""
    print("\nTest de lecture des données...")
    
    # Test 1: Récupérer les détections récentes
    print("  - Récupération des détections récentes...")
    detections = get_recent_detections(limit=5)
    if detections:
        print(f"    ✓ {len(detections)} détection(s) récupérée(s)")
        for det in detections[:2]:  # Afficher les 2 premières
            print(f"      - Drone ID: {det[0]}, Type: {det[1]}, RSSI: {det[5]}")
    else:
        print("    ⚠ Aucune détection trouvée (normal si c'est la première exécution)")
    
    # Test 2: Récupérer les alertes
    print("  - Récupération des alertes...")
    alerts = get_alerts(limit=5)
    if alerts:
        print(f"    ✓ {len(alerts)} alerte(s) récupérée(s)")
        for alert in alerts[:2]:  # Afficher les 2 premières
            print(f"      - {alert[1]}: {alert[2]}")
    else:
        print("    ⚠ Aucune alerte trouvée")
    
    return True


def main():
    """Fonction principale de test"""
    print("=" * 60)
    print("TEST DE LA BASE DE DONNÉES POSTGRESQL")
    print("=" * 60)
    print("MODE SANS BASE DE DONNÉES ACTIVÉ")
    print("=" * 60)
    test_connection()
    test_init_database()
    print("\nTous les tests liés à la base de données sont ignorés.")


if __name__ == "__main__":
    main()
