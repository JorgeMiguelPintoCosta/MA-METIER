import socket
import numpy as np


def read_from_tcp(host="127.0.0.1", port=5000, buffer_size=4096):
    """
    Réception des échantillons IQ envoyés par GNU Radio via un socket TCP.

    GNU Radio envoie un flux continu de données.
    Cette fonction se contente de recevoir les données brutes
    et de les convertir en tableau NumPy.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    raw = sock.recv(buffer_size)

    # IMPORTANT :
    # Le type doit correspondre exactement au type configuré dans GNU Radio
    # Float    -> np.float32
    # Complex  -> np.complex64
    samples = np.frombuffer(raw, dtype=np.complex64)

    return samples
