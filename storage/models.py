class Detection:
    """
    Classe représentant une détection RF.

    Elle regroupe toutes les informations utiles
    sur un événement de détection de drone.
    """

    def __init__(self, timestamp, freq, rssi, bandwidth, distance):
        # Date et heure de la détection (format texte ISO)
        self.timestamp = timestamp

        # Fréquence centrale observée (en Hertz)
        self.freq = freq

        # Puissance moyenne reçue (RSSI en dB)
        self.rssi = rssi

        # Largeur de bande occupée par le signal (en Hertz)
        self.bandwidth = bandwidth

        # Distance estimée entre le récepteur et la source
        self.distance = distance
