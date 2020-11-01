## OpenClassRooms, projet 5 : "Utilisez les données publiques de l'OpenFoodFacts".

L'exécution du programme suppose que Python 3 et pipenv sont installés sur votre ordinateur.

Téléchargez les fichiers 
- catalog.py (menu du programme qui doit être lancé en premier)
- database.py (informations de connexion à la base)
- fill_database.py (programme d'insertion des données de l'OpenFoodFacts dans la base MySQL)
- managers.py (ensemble des requêtes)
- off_base.sql (structure de la base MySQL)

L'exécution du programme nécessite les bibliothèques suivantes :
- requests
- termcolor
- colorama
- mysql-connector-python

Si vous utilisez pipenv il faut:
* se placer dans le dossier 
* placer la commande 'pipenv install nom_de_la_biliothèque'
* puis la commande 'pipenv shell'

Pour exécuter le programme : `python3 catalog.py`


**Le programme.**

Sélectionnez une catégorie puis une sous-catégorie et enfin le produit à substituer.
Si un des substitut proposé vous convient, enregistrez-le !
Vous pourrez ensuite consulter vos produits sauvegardés. 


*English version.*

Program execution assumes that Python 3 and pipenv are installed on your computer.
Download those files :
- catalog.py (the menu, first file to launch)
- database.py (database informations and credentials)
- fill_database.py (database filling with OpenFooFacts datas)
- managers.py (MySQL requests)
- off_base.sql (MySQL database structure)

Program execution requires the following libraries :
- requests
- termcolor
- colorama

If you use pipenv you must:
* enter the folder
* place the command 'pipenv install library_name'
* then the command 'pipenv shell'

To run the program : `python3 catalog.py`


**The program.**

Select a category then a subcategory and finally the product to be substituted.
If one of the proposed substitutes suits you, save it!
You can then view your saved products.
