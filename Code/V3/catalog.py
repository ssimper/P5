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
			return self.quit
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
		enumerated_categories = self.prod_manage.classify_categories()
		for a, b, c, d, e in zip(
			enumerated_categories[::5],
			enumerated_categories[1::5],
			enumerated_categories[2::5],
			enumerated_categories[3::5],
			enumerated_categories[4::5]
			):
			print(
				colored(a[0], 'green'), a[1],
				colored(b[0], 'green'), b[1],
				colored(c[0], 'green'), c[1],
				colored(d[0], 'green'), d[1],
				colored(e[0], 'green'), e[1]
				)
		try:
			#We want an integer !!!
			answer = int(input(
				"\nSaisissez le numéro de la catégorie pour afficher" +
				" les sous-catégories : "
				)
			)
		except ValueError:
			print("Saisie incorrecte !")
			return self.display_categories
		else:
			test = [
				item for item in enumerated_categories if item[0] == answer
				]
			if test != []:
				self.display_subcategories(answer)
			else:
				print("Le numéro n'est pas dans la liste !")
				return self.display_subcategories
	


	def display_subcategories(self, category):
		#find the category name from the number answered
		quest = self.prod_manage.classify_categories()[(category-1)][1]
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
		answer = int(input("Votre choix : "))
		self.products_from_selected_subcategory(answer, category)


	def products_from_selected_subcategory(self, subcategory, category):
		#Second : sort the product name from the answer
		quest = self.prod_manage.list_subcategories[(subcategory-1)][1]
		print(f"Les produits associés à la sous-catégorie {quest} sont :")
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
			return self.display_subcategories(category)
		elif answer == "3":
			cat_number = int(input("\nSaisissez le numéro du produit : "))
			self.product_substitution(cat_number)
		else:
			return self.accueil


	def product_substitution(self, cat_number):
		#Find the product bar-code from the list 'list_producs_category'
		quest = self.prod_manage.list_products_category[(cat_number-1)][1][1]
		print("Ma quête : ", quest)
		self.prod_manage.get_products_category_like_by_bar_code(quest)
		print("Le top 6 des aliments partageant le plus de categories :\n")
		for result in self.prod_manage.list_prod_cat_bar:
			print(
				result[0],
				colored(result[2], 'green'),
				"de score : ",
				colored(result[3], 'green')
				)
		answer = int(input(
			"Entrez le numéro du produit que vous souhaitez conserver : ")
			)
		quest = self.prod_manage.list_prod_cat_bar[(answer-1)][1]
		print("Hey ! ", quest)
		self.prod_manage.get_product_description(quest)
		self.prod_manage.get_product_stores(quest)
		info_product = self.prod_manage.list_description
		stores_product = ", ".join(self.prod_manage.list_stores)
		print(
			"Détails du produit sélectionné :\n" +
			info_product[0][0], "\n" +
			"Score : ", info_product[0][1], "\n" +
			"Description du produit :", info_product[0][2], "\n" +
			"Url d'accès au produit : ", info_product[0][3]
			)
		print(
			"Ce produit est disponible dans les magasins suivants :\n" +
			stores_product
			)
		answer = input("Sauvegarder (o/n)")



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