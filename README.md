# Bienvenue sur le site de la cantine Lo Garric

## Technos utilisées

+ HTML, CSS
+ Bootstrap
+ Python, flask

## Pour lancer le site web :

export FLASK_APP=main  
flask run

Il est nécessaire de posséder les modules *pandas*, *flask*, *flask_login* et *flask_bcrypt*

## Comptes
Voici plusieurs comptes pour jouer avec la base de données

Admin  
identifiant : admin  
MDP : admin

Enseignant  
identifiant : jneymar  
MDP : jneymar

Representant  
identifiant : gartalle  
MDP : test

Il y a d'autres comptes disponibles dans /documents/cantine.sql

## Date du jour
Il est possible de changer la date actuelle  
avec la fonction choixDate() ligne 96 dans le main.py afin de faire des tests sur une année scolaire (Aout/Année N - Juillet/Année N+1 )