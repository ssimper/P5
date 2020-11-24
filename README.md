## OpenClassRooms, projet 5 : "Utilisez les données publiques de l'OpenFoodFacts".

L'exécution du programme suppose que Python 3 et pipenv sont installés sur votre ordinateur.

Téléchargez les fichiers ici : https://github.com/ssimper/P5/archive/master.zip
- dezippez l'archive 'P5-master.zip'
- Entrez dans le dossier P5-master
- créez une base données dans MySQL : CREATE DATABASE IF NOT EXISTS nom-de-votre-base CHARACTER SET 'utf8mb4' COLLATE ‘utf8mb4_unicode_ci’;
- créez un utilisateur pour cette base de données et placez vous dans votre base de données
- lancez la commande 'USE off_base.sql' pour construire la structure de la base de données
- modifiez les informations du fichier config.py pour qu'elles correspondent à votre base (database, utilisateur, mot de passe)
- éxécutez la commande 'pipenv install' pour paramétrer l'environnement 
- lancez la commande 'python install.py'pour injecter un échantillon de données depuis OpenFoodFacts dans votre base de données.
- démarrez le programme avec la commande python -m catalog

**Le programme.**

Sélectionnez une catégorie puis une sous-catégorie et enfin le produit à substituer.
Si un des substitut proposé vous convient, enregistrez-le !
Vous pourrez ensuite consulter vos produits sauvegardés. 


*English version.*

Program execution assumes that Python 3 and pipenv are installed on your computer.
Download the files from here : https://github.com/ssimper/P5/archive/master.zip
- unzip 'P5-master.zip'
- enter the folder 'P5-master'
- create a MySQL database with the command : CREATE DATABASE IF NOT EXISTS nom-de-votre-base CHARACTER SET 'utf8mb4' COLLATE ‘utf8mb4_unicode_ci’;
- create an user for this database and enter the database
- build the structure of the database with this command : USE off_base.sql
- modify the file config.py with your informations (database, user, password)
- execute 'pipenv install' to configure your environment
- execute 'python install.py' to populate your database with a sample of data from OpenFoodFacts
- run the program with the command: 'python -m -catalog'


**The program.**

Select a category then a subcategory and finally the product to be substituted.
If one of the proposed substitutes suits you, save it!
You can then view your saved products.
