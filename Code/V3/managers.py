"""Création des Managers"""
from database import db, cnx

class ProductManager:

	def __init__(self):
		self.list_categories = list()
		self.list_products_category = list()
		self.list_products = list()
		self.list_categories_product = list()

	def save_product(self, product):
		pass

	def get_by_id(self, bar_code): #retourne un produit par rapport à un code barre
		rows = db.query("SELECT * FROM product WHERE bar_code='9002515601018'")
		print(rows)

	def get_products_by_name(self, product):
		cursor = cnx.cursor()
		query01 = """
			SELECT
    		    DISTINCT product.name,nutriscore.name as nutriscore
    		FROM
    		    product
    		INNER JOIN
    			nutriscore
    		ON
    			product.nutriscore_id = nutriscore.id
    		WHERE
    		    product.name LIKE CONCAT ('%', %s, '%') 
    		ORDER BY
    		    nutriscore.name

    		"""
		p = product
		cursor.execute(query01, (p,))
		results = cursor.fetchall()
		#Cleaning the list
		self.list_products = []
		for result in results:
			self.list_products.append((result[0], result[1]))
		return self.list_products


	def get_all_categories(self):
		cursor = cnx.cursor()
		cursor.execute(
			"""
			SELECT
				*
			FROM
				category
			"""
			)
		results = cursor.fetchall()
		#Cleaning the list
		self.list_categories = []
		#Filling self.list_categories with values
		for result in results:
			self.list_categories.append(result[1])
		return self.list_categories

	def get_products_by_category(self, category): #retourne tous les produits par rapport à une catégorie
		cursor = cnx.cursor()
		query01 = """
			SELECT
				DISTINCT product.name,nutriscore.name as nutriscore
			FROM
				product
			INNER JOIN
				product_category
			ON
				product.bar_code = product_category.product_bar_code
			INNER JOIN
				category
			ON
				product_category.category_id = category.id
			INNER JOIN
				nutriscore
			ON
				product.nutriscore_id = nutriscore.id
			WHERE
				category.name LIKE CONCAT ('%', %s, '%')
			ORDER BY
				nutriscore.name;
			"""
		p = category
		cursor.execute(query01, (p,))
			
		results = cursor.fetchall()
		#Cleaning the list
		self.list_products_category = []
		#Filling the list
		for result in results:
			self.list_products_category.append((result[0], result[1]))
		return self.list_products_category

	def get_all_categories_by_product(self, product):
		cursor = cnx.cursor()
		query01 = """
			SELECT
				DISTINCT category.name
			FROM
				category
			INNER JOIN
				product_category
			ON
				category.id = product_category.category_id
			INNER JOIN
				product
			ON
				product_category.product_bar_code = product.bar_code
			WHERE
				product.name LIKE CONCAT ('%', %s, '%')
			"""
		p = product
		cursor.execute(query01, (p,))
		results = cursor.fetchall()
		#cleaning the list
		self.list_categories_product = []
		#filling the list
		for result in results:
			self.list_categories_product.append(result[0])
		return self.list_categories_product




	def show_all_products():
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

def main():
    """Instantiation and starting the program."""
    test_category = ProductManager()
    answer = input("Une catégorie ?")
    test_category.get_all_by_category(answer)


if __name__ == "__main__":
    main()