import numpy as np
# NumPy permet de charger des fichiers binaires
# contenant des échantillons IQ


def read_iq_file(path):
    """
    Lit un fichier contenant des échantillons IQ complexes.

    path : chemin vers un fichier binaire IQ
           (par exemple généré par GNU Radio
            ou hackrf_transfer)
    """

    # Lecture du fichier binaire
    # Les données sont interprétées comme des complexes
    iq_samples = np.fromfile(path, dtype=np.complex64)

    # Retour des échantillons IQ
    return iq_samples


def read_from_sdr():
    """
    Fonction prévue pour lire directement depuis un SDR.

    Cette fonction est volontairement non implémentée
    tant qu'aucun matériel n'est connecté.
    """

    # Cette exception permet d'éviter toute ambiguïté :
    # si USE_MOCK = False et que rien n'est branché,
    # le programme s'arrête proprement
    raise NotImplementedError(
        "Lecture SDR non implémentée. Connecter un SDR réel."
    )
