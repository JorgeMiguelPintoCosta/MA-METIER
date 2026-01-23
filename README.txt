python/
├─ main.py                  # Boucle principale du programme
├─ detection/
│  ├─ __init__.py
│  ├─ features.py           # Extraction des caractéristiques du signal IQ
│  └─ detector.py           # Logique de détection du drone
├─ localization/
│  ├─ __init__.py
│  ├─ estimator.py          # Estimation de la distance du drone
│  ├─ rssi_model.py         # Modèle RSSI → distance relative
│  └─ tracker.py            # Suivi de l’évolution de la distance
├─ rf_input/
│  ├─ __init__.py
│  ├─ mock.py               # Simulation de signaux RF
│  ├─ reader.py             # Lecture de fichiers IQ
│  ├─ tcp_socket.py         # Réception des signaux RF en temps réel via socket TCP (depuis GNU Radio)
│  └─ source.py             # Point d'entrée unique pour récupérer les échantillons IQ (simulation ou réel)
├─ storage/
│  ├─ __init__.py
│  └─ database.py           # Gestion de la base de données PostgreSQL

2. main.py

main.py est le point d’entrée du projet.
Il orchestre l’ensemble des modules et fait tourner le système en continu.

À chaque itération, le programme :

récupère un signal RF (simulé par défaut),

extrait les caractéristiques principales du signal,

décide s’il s’agit probablement d’un drone,

estime une distance relative par rapport au récepteur,

observe si le drone se rapproche ou s’éloigne,

enregistre les informations dans la base de données si nécessaire.

La position du récepteur est fixée au départ, par exemple :

receiver_position = {"lat": 46.519, "lon": 6.5668}


Une pause d’une seconde est ajoutée entre chaque boucle afin de rendre l’affichage lisible.

3. Module detection
features.py

Ce fichier est chargé de transformer les échantillons IQ bruts en informations exploitables.
Les principales caractéristiques calculées sont :

le RSSI (puissance moyenne du signal),

la largeur de bande occupée,

la durée du signal analysé,

la structure fréquentielle du signal,

la stabilité spectrale.

Toutes ces valeurs sont relatives : elles servent à comparer les signaux entre eux, pas à donner des mesures absolues.

detector.py

La détection du drone repose sur une heuristique simple mais interprétable.
Chaque caractéristique contribue à un score global compris entre 0 et 1.

Si le score dépasse un seuil (0.7), le signal est considéré comme provenant d’un drone probable.
Cette approche permet de comprendre facilement pourquoi une détection a eu lieu.

4. Module localization
estimator.py

Ce module estime la distance relative entre le drone détecté et le récepteur RF.
Avec un seul capteur, il n’est pas possible de calculer une position GPS précise du drone.
À la place, le système indique si le drone est plutôt proche, à distance moyenne ou éloigné.

rssi_model.py

La distance est estimée à partir du RSSI à l’aide d’un modèle de propagation simplifié.
Le modèle n’est pas calibré en mètres réels, mais il permet de suivre les variations de distance.

tracker.py

Le tracker analyse l’évolution de la distance au fil du temps afin de déterminer si le drone :

se rapproche,

s’éloigne,

reste stable,

ou si les données sont insuffisantes pour conclure.


5. Module rf_input

Ce module gère toutes les sources de signaux RF utilisées dans le projet, que ce soit pour la simulation ou pour les tests réels avec du matériel SDR.

mock.py
Génère des signaux IQ simulés avec du bruit, pour tester l’ensemble du projet sans matériel.

reader.py
Permet de lire des fichiers IQ binaires (fonctionnalité avancée, à compléter selon le matériel utilisé).

tcp_socket.py
Permet de recevoir en temps réel les échantillons IQ envoyés par GNU Radio via un socket TCP. C’est ce fichier qui fait l’interface directe avec le flux réseau provenant du SDR.

