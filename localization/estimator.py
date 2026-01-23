from .rssi_model import rssi_to_distance

def estimate_position(receiver_pos, rssi):
    """
    Estime une distance RELATIVE entre le récepteur et le drone.

    Avec un seul capteur RF :
    - pas de direction
    - pas de position GPS du drone
    """

    # Conversion RSSI -> distance relative
    distance = rssi_to_distance(rssi)

    # Classification en zones simples
    if distance < 1.5:
        zone = "proche"
    elif distance < 4.0:
        zone = "moyenne"
    else:
        zone = "loin"

    return {
        "distance_relative": distance,
        "zone": zone,
        "receiver_lat": receiver_pos["lat"],
        "receiver_lon": receiver_pos["lon"]
    }
