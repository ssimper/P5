"""Création des Managers"""
from database import db

class ProductManager:

	def save_product(self, product):
		pass

	def get_by_id(self, bar_code): #retourne un produit par rapport à un code barre
		rows = db.query("SELECT * FROM product WHERE bar_code='9002515601018'")
		print(rows)

	def get_all_by_category(self, category): #retourne tous les produits par rapport à une catégorie
		pass

	def show_all_products(self, product):
		rows = db.query("SELECT * FROM product")
		for row in rows:
			print(row['name'])


class CategoryManager:

	def save_category(self, category):
		pass

	def show_category(self, category):
		pass

	def get_by_id(self, id):
		pass
