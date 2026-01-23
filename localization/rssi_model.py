import math

def rssi_to_distance(rssi):
    """
    Convertit un RSSI RELATIF en distance RELATIVE.

    Ce modèle n'est PAS calibré en mètres.
    Il sert uniquement à comparer les variations dans le temps.
    """

    # RSSI de référence quand le drone est "proche"
    rssi_reference = 40.0

    # Facteur de perte (environnement libre approximatif)
    path_loss_exponent = 2.0

    # Modèle de propagation logarithmique inversé
    distance = 10 ** ((rssi_reference - rssi) / (10 * path_loss_exponent))

    return float(distance)
