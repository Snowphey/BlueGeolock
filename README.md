# BlueGeolock

<p align="center" width="100%">
    <img src="https://github.com/Snowphey/BlueGeolock/blob/master/img/Blue_Geolock_logo_title.png?raw=true" alt="bluegeolock_logo"/ width=700>
</p>

# À propos du projet

BlueGeolock est une application de suivi GPS temps réel utilisant une architecture microservices.
Nous avons voulu pousser le projet initial (suivi de deux marqueurs GPS sur une carte) un peu plus loin en créant une simulation de match de foot dans l'univers du manga [Blue Lock](https://fr.wikipedia.org/wiki/Blue_Lock).

Le site permet de simuler deux types de matchs : un match classique en 11 contre 11 (inspiré par l'arc [U-20](https://bluelock.fandom.com/wiki/U-20_Arc) du manga) ou bien un match en 3 contre 3 (inspiré par l'arc de la [deuxième sélection](https://bluelock.fandom.com/wiki/Second_Selection_Arc) du manga). 

Il est possible de faire tourner tout le projet en local, chaque service de l'architecture disposant de son propre Dockerfile.
Cependant, si besoin, on peut les faire tourner de manière individuelle sur des machines virtuelles que l'on reliera ensuite via [docker swarm](https://docs.docker.com/engine/swarm/).

Les services étant tous configurés sur le même réseau Docker (```bluegeolock_network```), ils pourront continuer de fonctionner.

## Architecture

L'application est composée de plusieurs services interdépendants :

- Un broker Kafka, qui est un genre de bus de données dans lequel on vient écrire et lire des bytes
- Des producers qui sont chargés d'écrire des données dans ce bus (des coordonnées GPS générées aléatoirement en continu)
- Un consumer est chargé de lire ces données, et de les insérer dans une base de données PostgreSQL
- Une base de données PostgreSQL qui stocke les coordonnées GPS lues par le consumer
- Une API FastAPI qui permet de requêter cette base de données PostgreSQL et qui permettra d'établir une connexion Websocket avec le frontend pour envoyer les nouvelles données en continu
- Le frontend (sous Vite + Vue) affiche sur une carte Leaflet l'évolution des marqueurs GPS selon leurs nouvelles coordonnées fournies par la Websocket

## Prérequis

- Docker
- Docker Compose

## Installation

1. Clonez le repository :
```bash
git clone https://github.com/Snowphey/BlueGeolock.git
cd BlueGeolock
```

2. Lancez le projet à l'aide des scripts bash déjà mis en place :
```bash
./start.sh
```

3. Le site est accessible à l'URL [```localhost:8080```](http://localhost:8080).

## Séparation des services avec Docker Swarm

Si l'on souhaite déplacer certains services sur d'autres machines virtuelles, on peut par exemple utiliser la commande ```docker swarm init``` qui renverra le résultat suivant :

```
$ docker swarm init
Swarm initialized: current node (6h48) is now a manager.

To add a worker to this swarm, run the following command:
docker swarm join \
--token SWMTKN-1-<generated_token_for_your_cluster> \
<manager internal IP address>:2377

To add a manager to this swarm, run 'docker swarm join-token manager'
and follow the instructions.
```

On peut alors ensuite ajouter des workers depuis leurs machines virtuelles grâce à la commande qui fournit le token du cluster et l'adresse IP du manager, puis lancer les services souhaités avec ```docker run```.

##

<p align="center" width="100%">
    <div align="center">Projet réalisé par :</div>
    <div align="center">
        <img src="https://github.com/Snowphey/BlueGeolock/blob/master/img/team%20cy%20hd.png?raw=true" alt="team_cy"/>
    </div>
    <div align="center">
        <a href="https://github.com/MatisToniutti">Matis Toniutti</a>, <a href="https://github.com/Snowphey">Sophie Longy</a>, <a href="https://github.com/Katorrz">Brice Morand</a>, <a href="https://github.com/a-vtn">Aventin Farret</a>
    </div>
</p>