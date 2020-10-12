"""Création des Managers"""
from database import db, cnx

class ProductManager:

	def __init__(self):
		self.dict_categories = dict()
		self.list_categories = list()
		self.list_products_category = list()
		self.list_products = list()
		self.list_categories_product = list()
		self.set_classified_categories = set()
		self.list_classified_categories = list()
		self.list_sub_categories = list()
		self.list_enumerated_categories = list()
		self.list_description = list()

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


	def get_product_description(self, bar_code):
		"""Find all information the customer needs about his new product"""
		cursor = cnx.cursor()
		query01 = """
			SELECT
				DISTINCT
					product.name,
					nutriscore.name,
					product.description,
					product.url
			FROM
				product
			INNER JOIN
				nutriscore
			ON
				product.nutriscore_id = nutriscore.id
			INNER JOIN
				product_category
			ON
				product.bar_code = product_category.product_bar_code
			INNER JOIN
				category
			ON
				product_category.category_id = category.id
			WHERE
				product.bar_code = %s
			"""
		p = bar_code
		cursor.execute(query01, (p,))
		results = cursor.fetchall()
		self.list_description = []
		self.list_description = results
		return self.list_description


	def get_product_stores(self, bar_code):
		"""Find the store where the product is referenced. We need the 
		store id for saving the product."""
		cursor = cnx.cursor()
		query01 = """
			SELECT
				store.name, store.id
			From
				store
			INNER JOIN
				product_store
			ON
				store.id = product_store.store_id
			WHERE
				product_store.product_bar_code = %s
		"""
		p = bar_code
		cursor.execute(query01, (p,))
		results = cursor.fetchall()
		#List with store name and store id
		self.list_stores_tuples = []
		#List with just store name
		self.list_stores = []
		self.list_stores_tuples = results
		#Put store name in self.list_store from self.list_stores_tuples
		for i, store in enumerate(self.list_stores_tuples):
			self.list_stores.append(self.list_stores_tuples[i][0])
		return self.list_stores
		pass
		


	def classify_categories(self):
		"""Get all items from 'category' tables, add the tuple to the
		collection if its second element hasn't the first fourth caracters
		in common with tuple(s) allready in the collection. Finally put all 
		those items in a list ordered and numbered."""
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
		self.list_categories = []
		#Put the result of the query in a list.
		for result in results:
			#category with the same fourth first caracters are not added
			item_in = [item
				for item in self.list_categories
				if result[1][:4] in item[1][:4]
				]
			if item_in != []:
				continue
			else:
				self.list_categories.append(result)
		#Extract the first word of the second element of the list of tuple
		#and put it in a set to avoid duplicates 
		for i, element in enumerate(self.list_categories):
			self.set_classified_categories.add(
				(self.list_categories[i][1].split(" "))[0]
				)
		#Browse the collection in ordered way and put its items in a numerate 
		#list
		for i, category in enumerate(
			sorted(self.set_classified_categories), start = 1
			):
			self.list_enumerated_categories.append((i, category))
		return self.list_enumerated_categories


	def get_subcategories_from_categories(self, category):
		"""Get categories which names start like the sub-category name"""
		cursor = cnx.cursor()
		query01 = """
			SELECT
				*
			FROM
				category
			WHERE
				name LIKE CONCAT (%s, '%')
			"""
		p = category
		cursor.execute(query01, (p,))
		results = cursor.fetchall()
		self.list_subcategories = []
		for i, result in enumerate(results, start = 1):
			self.list_subcategories.append((i, result[1]))
		return self.list_subcategories


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
		self.list_categories = []
		for i, result in enumerate(results, start = 1):
			self.list_categories.append((i, result[1]))
		return self.list_categories


	def get_all_products(self):
		cursor = cnx.cursor()
		cursor.execute(
			"""
			SELECT
				name
			FROM
				product
			"""
			)
		results = cursor.fetchall()
		self.list_products = []
		for i, result in enumerate(results, start = 1):
			self.list_products.append((i, result))
		return self.list_products


	def get_products_category_like_by_bar_code(self, bar_code):
		"""Find the products that have the most category in common
		with the initial product."""
		cursor = cnx.cursor()
		query03 = """
			SELECT
				product_bar_code,
				product.name,
				nutriscore.name,
				COUNT(category_id) AS nombre_categorie
			FROM
				product_category
			INNER JOIN
				product
			ON
				product_category.product_bar_code = product.bar_code
			INNER JOIN
				nutriscore
			ON
				product.nutriscore_id = nutriscore.id
			WHERE
				product_bar_code != %s
			AND
				category_id
			IN
				(
				SELECT
					category_id
				FROM
					product_category
				WHERE
					product_bar_code = %s
				)
			GROUP BY
				product_bar_code
			ORDER BY
				nombre_categorie
			DESC LIMIT 6;
			"""
		p = bar_code
		print(p)
		cursor.execute(query03, (p,p))
		results = cursor.fetchall()
		#cleaning the list
		self.list_prod_cat_bar = []
		#Filing the list
		for i, result in enumerate(results, start = 1):
			self.list_prod_cat_bar.append(
				(i, 
				result[0],
				result[1],
				result[2],
				result[3]
				)
			)
		return self.list_prod_cat_bar

		pass

	def get_products_by_category(self, category):
		"""Find all products in relation with a category"""
		cursor = cnx.cursor()
		query01 = """
			SELECT
				DISTINCT product.name,product.bar_code,nutriscore.name as nutriscore
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
		for i, result in enumerate(results, start = 1):
			self.list_products_category.append((i, (result[0], result[1], result[2])))
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