source.py
Centralise la récupération des échantillons IQ. Le reste du projet utilise uniquement la fonction get_iq_samples(), qui bascule automatiquement entre la simulation (mock) et la réception réelle (tcp_socket) selon la configuration. Cela garantit une architecture propre et facilite les tests.

6. Module storage
database.py

Les détections peuvent être sauvegardées dans une base de données PostgreSQL.
La base contient notamment :

les informations générales sur les drones détectés,

les événements liés aux signaux RF,

les alertes générées par le système.

La base de données sert uniquement à conserver les résultats.
Toute la logique de détection reste dans le code Python.

7. Notes importantes

Tous les dossiers contiennent un fichier __init__.py afin de permettre les imports.

Les signaux RF utilisés sont simulés et volontairement simplifiés.

Les distances et valeurs RSSI sont relatives et non calibrées.

Le projet repose sur des règles heuristiques, et non sur du machine learning.

8. Comment tester le projet

Avant de lancer le projet, il faut s’assurer que Python (version 3.9 ou plus récente) est installé.

Installer les dépendances nécessaires :

pip install numpy psycopg2-binary


Lancer ensuite le programme :

python main.py


Le terminal affiche alors les caractéristiques du signal analysé et indique si un drone est détecté ou non.



9. Passage du mode simulé au mode réel (GNU Radio + SDR)

Le projet fonctionne en deux modes, facilement interchangeables :

 Mode simulé (par défaut) :
	- Les signaux IQ sont générés par rf_input/mock.py.
	- Toute la chaîne de traitement fonctionne sans matériel SDR.
	- Idéal pour le développement, les tests et la validation de l’architecture.
	- Pour ce mode, dans rf_input/source.py : USE_GNURADIO = False

 Mode réel (test final avec GNU Radio) :
	- GNU Radio récupère les signaux RF depuis le SDR et les envoie via un bloc TCP Sink.
	- Python reçoit ces signaux en temps réel grâce à rf_input/tcp_socket.py.
	- Pour activer ce mode, il suffit de mettre USE_GNURADIO = True dans rf_input/source.py

La bascule entre les deux modes se fait en changeant une seule variable, sans toucher au reste du code.

Lancement :
1. Démarrer GNU Radio avec un bloc TCP Sink (Host : 127.0.0.1, Port : 5000, Type : Complex ou Float selon le traitement).
2. Vérifier que le type de données envoyé par GNU Radio correspond à celui attendu en Python (voir tableau ci-dessous).
3. Lancer python main.py

Lors du test réel, GNU Radio est utilisé pour récupérer les signaux RF depuis un SDR, puis les transmettre au programme Python via un socket TCP.

Principe général :

SDR → GNU Radio → TCP Socket → Python → Détection de drone


Étapes à suivre :

Configurer GNU Radio avec un TCP Sink

Host : 127.0.0.1

Port : 5000

Type : Complex (ou Float, selon le traitement choisi)

Activer la réception GNU Radio côté Python :

USE_GNURADIO = True


Lancer les programmes dans le bon ordre :

D’abord GNU Radio

Ensuite python main.py


9.3 Types de données échangées

Le type de données envoyé par GNU Radio doit correspondre exactement à celui utilisé dans le code Python :

 GNU Radio  Python        

 Float      np.float32   
 Complex    np.complex64 

Une incohérence de type entraînera des résultats incorrects (RSSI faux, bande passante erronée, détection invalide).

9.4 Ajustement des seuils en conditions réelles

Les seuils utilisés pour la détection (RSSI, bande passante, durée, score) sont définis pour un environnement simulé.

Lors des tests réels, il est normal de devoir :

ajuster la bande passante minimale

ajuster le seuil de score global

affiner les critères en fonction du bruit réel

Ces ajustements font partie du travail d’expérimentation et ne constituent pas une erreur du système.

9.5 Point important

Le fichier main.py reste strictement identique entre les deux modes.

Toute la gestion de la source RF est centralisée dans le module rf_input/source.py, ce qui permet :

une architecture propre

une maintenance simple

une transition fluide entre simulation et réel
