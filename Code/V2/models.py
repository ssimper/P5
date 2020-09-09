"""Création des modèles pour chaque tables"""

class Category:

	def __init__(self, name, id=None):
		self.id = id
		self.name = name

class Nutriscore:

	def __init__(self, name, id=None):
		self.id = id
		self.name = name

class Product:

	def __init__(self, bar_code, name, nutriscore_id):
		self.id = id
		self.bar_code = bar_code
		self.name = name
		self.nutriscore_id = nutriscore_id

class Store:

	def __init__(self, name, id=None):
		self.id = id
		self.name = name

class ProductCategory:

	def __init__(self, id, product_bar_code, category_id):
		self.id = id
		self.product_bar_code = product_bar_code
		self.category_id = category_id

class ProductStore:

	def __init__(self, product_bar_code, store_id):
		self.id = id
		self.product_bar_code = product_bar_code
		self.store_id = store_id

"""Exemple d'instenciation """

#manager = ProductManager()
#manager.save_product(mon_produit)