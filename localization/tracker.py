from collections import deque

class DistanceTracker:
    """
    Analyse l'évolution de la distance dans le temps.
    Permet de savoir si le drone se rapproche ou s'éloigne.
    """

    def __init__(self, window_size=5):
        self.history = deque(maxlen=window_size)

    def update(self, distance):
        self.history.append(distance)

        # Pas assez de données
        if len(self.history) < 2:
            return "inconnue"

        # Variation globale
        delta = self.history[-1] - self.history[0]

        if delta < -0.2:
            return "rapprochement"
        elif delta > 0.2:
            return "eloignement"
        else:
            return "stable"
