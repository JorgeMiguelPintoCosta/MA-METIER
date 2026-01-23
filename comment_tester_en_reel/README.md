# Comment tester le projet en conditions réelles (côté Python uniquement)

Ce guide explique uniquement ce qu'il faut faire dans le code Python pour passer du mode simulation au test réel avec des signaux reçus en direct.

## Étapes à suivre côté Python

1. **Ouvrir le fichier** `rf_input/source.py`.
2. **Modifier la ligne suivante** pour activer la réception réelle :

   ```python
   USE_GNURADIO = True
   ```

   (Par défaut, la valeur est False pour la simulation. Il suffit de la passer à True pour recevoir les signaux envoyés en temps réel sur le port 5000.)

3. **Vérifier la correspondance du type de données** :
   - Si GNU Radio envoie des données Complex, le code Python attend `np.complex64` (c'est le cas par défaut).
   - Si GNU Radio envoie des Float, il faut adapter le type dans `tcp_socket.py` (remplacer `np.complex64` par `np.float32`).

4. **Lancer le programme Python** normalement :

   ```bash
   python main.py
   ```

Le script va alors recevoir les signaux en temps réel, effectuer la détection et afficher les résultats dans le terminal.

## Conseils
- Il n'y a qu'un seul paramètre à changer pour passer du mode simulation au mode réel : `USE_GNURADIO` dans `source.py`.
- Si vous devez ajuster la sensibilité ou les seuils de détection, modifiez les paramètres dans les modules de détection.
- Si vous ne recevez rien, vérifiez que le port 5000 est bien utilisé et que le type de données correspond.

Ce guide est fait pour que toute personne reprenant le code Python puisse faire le test réel sans question supplémentaire.