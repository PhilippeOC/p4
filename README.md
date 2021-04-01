# Projet 4 : Développez un programme logiciel en Python.
## Programme de gestion de tournois d'échecs

Ce programme permet:
- de creér un nouveau tournoi,
- d'ajouter des joueurs à ce tournoi,
- de rentrer le nombre de rondes de ce tournoi,
- de saisir les scores des matchs,
- de générer des paires à l'aide du système suisse,
- de reprendre un tournoi en cours.

Toutes les données sont enregistrées dans une base de données.

# Installation
1. Créer un environnement virtuel avec la commande:
- sous Windows: `python -m venv <environment_name>`  
- sous Linux: `python3 -m venv <environment_name>`

2. Activer cet environnement avec la commande:
- sous Windows: `<environment_name>\Scripts\Activate.ps1`
- sous Linux: `source <environment_name>/bin/activate`

3. Installer, dans cet environnement, le paquet tinydb avec la commande:
- sous Windows: `pip install tinydb`
- sous Linux: `pip3 install tinydb`  

# Exécution
Pour lancer le programme taper la commande: 
- sous Windows: `python main.py`
- sous Linux: `python3 main.py`

# Générer un nouveau fichier flake-html
1. Installer le paquet flake8-html avec la commande:
- sous Windows: `pip install flake8-html`  
- sous Linux: `pip3 install flake8-html`

2. Enregistrer le fichier de configuration dans le répertoire de l'application:

        [flake8]  
        format=html   
        htmldir=<directory_name>  
        max-line-length=120  
        exclude=<environment_name>\Lib  

3. Taper la commande: `flake8 --config=<nom du fichier de configuration>`
