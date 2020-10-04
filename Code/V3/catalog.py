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
			colored("Vous souahitez remplacer un aliment.\n", 'yellow') +
			colored("1", 'red') +
			" - Sélectionnez la catégorie\n" +
			colored("2", 'red') +
			" - Retour au menu principal",
			)
		answer = input("Votre choix : ")
		if answer == "1":
			return self.categories
		elif answer == "2":
			return self.accueil
		else:
			return self.product_replace


	def categories(self):
		#Display all categories
		#First : call 'get_all_categories' from managers
		self.prod_manage.get_all_categories()
		#managers return the list of categories 'list_categories'
		for category in self.prod_manage.list_categories:
			print(
				colored(category[0], 'green'),
				category[1],
				sep = ' : ',
				end =' | '
				)
		#We want an integer !!!
		answer = int(input("\nSaisissez le numéro de la catégorie : "))
		#Second : sort the product name from the answer
		quest = self.prod_manage.list_categories[(answer-1)][1]
		#Third : call 'get_products_by_category' with quest parameter
		self.prod_manage.get_products_by_category(quest)
		#managers return  the list of products 'list_products'
		print(self.prod_manage.list_products_category)
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
			" - Sélectionnez l'aliment à substituer\n" +
			colored("3", 'red') +
			" - Retour au menu principal"
			)
		answer = input("Votre choix : ")
		if answer == "1":
			return self.categories
		elif answer == "2":
			cat_number = int(input("\nSaisissez le numéro de la catégorie : "))
			quest = self.prod_manage.list_products_category[(cat_number-1)][1][1]
			print(quest)
			return self.products
		else:
			return self.accueil


	def product_from_number(self, product_number):
		self.product_number = product_number	
		pass

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