"""
Ce module centralise la récupération des signaux RF.

Le reste du projet ne dépend pas de la source :
- signal simulé
- signal réel via GNU Radio
"""

from rf_input.mock import generate_iq_samples

USE_GNURADIO = False


def get_iq_samples():
    """
    Fonction unique utilisée dans tout le projet
    pour récupérer des échantillons IQ.
    """

    if USE_GNURADIO:
        from rf_input.tcp_socket import read_from_tcp
        return read_from_tcp()

    return generate_iq_samples()
