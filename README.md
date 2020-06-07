# API pour l'application ARriddle

## Développement

Python 3.6+ nécessaire

* Création du virtualenv (à ne faire qu'une fois) : `python3 -m venv .venv`
* Activation du virtualenv : `source .venv/bin/activate`
* Installation des dépendances (seulement si les dépendances ont changé) : `pip install -r requirements.txt`
* Se placer dans le dossier de l'application : `cd app/`
* Lancer le serveur avec : `uvicorn --reload main:app --host 0.0.0.0`

## Déploiement

Le plus simple pour le déploiement est d'utiliser docker avec le `Dockerfile` fourni (`docker build . -t arriddle --build-arg API_VERSION=1`)
Pour lancer le conteneur Docker  : `docker run -p 8000:8000 -it arriddle`
Dans le cas d'une utilisation avec un reverse proxy tel que Traefik, on peut également utiliser le `docker-compose.yml` fourni.
Dans ce cas, on pourra simplement faire `docker-compose up -d` après avoir paramétré les champs du docker-compose

## Documentation
Il est possible de se connecter au endpoint `redoc` ou `doc` pour obtenir la liste des endpoints disponibles.
Plus de documentation sur fastapi est disponible sur https://fastapi.tiangolo.com/