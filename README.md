# Procédure d'installation du projet

A brief description of what this project does and who it's for

## Prérequis matériel

## Prérequis logiciel


## Procédure d'installation

## GNU Radio


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

