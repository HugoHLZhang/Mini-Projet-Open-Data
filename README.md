# Description

À partir de Dataset Pokémon, OULLAI Oussama et moi-même avons réalisé un dashboard sur Pokémon. 

# Installation
Si ce n'est pas déjà fait, installer Python et Git sur sa machine :

- Pour Python, effectuer le téléchargement de la dernière version stable depuis [ce lien](https://www.python.org/downloads/windows/) puis
suivre le tutoriel [ici](https://perso.esiee.fr/~courivad/Python/install/python.html) afin de finaliser l'installation de Python : 

- Pour Git, télécharger la version correspondante (32 ou 64 bits) sur [cette page web](https://git-scm.com/download/win).


Instruction pour cloner le projet sur sa machine personnelle :

    git clone https://git.esiee.fr/zhanhu/mini-projet-open-data.git

Se placer dans le répertoire du projet :

> sur Git Bash :

    cd mini-projet-open-data/
    
> sur Windows PowerShell :

    cd .\mini-projet-open-data\

La liste des packages additionnels sont dans le fichier **requirements.txt** contenant les packages à installer.
Si nécessaire, faire une mise à jour du pip : 

    python.exe -m pip install --upgrade pip
    
Instruction pour installer ces packages :

    python -m pip install -r requirements.txt

# Démarrage

Instruction à exécuter dans le terminal pour lancer le projet :

    python main.py

Cette application est lancée dans une console :

    $ python main.py 
    Dash is running on http://127.0.0.1:8050/

    * Serving Flask app 'main' (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on

Et le résultat s’observe dans la fenêtre d’un navigateur à l’adresse indiquée dans la console (ici http://127.0.0.1:8050/)

![PokéData !](/images/dashboard.PNG "PokéData Dashboard")

# Utilisation

> **Conseil : Adaptez le zoom de votre fenêtre pour bien visualiser le dashboard ou la partie qui vous intéresse** 

Le PokéData Dashboard comporte 3 compléments : 

> **La Carte**
 
La carte vous permet de visualiser toutes les régions des jeux Pokémon qui ont été inspirés de vrais régions et pays dans le monde. Plusieurs cartes sont à disposition. Vous retrouverez tous les pokémons en fonction de leur région, de leur premier type ou de leur second type.<br> _Cliquez sur les légendes, elles peuvent être filtrées._

![La Carte !](/images/carte.PNG "PokéData Carte")

> **Les Types**

L'histogramme vous montre le nombre de premiers type identiques et de seconds type identiques. Vous pourrez observer deux histogramme et obtenir les informations que vous souhaitez.<br>
_Cliquez sur les légendes, elles peuvent être filtrées._

![Les Types !](/images/types.PNG "PokéData Types")

> **Le Pokédex**

Ici, vous avez un Pokédex en cours de développement. Le Professeur Chen nous a demandé de créer le Pokédex le plus complet du monde. Voici ce que notre Pokédex peut faire : 

- Comparer les statistiques des Pokémons entre eux
- Choisir les Pokémons à comparer
- Connaître leurs numéros de Pokédex National, leurs types et leurs statistiques de base
- Visualiser leurs images et sprites de jeux 
- Savoir de quelle région vient le Pokémon

![Le Pokédex !](/images/pokedex.PNG "PokéData Pokédex")

# Architecture du code

![Architecture !](/images/architecture.svg "PokéData Architecture")

# Copyright

Je déclare sur l'honneur que le code fourni a été produit par nous même.
