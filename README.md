# Procédure d'installation du projet

A brief description of what this project does and who it's for


## Prérequis matériel
Une clé USB d'au moins 8 Go (vide).
L'image disque (ISO) d'Ubuntu (version 24.04 LTS recommandée pour la stabilité).
Un utilitaire pour flasher la clé (comme Rufus).
PC Physique : Un processeur i5/i7 (minimum 4 cœurs) pour gérer le traitement du signal en temps réel et 8 Go de RAM.
HackRF One : Le transceiver SDR capable de balayer de 1 MHz à 6 GHz.
Antennes : * Antennes bi-bandes (2.4/5.8 GHz) à gain élevé.
Câblage : Câble USB blindé avec ferrite pour limiter les interférences électromagnétiques du PC.


## Prérequis logiciel
Système : Ubuntu 24.04 LTS (installé en "Bare Metal" pour l'accès direct à l'USB).
GNU Radio (v3.10+) : Pour la création des blocs de traitement numérique.
Python 3 : Pour scripter l'automatisation du scan et l'export des données.
Librairies clés : gr-osmosdr (interface HackRF), gr-specest (pour l'estimation de direction si plusieurs antennes) et python3-numpy.


## Procédure d'installation
Téléchargez l'ISO sur le site officiel d'Ubuntu.
Branchez votre clé USB.
Ouvrez votre utilitaire (rufus), sélectionnez l'ISO, choisissez la clé USB et cliquez sur Flash.
Le PC va démarrer sur la clé. Choisissez "Try or Install Ubuntu".
1.	Langue : Sélectionnez "Français".
2.	Type d'installation : Choisissez "Installation normale".
3.	Options : Cochez impérativement "Installer un logiciel tiers pour le matériel graphique et Wi-Fi". Cela facilite grandement la gestion des drivers plus tard.
4.	Type d'installation : * Si vous voulez effacer Windows : "Effacer le disque et installer Ubuntu".
5.	Partitionnement : Si vous débutez, laissez les options par défaut.
6.	Utilisateur : Choisissez un nom d'utilisateur et un mot de passe (ne l'oubliez pas, il sera requis pour chaque commande sudo dans GNU Radio).
Une fois l'installation terminée, retirez la clé et redémarrez. Ouvrez un terminal pour finaliser la configuration système.

# Mise à jour des dépôts
sudo apt update

# Installation des outils de compilation (essentiels pour les drivers SDR futurs)
sudo apt install build-essential cmake git -y


## GNU Radio
Sur Ubuntu, vous avez deux choix principaux : les dépôts officiels (simple, mais parfois datés) ou le PPA de l'équipe GNU Radio (recommandé pour avoir les dernières fonctionnalités).
Option recommandée : Via PPA

sudo add-apt-repository ppa:gnuradio/gnuradio-releases
sudo apt update
sudo apt install gnuradio

sudo add-apt-repository ppa:gnuradio/gnuradio-releases sudo apt update sudo apt install gnuradio gr-osmosdr hackrf libhackrf-dev

sudo cp /usr/share/libhackrf0/53-hackrf.rules /etc/udev/rules.d/ sudo udevadm control --reload-rules && sudo udevadm trigger

Une fois l'installation terminée, tapez gnuradio-companion dans votre terminal. L'interface graphique devrait s'ouvrir. Puis hackrf_info pour plus d’info sur le HackRF connecté.


GNU Radio seul ne sert à rien sans drivers pour communiquer avec votre matériel (RTL-SDR, HackRF, Ettus USRP, etc.).

sudo apt install soapysdr-tools libsoapysdr-dev

B. Pour les clés RTL-SDR (les plus communes)

sudo apt install rtl-sdr librtlsdr-dev
Important : Par défaut, Linux charge un driver "TV" qui bloque la SDR. Il faut le "blacklister".
1.	Créez un fichier : sudo nano /etc/modprobe.d/blacklist-rtl.conf
2.	Copiez-y cette ligne : blacklist dvb_usb_rtl28xxu
3.	Enregistrez (Ctrl+O, Entrée) et quittez (Ctrl+X).
C. Pour le matériel Ettus (USRP)
Si vous avez un USRP, il vous faut le driver UHD :

sudo apt install libuhd-dev uhd-host

Pour aller plus loin, vous aurez besoin de gr-osmosdr, qui permet d'utiliser les blocs "Source" et "Sink" pour la plupart des radios.

sudo apt install gr-osmosdr

## Base de données
### Lancer le container PostgreSQL
Télécharger le fichier localisation_dronesdb.sql.
Ouvrez un terminal et exécutez une seule ligne :
´´´
docker run -d --name postgres_db -p 5432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=localisation_dronesdb postgres:14.20-trixie
Cette commande :
Crée un container postgres_db
Expose PostgreSQL sur le port 5432
Crée l’utilisateur admin avec le mot de passe admin
Crée la base localisation_dronesdb
Au premier lancement, Docker télécharge automatiquement l’image PostgreSQL.
Vérifier que le container fonctionne docker ps
Vous devez voir :
NAME → postgres_db
STATUS → Up ...
Si le container n’apparaît pas :
docker ps -a

