import numpy as np
# Import de NumPy, bibliothèque essentielle pour le calcul numérique
# et le traitement du signal (FFT, moyennes, variances, etc.)


def spectral_flatness(power_spectrum):
    """
    Calcule la spectral flatness (platitude spectrale).

    Cette métrique permet de savoir si l'énergie du signal
    est répartie uniformément sur les fréquences ou non.

    - Bruit pur            -> valeur proche de 1
    - Signal structuré     -> valeur plus faible (OFDM, drone)
    """

    # Ajout d'une très petite valeur pour éviter log(0),
    # ce qui provoquerait une erreur mathématique
    safe_power = power_spectrum + 1e-12

    # Calcul de la moyenne géométrique :
    # 1. logarithme de chaque valeur du spectre
    # 2. moyenne des logarithmes
    # 3. exponentielle pour revenir à l'échelle normale
    geometric_mean = np.exp(np.mean(np.log(safe_power)))

    # Calcul de la moyenne arithmétique classique
    # Elle représente l'énergie moyenne globale du spectre
    arithmetic_mean = np.mean(power_spectrum)

    # Rapport entre moyenne géométrique et arithmétique
    # Plus ce rapport est bas, plus le signal est structuré
    return geometric_mean / (arithmetic_mean + 1e-12)


def extract_features(iq_samples, fs):
    """
    Extrait des caractéristiques RF à partir d'échantillons IQ.

    iq_samples : tableau complexe représentant le signal RF
    fs         : fréquence d'échantillonnage en Hertz
    """

    # Transformation du signal du domaine temporel
    # vers le domaine fréquentiel (FFT)
    spectrum = np.fft.fft(iq_samples)

    # Réorganisation du spectre pour centrer la fréquence 0
    spectrum = np.fft.fftshift(spectrum)

    # Calcul de la puissance pour chaque fréquence
    # |X|^2 = puissance du signal
    power = np.abs(spectrum) ** 2

    # Conversion de la puissance en décibels
    # 10*log10 car on travaille sur une puissance
    power_db = 10 * np.log10(power + 1e-12)

    # Estimation du RSSI :
    # moyenne de la puissance spectrale en dB
    rssi = power_db.mean()

    # Définition d'un seuil dynamique :
    # 6 dB au-dessus du niveau moyen du bruit
    threshold = rssi + 6

    # Création d'un masque indiquant quelles fréquences
    # sont significativement occupées par un signal
    occupied_bins = power_db > threshold

    # Calcul de la largeur de bande occupée :
    # - nombre de bins actifs
    # - multiplié par la résolution fréquentielle
    bandwidth = np.sum(occupied_bins) * fs / len(power_db)

    # Calcul de la platitude spectrale
    # Permet de détecter une structure OFDM
    flatness = spectral_flatness(power)

    # Calcul de la variance du spectre en dB
    # Faible variance -> signal stable (drone)
    # Forte variance  -> Wi-Fi, bruit impulsionnel
    spectral_variance = np.var(power_db)

    # Retour des caractéristiques sous forme de dictionnaire
    return {
        # Puissance moyenne reçue
        "rssi": float(rssi),

        # Largeur de bande occupée par le signal
        "bandwidth": float(bandwidth),

        # Durée du signal analysé en secondes
        "duration": len(iq_samples) / fs,

        # Indicateur de structure fréquentielle
        "spectral_flatness": float(flatness),

        # Indicateur de stabilité du spectre
        "spectral_variance": float(spectral_variance),
    }
