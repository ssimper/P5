"""Module for the menu which help the user to find the substitute."""

from termcolor import colored
import colorama

import config
from .managers import ProductManager

colorama.init()


class TheMenu:
    """Class reponsible of the display of each submenus to help the user
    to find the original produ and its substitute."""

    def __init__(self):
        """Definition of the next attribute and instantiation of 
        ProductManager's class."""
        self.next = self.welcome
        self.prod_manage = ProductManager()

    def start(self):
        """Definition of the running status of the programme and loop which
        define the next methode to run."""
        self.running = True
        while self.running:
            self.next = self.next()

    def welcome(self):
        """First menu"""
        print(
            colored("Accueil\n", 'yellow') +
            colored("1", 'red') +
            " - Quel aliment souhaitez-vous remplacer ?\n" +
            colored("2", 'red') +
            " - Retrouver mes aliments substitués.\n" +
            colored("3", 'red') +
            " - Sortir"
        )
        answer = input("Votre choix : ")
        if answer == "1":
            return self.product_replace
        elif answer == "2":
            return self.stored_product
        elif answer == "3":
            return self.quit
        else:
            return self.welcome

    def product_replace(self):
        """Menu to choose a category"""
        print(
            colored("Vous souhaitez remplacer un aliment.\n", 'yellow') +
            colored("1", 'red') +
            " - Sélectionnez la catégorie\n" +
            colored("2", 'red') +
            " - Retour au menu principal",
        )
        answer = input("Votre choix : ")
        if answer == "1":
            return self.display_categories
        elif answer == "2":
            return self.welcome
        else:
            return self.product_replace

    def display_categories(self):
        """Method responsible for displaying the chosen categories"""
        #Here we use 'zip' ton organize the display of the results
        #in 8 columns
        enumerated_categories = self.prod_manage.classify_categories()
        for i, category in enumerated_categories:
            print(
                colored(i, "green"), category,
                end=" " if i % 8 else "\n"
            )
       
        # We check the answer
        try:
            # We want an integer !!!
            category_number = int(input(
                "\nSaisissez le numéro de la catégorie pour afficher" +
                " les sous-catégories : "
            )
            )
        except ValueError:
            # The answer is not an integer
            print("Saisie incorrecte !")
            input("Appuyez sur 'Entrée' pour continuer.")
            return self.display_categories
        else:
            # Is the answer in the list of categories ?
            test = [
                item
                for item in enumerated_categories
                if item[0] == category_number
            ]
            if test != []:
                # The answer is in the list
                self.last_category_number = category_number
                return self.display_subcategories
            else:
                # The answer is not in the list
                print("Le numéro n'est pas dans la liste !")
                input("Appuyez sur 'Entrée' pour continuer.")
                return self.display_categories

    def display_subcategories(self):
        """Method responsible for displaying the chosen subcategories"""
        # find the category name from the number answered
        quest = self.prod_manage.classify_categories()[(
            self.last_category_number-1
        )][1]
        print(f"\nLes sous-catégory de {quest} sont :")
        self.prod_manage.get_subcategories_from_categories(quest)
        list_cat = self.prod_manage.list_subcategories
        for cat in list_cat:
            print(
                colored(cat[0], 'green'),
                cat[1],
                sep=' : ',
                end=' | '
            )
        print("\n\nDe quelle sous-catégorie souhaitez-vous extraire " +
              "les produits ?")
        # We check the answer
        try:
            sub_category_number = int(input("Votre choix : "))
        except ValueError:
            # The answer is not an integer
            print("Saisie incorrecte !")
            input("Appuyez sur 'Entrée' pour continuer.")
            return self.display_subcategories
        else:
            #The answer is an integer, is-it in the list ?
            test = [
                item
                for item in list_cat
                if item[0] == sub_category_number
            ]
            if test != []:
                # The answer is in the subcategories list.
                self.last_sub_category_number = sub_category_number
                return self.products_from_selected_subcategory
            else:
                # The answer is not in the list.
                print("Le numéro n'est pas dans la liste !")
                input("Appuyez sur 'Entrée' pour continuer.")
                return self.display_subcategories

    def products_from_selected_subcategory(self):
        """ Method which find products matching with the selecter 
        sub category"""
        # sort the product name from the answer
        quest = self.prod_manage.list_subcategories[(
            self.last_sub_category_number-1
        )][1]
        print(
            "Les produits associés à la sous-catégorie",
            colored(quest, 'yellow'),
            "sont :"
        )
        # call 'get_products_by_category' with quest parameter
        self.prod_manage.get_products_by_category(quest)
        # managers return  the list of products 'list_products'
        for result in self.prod_manage.list_products_category:
            print(
                colored(result[0], 'green'), # Product number
                colored(result[1][0], 'yellow'), # Product name
                " score :",
                colored(result[1][2], 'yellow'), # Product score
                end="\n"
            )
        print(
            colored("1", 'red') +
            " - Sélectionne une autre catégorie ?\n" +
            colored("2", 'red') +
            " - Sélectionne une autre sous-catégorie ?\n" +
            colored("3", 'red') +
            " - Sélectionnez l'aliment à substituer\n" +
            colored("4", 'red') +
            " - Retour au menu principal"
        )
        answer = input("Votre choix : ")
        if answer == "1":
            return self.display_categories
        elif answer == "2":
            return self.display_subcategories
        elif answer == "3":
            for result in self.prod_manage.list_products_category:
                # Display one more time the products
                print(
                    colored(result[0], 'green'), # Product number
                    colored(result[1][0], 'yellow'), # Product name
                    " score :",
                    colored(result[1][2], 'yellow'), # Product score
                    end="\n"
                )
            # We check the answer
            try:
                product_to_substitute = int(input(
                    "Saisissez le numéro de l'aliment à substituer : "
                ))
            except ValueError:
                # The answer is not an integer
                print("Saisie incorrecte !")
                input("Appuyez sur 'Entrée' pour continuer.")
                return self.products_from_selected_subcategory
            else:
                # The answer is an integer, is it in the list ?
                test = [
                    item
                    for item in self.prod_manage.list_products_category
                    if item[0] == product_to_substitute
                ]
            if test != []:
                # The answer is in the list.
                self.last_product_to_substitute = product_to_substitute
                return self.product_substitution
            else:
                # The answer is not in the list.
                print("Le numéro n'est pas dans la liste !")
                input("Appuyez sur 'Entrée' pour continuer.")
                return self.products_from_selected_subcategory

        elif answer == "4":
            return self.welcome
        else:
            return self.products_from_selected_subcategory

    def product_substitution(self):
        """Method responsible for the search of products which have many
        categories in common but with better nutriscore"""
        # Find the product bar-code from the list 'list_producs_category'
        old_product_bar_code = self.prod_manage.list_products_category[(
            self.last_product_to_substitute-1
        )][1][1]
        old_product_name = self.prod_manage.list_products_category[(
            self.last_product_to_substitute-1
        )][1][0]
        old_product_score = self.prod_manage.list_products_category[(
            self.last_product_to_substitute-1
        )][1][2]
        #Call the method which find products which have categories in common
        #with the selected product
        self.prod_manage.get_products_category_like_by_bar_code(
            old_product_bar_code
        )
        categories_match = len(self.prod_manage.list_prod_cat_bar)
        if categories_match == 0:
            # No products found.
            print("Pas de substitut pour ce produit ...")
            return self.welcome
        else:
            # Products found.
            print(
                "Le top",
                categories_match,
                "des aliments partageant le plus de categories avec ",
                colored(old_product_name, 'yellow'),
                "de score",
                colored(old_product_score, 'red'),
                "sont :"
            )
            for result in self.prod_manage.list_prod_cat_bar:
                print(
                    result[0], # Product number
                    colored(result[2], 'green'), # Product name
                    "de score : ",
                    colored(result[3], 'green') # Product score
                )
        # We check the answer
        try:
            answer = int(input(
                "Entrez le numéro du produit que vous souhaitez conserver : "
            )
            )
        except ValueError:
            # The answer is not an integer
            print("Saisie incorrecte !")
            input("Appuyez sur 'Entrée' pour continuer.")
            return self.product_substitution
        else:
            # Is the answer in the list ?
            test = [
                item
                for item in self.prod_manage.list_prod_cat_bar
                if item[0] == answer
            ]
        if test != []:
            # The answer is in the list.
            self.last_answer = answer
            self.old_product_bar_code = old_product_bar_code
            return self.save_product
        else:
            # the answer is not in the list.
            print("Le numéro n'est pas dans la liste !")
            input("Appuyez sur 'Entrée' pour continuer.")
            return self.product_substitution

    def save_product(self):
        """Method responsible for displaying information about the substitute
        and recording it in the database."""
        # Find the the bar-code of the new product.
        new_product = self.prod_manage.list_prod_cat_bar[(
            self.last_answer-1
        )][1]
        # Get the new product description.
        self.prod_manage.get_product_description(new_product)
        # Get the new product stores.
        self.prod_manage.get_product_stores(new_product)
        info_product = self.prod_manage.list_description
        info_product_name = info_product[0][0]
        info_product_score = info_product[0][1]
        # If the new product doesn't have description we put e default one
        if info_product[0][2] == '':
            info_product_description = "(pas de description)"
        else:
            info_product_description = info_product[0][2]
        info_product_url = info_product[0][3]
        stores_product = ", ".join(self.prod_manage.list_stores)
        print(
            "Détails du produit sélectionné :" +
            # New product name.
            colored(info_product_name, 'yellow') +
            # New product score.
            " (Score : ", colored(info_product_score, 'yellow'), ")\n" +
            "Description du produit :",
            # New product description.
            colored(info_product_description, 'yellow'), "\n" +
            "Url d'accès au produit : ",
            # New product url.
            colored(info_product_url, 'yellow')
        )
        print(
            "Ce produit est disponible dans les magasins suivants :\n" +
            # New product stores.
            colored(stores_product, 'yellow')
        )
        print(
            colored("1", 'red') +
            " - Enregistrer le produit dans votre historique\n" +
            colored("2", 'red') +
            " - Choisir un autre produit de la même catégorie\n" +
            colored("3", 'red') +
            " - Retour au menu principal\n" +
            colored("4", 'red') +
            " - Quitter"
        )
        answer = input("Votre choix : ")
        if answer == "1":
            self.prod_manage.record_product(
                self.old_product_bar_code,
                new_product
            )
            return self.welcome
        elif answer == "2":
            return self.product_substitution
        elif answer == "3":
            return self.welcome
        elif answer == "4":
            return self.quit
        else:
            return self.save_product
        return self.welcome

    def stored_product(self):
        """ Method responsible for displaying recorded substitutes from the
        database."""
        print("Voici la liste de vos produits de substitution :\n")
        # Get the list of stored products.
        self.prod_manage.list_stored_product()
        save_product = self.prod_manage.list_saved_product
        for product in save_product:
            # The original product is the first element of the tuple.
            print(
                "Produit d'origine", colored(product[0][0], 'red'), "\n" +
                "Description :", product[0][1] +
                " de score :", colored(product[0][2], 'red'), "\n" +
                "Remplacé par :"
            )
            i = 0
            # The second element of the tuple is a liste of substitutes 
            while i < len(product[1]):
                # Check if the list is empty.
                if i > 0:
                    # The list is not empty we use 'or' to separate substitues
                    print(" ou")
                print(
                    # Substitute name.
                    colored(product[1][i][0], 'green'), "\n" +
                    # Substitute description.
                    "Description :", product[1][i][1] +
                    # Substitute score
                    " de score :", colored(product[1][i][2], 'green')
                )
                i += 1
            print("-----------------------")
        print(
            colored("1", 'red') +
            " - Retour au menu principal\n" +
            colored("2", 'red') +
            " - Quitter"
        )
        answer = input("Votre choix : ")
        if answer == "1":
            return self.welcome
        elif answer == "2":
            return self.quit
        else:
            return self.stored_product

    def products(self):
        """ Method responsible for diplaying all products."""
        self.prod_manage.get_all_products()
        for product in self.prod_manage.list_products:
            print(
                colored(product[0], 'green'),
                product[1][0],
                sep=' : ',
                end=' | '
            )
        answer = input("\nSaisissez le numéro du produit : ")
        if answer == "1":
            return self.categories
        elif answer == "2":
            return self.quit
        else:
            return self.welcome

    def quit(self):
        print("Menu Quitter, au revoir !")
        self.running = False