###	Importer le fichier SQL du projet
Copiez ces deux commandes une par une :
docker cp localisation_dronesdb.sql postgres_db:/localisation_dronesdb.sql
docker exec -it postgres_db psql -U admin -d localisation_dronesdb -f /localisation_dronesdb.sql

###	Accéder à PostgreSQL depuis le container docker exec -it postgres_db psql -U admin -d localisation_dronesdb
Prompt attendu :
localisation_dronesdb=#
Commandes utiles
Lister les tables : \dt
Voir les colonnes d’une table : \d nom_de_la_table
Vérifier les données : SELECT * FROM nom_de_la_table;

### Arrêter / relancer le container 
docker stop postgres_db docker start postgres_db
Les données sont conservées automatiquement grâce au volume Docker.

### Problèmes fréquents
failed to connect to the Docker API → Docker n’est pas lancé
docker: invalid reference format → commande mal copiée (doit être sur une seule ligne)
Port 5432 déjà utilisé → fermer PostgreSQL local ou changer le port :
-p 5433:5432



Étapes pour installer et configurer l’environnement.
1.	Configurer la base de données PostgreSQL si besoin :
- Remplir le fichier .env avec les bons identifiants (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
Pour sortir du mode simulation (activé par défaut) :
1. Ouvrir le fichier rf_input/source.py
2. Remplacer la ligne :

   	 USE_GNURADIO = False
  	par
   	 USE_GNURADIO = True

3. Lancer le script Python normalement :

    python main.py

2. Configurer la base de données PostgreSQL si besoin :
   - Remplir le fichier .env avec les bons identifiants (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

## Scripts Python


## Application Web

### Lancement avec Docker

### Prérequis
- Docker Desktop installé et en cours d'exécution
- Node.js (version 16 ou plus)
- npm

### Installation
1. Cloner le projet
2. Lancer `npm install` pour installer les dépendances.

### Démarrage


```bash
# Construire et lancer l'application
docker-compose up --build

# Ou en arrière-plan
docker-compose up --build -d
```

### Accès
- **Application**: http://localhost:5000
- **Base de données**: localhost:5432 (drone_user / drone_pass)

## API

### Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/detections` | Liste des détections |
| POST | `/api/detections` | Nouvelle détection |
| GET | `/api/detections/:id` | Détection par ID |
| DELETE | `/api/detections/:id` | Supprimer détection |
| GET | `/api/detections/stats` | Statistiques |
| GET | `/health` | État du service |

### Ajouter une détection (exemple)

```bash
curl -X POST http://localhost:5000/api/detections \
  -H "Content-Type: application/json" \
  -d '{
    "frequency": "2.4 GHz",
    "rssi": -55,
    "position_gps": "48.8566,2.3522",
    "drone_id": "TEST-001",
    "detection_type": "DJI Mavic",
    "status": "threat"
  }'
```

## Base de données

La base PostgreSQL est initialisée automatiquement avec des données de test au premier démarrage.

### Structure de la table `detections`

| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL | Identifiant unique |
| timestamp | TIMESTAMP | Horodatage |
| drone_id | VARCHAR(50) | ID du drone |
| detection_type | VARCHAR(50) | Type de signal |
| frequency | VARCHAR(20) | 2.4 GHz ou 5.8 GHz |
| rssi | INTEGER | Puissance signal (-100 à 0 dBm) |
| position_gps | VARCHAR(50) | Coordonnées GPS |
| status | VARCHAR(20) | threat, friendly, unknown |

## Arrêt

```bash
# Arrêter les conteneurs
docker-compose down

# Arrêter et supprimer les données
docker-compose down -v
```

## Dépanage
Si rien ne s’affiche, vérifiez :
-	La configuration du port et le type de données.
-	Ajuster la sensibilité ou le seuil de détection (vous pouvez les modifier dans les paramètres des modules de détection.)
-	Testez la connection avec la base de données avec :
python test_database.py
Problèmes fréquents :
Probleme : "Base de donnees non disponible"
 	Solution : Verifier que .env existe avec les bonnes infos
Solution : Lancer python test_database.py pour voir l'erreur

Probleme : "could not connect to server"
Solution : Vérifier l'adresse IP dans .env
Solution : Vérifier qu'on est sur le même WiFi

Probleme : "password authentication failed"
Solution : Vérifier le mot de passe dans .env
Solution : Pas d'espace avant ou après le signe « = »

Probleme : "ModuleNotFoundError: psycopg2"
Solution : pip install psycopg2-binary

