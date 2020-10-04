from managers import ProductManager
from termcolor import colored
from os import system, name 

class Interface:

	def __init__(self):
		self.prod_manage = ProductManager()


	def menu01(self):
		self.running = True
		while self.running:
			choice = input(
				"1 : Toutes les catégories\n"
				"2 : Produits par catégorie\n"
				"3 : Produits par nom\n"
				"4 : Catégories par produit\n"
				"Pour sortir entrez 'q'\n"
				"Votre choix : "
				)
			if choice == '1':
				self.prod_manage.get_all_categories()
				for category in self.prod_manage.list_categories:
					print(
						colored(category[0], 'green'),
						category[1],
						sep= ' : ',
						end=' | '
						)
			elif choice == '2':
				answer = input("Quelle catégorie ?")
				self.prod_manage.get_products_by_category(answer)
				for product in self.prod_manage.list_products_category:
					print(
						product[0],
						colored("Nutriscore = ", 'green'),
						colored(product[1], 'green')
						)
				print("La demande était : ", answer)
			elif choice == '3':
				answer = input("Nom du produit : ")
				self.prod_manage.get_products_by_name(answer)
				for product in self.prod_manage.list_products:
					print(
						product[0],
						colored("Nutriscore = ", 'green'),
						colored(product[1], 'green')
						)
			elif choice == '4':
				answer = input("Nom du produit : ")
				self.prod_manage.get_all_categories_by_product(answer)
				for product in self.prod_manage.list_categories_product:
					print(product)

			elif choice == 'q':
				self.running = False
			else:
				print("Ce choix n'existe pas !")
			

def main():
	test = Interface()
	test.menu01()

if __name__ == "__main__":
    main()