# Stage 2019-2020 LPRGI - Homéo

Homéo est un outil open-source permettant la gestion d'un parc locatif pour les propriétaires et proposer une plateforme de contact entre propriétaires et locataires

  - Permet la gestion d'un Immeuble/Bien/Bail
  - Génération automatique des quittances de loyers
  - Verification des retards

# Installation

## prérequis

Afin d'installer le projet, vous devez tout d'abord installer python 2.7 ainsi que pip

Installation de pip :
```sh
    $ sudo apt update
    $ sudo apt install python-pip
    $ pip --version
```

Maintenant vous devez installer les dépendances suivantes avec la commande pip install
  - flask
  - requests
  - peewee
  - flask-login
  - wtforms
  - flask-wtf
  - flask-mail
  - reportlab
  - pbkdf2
  - pdfkit
  - flask-restful
  - itsdangerous



## Installation du projet
Créer un nouveau virtualhost dans le directory d'apache2 avec le code suivant en prennant le temps de remplacer les XXXXXXXX par vos valeurs personnelles 

```sh
<VirtualHost *:80>
                ServerName XXXXXXXX 
                ServerAdmin XXXXXXXX
		DocumentRoot "/var/www/vhosts/XXXXXXXX"
		ServerAlias XXXXXXXX

                WSGIScriptAlias / /var/www/vhosts/XXXXXXXX/webapp.wsgi
                <Directory /var/www/vhosts/XXXXXXXX/webApp/>
                        Require all granted
                        Allow from all
                </Directory>
                Alias /static /var/www/vhosts/XXXXXXXX/webApp/static
                <Directory /var/www/vhosts/XXXXXXXX/webApp/static/>
                        Require all granted
                        Allow from all
                </Directory>
                <Directory /var/www/vhosts/XXXXXXXX/webApp/static/css/images>
                        Require all granted
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
Taper la commande suivante afin d'activer le site
```sh
    a2ensite nomDeVotreFichier.conf
```

Dans le repertoire /var/www créez un nouveau directory pour tout vos virtualhost.
Dans celui-ci créez un nouveau directory portant le nom du projet.
Dans ce même directory créez un nouveau fichier webapp.wsgi et collez-y le code suivant tout en modifiant les XXXXX et la secret_key

```sh
    #!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/vhosts/XXXXXX/")

from webApp import app as application
application.secret_key = 'Add your secret key'
```

Dans le directory crée précédemment, créez un directory nommé webApp. 

Ici vous pouvez effectuer un clone du projet.

Avant de pouvoir lancer votre site, allez dans le fichier models.py et modifiez la ligne suivante avec le lien absolu donnant l'accès à la base de données SQLITE.

```sh
    database = SqliteDatabase("/var/www/vhosts/XXXXXXXX/webApp/database.sqlite3")
```

Vous pouvez maintenant relancer Apache sur votre serveur avec la commande 

```sh
    systemctl restart apache2
```

# En cas de problème
  - vérifiez qu'apache ait l'accès au dossier du projet
  - verifiez les droits d'accès à la base de données
  - Pensez à verifier les log apache dans le fichier error.log situé dans le repertoire var/log/apache2
  - En cas de problème autre, envoyez un mail de contact sur l'adresse kevin.leleu.pro@gmail.com






