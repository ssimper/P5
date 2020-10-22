from managers import ProductManager
from termcolor import colored

class TheMenu:


	def __init__(self):
		self.next = self.accueil
		self.prod_manage = ProductManager()


	def start(self):
		self.running = True
		while self.running:
			self.next = self.next()


	def accueil(self):
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
			return self.accueil


	def product_replace(self):
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
			return self.accueil
		else:
			return self.product_replace


	def display_categories(self):
		enumerated_categories = []
		enumerated_categories = self.prod_manage.classify_categories()
		for a, b, c, d, e, f in zip(
			enumerated_categories[::6],
			enumerated_categories[1::6],
			enumerated_categories[2::6],
			enumerated_categories[3::6],
			enumerated_categories[4::6],
			enumerated_categories[5::6]
			):
			print(
				colored(a[0], 'green'), a[1],
				colored(b[0], 'green'), b[1],
				colored(c[0], 'green'), c[1],
				colored(d[0], 'green'), d[1],
				colored(e[0], 'green'), e[1],
				colored(f[0], 'green'), f[1]
				)
		try:
			#We want an integer !!!
			category_number = int(input(
				"\nSaisissez le numéro de la catégorie pour afficher" +
				" les sous-catégories : "
				)
			)
		except ValueError:
			print("Saisie incorrecte !")
			input("Appuyez sur 'Entrée' pour continuer.")
			return self.display_categories
		else:
			test = [
				item
				for item in enumerated_categories
				if item[0] == category_number
				]
			if test != []:
				self.last_category_number = category_number
				return self.display_subcategories
			else:
				print("Le numéro n'est pas dans la liste !")
				input("Appuyez sur 'Entrée' pour continuer.")
				return self.display_categories
	


	def display_subcategories(self):
		#find the category name from the number answered
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
				sep = ' : ',
				end = ' | '
				)
		print("\n\nDe quelle sous-catégorie souhaitez-vous extraire " +
			"les produits ?")
		try:
			sub_category_number = int(input("Votre choix : "))
		except ValueError:
			print("Saisie incorrecte !")
			input("Appuyez sur 'Entrée' pour continuer.")
			return self.display_subcategories
		else:
			test = [
				item
				for item in list_cat
				if item[0] == sub_category_number
				]
			if test != []:
				self.last_sub_category_number = sub_category_number
				return self.products_from_selected_subcategory
			else:
				print("Le numéro n'est pas dans la liste !")
				input("Appuyez sur 'Entrée' pour continuer.")
				return self.display_subcategories


	def products_from_selected_subcategory(self):
		#Second : sort the product name from the answer
		quest = self.prod_manage.list_subcategories[(
			self.last_sub_category_number-1
			)][1]
		#print(f"Les produits associés à la sous-catégorie {quest} sont :")
		print(
			"Les produits associés à la sous-catégorie",
			 colored(quest, 'yellow'),
			 "sont :"
			 )
		#Third : call 'get_products_by_category' with quest parameter
		self.prod_manage.get_products_by_category(quest)
		#managers return  the list of products 'list_products'
		for result in self.prod_manage.list_products_category:
			print(
				colored(result[0], 'green'),
				colored(result[1][0], 'yellow'),
				" score :",
				colored(result[1][2], 'yellow'),
				end = "\n" 
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
				print(
					colored(result[0], 'green'),
					colored(result[1][0], 'yellow'),
					" score :",
					colored(result[1][2], 'yellow'),
					end = "\n" 
					)
			try:
				product_to_substitute = int(input(
				"Saisissez le numéro de l'aliment à substituer : "
				))
			except ValueError:
				print("Saisie incorrecte !")
				input("Appuyez sur 'Entrée' pour continuer.")
				return self.products_from_selected_subcategory
			else:
				test = [
				item
				for item in self.prod_manage.list_products_category
				if item[0] == product_to_substitute
				]
			if test != []:
				self.last_product_to_substitute = product_to_substitute
				return self.product_substitution				
			else:
				print("Le numéro n'est pas dans la liste !")
				input("Appuyez sur 'Entrée' pour continuer.")
				return self.products_from_selected_subcategory
				#return self.display_subcategories
			
		elif answer == "4":
			return self.accueil
		else:
			return self.products_from_selected_subcategory

	def product_substitution(self):
		#Find the product bar-code from the list 'list_producs_category'
		old_product_bar_code = self.prod_manage.list_products_category[(
			self.last_product_to_substitute-1
			)][1][1]
		old_product_name = self.prod_manage.list_products_category[(
			self.last_product_to_substitute-1
			)][1][0]
		old_product_score = self.prod_manage.list_products_category[(
			self.last_product_to_substitute-1
			)][1][2] 
		self.prod_manage.get_products_category_like_by_bar_code(
			old_product_bar_code
			)
		categories_match = len(self.prod_manage.list_prod_cat_bar)
		if categories_match == 0:
			print("Pas de substitut pour ce produit ...")
			return self.accueil
		else:
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
					result[0],
					colored(result[2], 'green'),
					"de score : ",
					colored(result[3], 'green')
					)
		try:
			answer = int(input(
				"Entrez le numéro du produit que vous souhaitez conserver : "
				)
			)
		except ValueError:
				print("Saisie incorrecte !")
				input("Appuyez sur 'Entrée' pour continuer.")
				return self.product_substitution
		else:
			test = [
			item
			for item in self.prod_manage.list_prod_cat_bar
			if item[0] == answer 
			]
		if test != []:
			self.last_answer = answer
			self.old_product_bar_code = old_product_bar_code
			return self.save_product			
		else:
			print("Le numéro n'est pas dans la liste !")
			input("Appuyez sur 'Entrée' pour continuer.")
			return self.product_substitution
	

	def save_product(self):
		new_product = self.prod_manage.list_prod_cat_bar[(
			self.last_answer-1
			)][1]
		self.prod_manage.get_product_description(new_product)
		self.prod_manage.get_product_stores(new_product)
		info_product = self.prod_manage.list_description
		info_product_name = info_product[0][0]
		info_product_score = info_product[0][1]
		if info_product[0][2] == '':
			info_product_description = "(pas de description)"
		else:
			info_product_description = info_product[0][2]
		info_product_url = info_product[0][3]
		stores_product = ", ".join(self.prod_manage.list_stores)
		print(
			"Détails du produit sélectionné :" +
			colored(info_product_name, 'yellow') +
			" (Score : ", colored(info_product_score, 'yellow'), ")\n" +
			"Description du produit :",
			colored(info_product_description, 'yellow'), "\n" +
			"Url d'accès au produit : ",
			colored(info_product_url, 'yellow')
			)
		print(
			"Ce produit est disponible dans les magasins suivants :\n" +
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
			return self.accueil
		elif answer == "2":
			return self.product_substitution
		elif answer == "3":
			return self.accueil
		elif answer == "4":
			return self.quit
		else:
			return self.save_product
		return self.accueil

	
	def stored_product(self):
		print("Voici la liste de vos produits de substitution :\n")
		self.prod_manage.list_stored_product()
		save_product = self.prod_manage.list_saved_product
		for product in save_product:
			print(
				"Produit d'origine", colored(product[0][0], 'red'), "\n" +
				"Description :", product[0][1] +
				" de score :", colored(product[0][2], 'red'), "\n" +
				"Remplacé par :"
				)
			i = 0
			while i < len(product[1]):
				if i > 0:
					print(" ou")
				print(
					colored(product[1][i][0], 'green'), "\n" +
					"Description :", product[1][i][1] +
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
			return self.accueil
		elif answer =="2":
			return self.quit
		else:
			return self.stored_product




	
	def products(self):
		self.prod_manage.get_all_products()
		for product in self.prod_manage.list_products:
			print(
				colored(product[0], 'green'),
				product[1][0],
				sep= ' : ',
				end=' | '
				)
		answer = input("\nSaisissez le numéro du produit : ")
		if answer == "1":
			return self.categories
		elif answer == "2":
			return self.quit
		else:
			return self.accueil

	
	def quit(self):
		print("Menu Quitter, au revoir !")
		self.running = False


	
def main():
	test = TheMenu()
	test.start()

if __name__ == "__main__":
    main()