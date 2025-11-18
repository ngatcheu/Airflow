# Airflow — Déploiement local avec Docker Compose

Ce dossier contient une configuration d'Apache Airflow destinée au développement local, basée sur l'image officielle et un exemple de pipeline (DAG) de démonstration.

## Contenu du dossier `Airflow/`

- `Dockerfile` : image personnalisée qui installe les dépendances listées dans `Airflow/requirements.txt`.
- `docker-compose.yaml` : composition Docker pour exécuter Airflow (Postgres, Redis, webserver, scheduler, workers, ...).
- `dags/` : dossiers des DAGs (ex : `demo_etl_pipeline.py`).
- `logs/`, `plugins/`, `config/` : volumes partagés montés dans le conteneur.

## Prérequis

- Docker (version récente)
- Docker Compose (ou la commande `docker compose` intégrée)
- Bash / shell (exemples fournis pour Linux)

Assurez-vous d'avoir alloué suffisamment de ressources à Docker (au moins 4GB RAM et 2 CPUs recommandés pour ce setup local).

## Configuration importante

- L'image par défaut utilisée est `apache/airflow:3.1.2` (visible dans `docker-compose.yaml`).
- Les identifiants d'administration par défaut (créés par le service `airflow-init`) sont :
	- utilisateur : `airflow`
	- mot de passe : `airflow`
	Ces valeurs peuvent être surchargées via les variables d'environnement `_AIRFLOW_WWW_USER_USERNAME` et `_AIRFLOW_WWW_USER_PASSWORD` (ex : via un fichier `.env`).

- Les DAGs, logs, config et plugins sont montés depuis le dossier `Airflow/` vers `/opt/airflow/` dans les conteneurs. Pour ajouter un DAG, déposer le fichier dans `Airflow/dags/`.

## Démarrage (Bash / Linux)

1) Se placer à la racine du dépôt :

```bash
cd /chemin/vers/le/projet/airflow
# Exemple (si vous avez le même emplacement que dans l'environnement de développement) :
# cd ~/Desktop/DEV/airflow
```

2) Sur tous les systèmes d'exploitation, vous devez exécuter des migrations de base de données et créer le premier compte utilisateur. Pour ce faire, courez:

```bash
# depuis le dossier Airflow/
docker compose up airflow-init
```

3) Lancer les services avec Docker Compose :

```bash
# Utiliser le fichier docker-compose inclus dans ce dossier (Airflow/)
docker compose  up -d
```

4) Vérifier les services :

```bash
docker ps --filter "name=airflow" --filter "name=postgres" --filter "name=redis"
```

5) Accéder à l'interface web :

- URL : http://localhost:8080
- identifiants : `airflow` / `airflow` (si non modifiés)

## Commandes utiles

- Voir les logs d'un service (ex : webserver) :

```bash
docker-compose  logs -f airflow-apiserver
```

- Exécuter des commandes `airflow` dans le conteneur :

```bash
docker-compose  run --rm airflow-cli airflow dags list
```

- Arrêter et supprimer les conteneurs :

```bash
docker-compose  down --volumes --remove-orphans
```

## DAG de démonstration

Un DAG d'exemple est présent dans `dags/demo_etl_pipeline.py`. Il illustre un pipeline ETL simple (extract → transform → load → notify). Pour le tester, il suffit de déposer/éditer le fichier dans `dags/` et de surveiller l'UI Airflow.

## Debug / problèmes courants

- Ressources Docker insuffisantes : augmentez la RAM/CPU dans les paramètres Docker Desktop.
- Permissions sur les fichiers (Linux/macOS) : définir `AIRFLOW_UID` dans `.env` pour correspondre à votre UID local (cf. commentaires dans `docker-compose.yaml`).
- Installation de dépendances : le `Dockerfile` installe les paquets listés dans `requirements.txt`. Pour ajouter une dépendance, mettez-la dans ce fichier et rebuild l'image.


