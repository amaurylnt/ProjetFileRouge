Rendu – Projet Docker : Plateforme de Supervision “Lite” de Caméras

1. Contexte du projet

Dans le cadre du module “Conteneurisation avec Docker”, l’objectif était de réaliser un projet libre autour de Docker, permettant de démontrer la compréhension et la maîtrise :

de la création d’images Docker,
de l’orchestration via Docker Compose,
de la gestion d’un écosystème multi-services,
ainsi que du monitoring (Prometheus + Grafana).

Mon choix s’est porté sur une plateforme de supervision “lite” de caméras simulées, un sujet cohérent avec mon domaine professionnel (vidéoprotection).


2. Objectifs techniques

Le projet devait permettre de :

Simuler un ensemble de caméras IP (nom, IP, localisation, statut).
Les stocker dans une base de données PostgreSQL.
Exposer ces données via une API Python/Flask containerisée.
Afficher les caméras dans un front web Nginx statique, containerisé lui aussi.
Mettre en place un monitoring complet avec :
Prometheus → récupération des métriques de l’API
Grafana → visualisation et dashboard d’observabilité

Le tout orchestré dans un docker-compose, avec réseau interne, volumes et variables d’environnement.


3. Architecture technique

Voici les services mis en place :

	1. Base de données – PostgreSQL

	Stocke la liste des caméras (id, nom, IP, statut, localisation).
	Initialisée automatiquement via un script init.sql.
	Volume Docker pour la persistance : db-data.

	2. API – Python Flask

	Expose plusieurs endpoints :

	/health → état du service
	/cameras → renvoie la liste des caméras
	/cameras/<id> → détail d’une caméra
	/metrics → métriques Prometheus

	Connexion à PostgreSQL via SQLAlchemy.
	Image construite à partir d’un Dockerfile custom.

	3. Frontend – NGINX

	Interface simple HTML / JavaScript.
	Récupère les données via /api/cameras grâce à un reverse proxy NGINX.
	Image custom basée sur nginx:alpine.

	4. Prometheus

	Scrappe automatiquement :

	l’API Flask (endpoint /metrics),
	Prometheus lui-même.

	Configuré via prometheus.yml.

	5. Grafana

	Permet la visualisation des métriques.

	Dashboard créé avec plusieurs panels :
	total des requêtes API,
	taux de requêtes par seconde,
	statut de l’API (UP/DOWN),
	etc.


4. Fonctionnement global

Lorsque la stack est lancée :
PostgreSQL démarre et initialise automatiquement la table cameras et ses données.
L’API Flask se connecte à la base et expose les endpoints.
Le front NGINX interroge l’API via /api/... et affiche les caméras.
Prometheus scrappe l’API toutes les 15 secondes.
Grafana permet d’afficher les métriques sous forme de dashboard.

L’ensemble fonctionne grâce à Docker Compose, qui gère :
les builds,
les réseaux internes,
les dépendances,
les volumes,
les variables d’environnement (via .env).


5. Commandes principales

Lancer toute la stack :
docker compose up -d --build

Arrêter la stack :
docker compose down

Voir les logs d’un service :
docker compose logs api
docker compose logs db

Accès aux services :
Frontend → http://localhost:8080
API → http://localhost:8000
Prometheus → http://localhost:9090
Grafana → http://localhost:3000


6. Tests réalisés

Vérification que le front affiche bien les caméras en provenance de la base SQL.
Vérification du bon fonctionnement des endpoints API.
Vérification que Prometheus détecte correctement l’API (cible UP).

Création d’un dashboard Grafana incluant :

courbe api_requests_total
taux de requêtes par seconde via rate()
statut de scrape up{job="api"}

Tout est fonctionnel.


7. Difficultés rencontrées

Plusieurs difficultés techniques ont été rencontrées lors de la mise en place des services Docker :

Problèmes de dépendances Python lors du build de l’API
L’installation de certaines librairies, notamment psycopg2-binary, échouait dans l’image python:3.12-slim car les dépendances système n’étaient pas présentes. J’ai dû ajouter l’installation de libpq-dev et build-essential dans le Dockerfile pour garantir une compilation correcte.

Connexion API → Base de données instable au démarrage
L’API tentait de se connecter à PostgreSQL alors que celui-ci n’était pas encore totalement initialisé, provoquant des erreurs “connection refused”. L’utilisation de depends_on, associée à une configuration plus robuste via SQLAlchemy, a permis de stabiliser la connexion.

Script SQL d’initialisation non exécuté
Au premier démarrage, la table cameras n’était pas créée car le fichier init.sql n’était pas correctement monté dans le dossier attendu par Postgres. Une correction du chemin dans le docker-compose.yml ( /docker-entrypoint-initdb.d/ ) a résolu le problème.

Fichiers du front non chargés par NGINX
Lors des premiers tests, le front affichait une page blanche. Les fichiers HTML/JS n’étaient pas copiés au bon emplacement dans l’image NGINX. Après ajustement du Dockerfile et copie dans /usr/share/nginx/html/, le front s’est chargé correctement.


8. Améliorations possibles

Ajout d’une authentification sur l’API.
Ajout d’un vrai flux RTSP simulé (ex : rtsp-simple-server).
Partition multi-sites (plusieurs villes, VLANs simulés).
Alerting via Alertmanager.
Ajout de métriques plus détaillées : temps de réponse, histogrammes, labels par endpoint.


9. Conclusion

Ce projet m’a permis de mettre en œuvre les connaissances acquises sur Docker :

Création d’images,
Docker Compose multi-services,
Réseaux internes,
Persistance avec volumes,
Monitoring complet avec Prometheus + Grafana.

Le projet est totalement fonctionnel et reproductible sur n’importe quelle machine disposant de Docker.