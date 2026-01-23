def is_drone(features):
    """
    Détecte un drone à partir de caractéristiques RF.
    Retourne une décision ET un score de confiance.
    """

    score = 0.0

    # Largeur de bande typique drone
    if 5e6 < features["bandwidth"] < 25e6:
        score += 0.25

    # Puissance suffisante
    if features["rssi"] > -85:
        score += 0.15

    # Émission continue
    if features["duration"] > 0.05:
        score += 0.15

    # Structure OFDM
    if features["spectral_flatness"] < 0.6:
        score += 0.25

    # Stabilité spectrale
    if features["spectral_variance"] < 200:
        score += 0.20

    detected = score >= 0.7

    return detected, score
