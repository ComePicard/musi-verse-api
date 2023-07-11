# musi-verse-api
Projet d'API pour le site web MusiVerse.
Nécessite une installation de Python (ici 3.10)

py ou python selon l'os ou l'installation

`py -m venv env `

`source env/bin/activate` (Linux)

`.\env\Scripts\Activate.ps1` (Windows)

`pip install -r requirements.txt`

Docker de test :
`docker run --name test -p 5432:5432 -e POSTGRES_PASSWORD=pwd -d postgres`

Une connexion à la DB par un moyen quelconque et : 
`CREATE DATABASE MUSIVERSE_DB`
Dans un terminal en mode administrateur / sudo
`python`
Dans la console python :
`import nltk`
`nltk.download()`
Choisir all et télécharger la data pour l'analyse de sentiment

Quitter le terminal admin
`cd api_musi`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py  createsuperuser --email admin@example.com --username admin`

`python manage.py runserver 8000`

se rendre sur http://127.0.0.1:8000/admin/ et tester admin puis {mot de passe} pour voir si la page d'administration apparaît

