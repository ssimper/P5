import requests
import mysql.connector


payload = {
	"action": "process",
	"sort_by": "unique_scan_n",
	"page_size": 500,
	"json": 1
}

res = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?',
	params = payload)

results = res.json()
products = results["products"]

cnx = mysql.connector.connect(
	user='simper',
	password='eugostodomysql',
	host='localhost',
	database='off_test3',
	charset='utf8'
	)

cursor = cnx.cursor()

print("Nettoyage des tables ...")
cursor.execute(
	"""DELETE FROM product_category"""
	)
cursor.execute(
	"""DELETE FROM product_store"""
	)
cursor.execute(
	"""DELETE FROM product"""
	)
cursor.execute(
	"""DELETE FROM nutriscore"""
	)
cursor.execute(
	"""DELETE FROM store"""
	)
cursor.execute(
	"""DELETE FROM category"""
	)
cnx.commit()

"""Variables defintion"""
deleted_product = 0

"""Filling the database."""
for i, product in enumerate(products):
	"""Verification of the existence of nutriscore and generic_name_fr. If exists it is put in the
	database else it is removed."""
	if 'nutrition_grades' in product and 'generic_name_fr' in product:
		cursor.execute(
			"""
			INSERT INTO
				nutriscore (name)
			VALUES
				(
					%(nutrition_grades)s
				)
			ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
			"""
			, {
			    "nutrition_grades": product['nutrition_grades']
			}
			)
		cnx.commit()
		
		"""Product table filling (nutriscore ok)"""
		print(f"Traitement du produit n°{i}",
			"code :", product['code'],
			"nom :", product['product_name_fr'],
			"description", product['generic_name_fr'],
			"nutriscore :", product['nutrition_grades']
			)
		cursor.execute(
			"""
			INSERT INTO
		    	product (bar_code, name, description, nutriscore_id, url)
			VALUES
		    	(
		    		%(bar_code)s,
		    		%(name)s,
		    		%(description)s,
		    		(
		    	    	SELECT id FROM nutriscore
		    	    	WHERE name = %(score)s
		    		),
		    		%(url)s
		    	)
			""",
			{
				"bar_code": product['code'],
				"name": product['product_name_fr'],
				"description": product['generic_name_fr'],
				"score": product['nutrition_grades'],
				"url": product['url']
			}
		)
		cnx.commit()
	else:
		del products[i]
		deleted_product += 1
		continue #abort product treatment, go back to for !

	"""Product stores enumeration"""
	if 'stores' not in product:
		cursor.execute(
			"""
			INSERT INTO
				store (id, name)
			VALUES
				(
					null, %(stores)s
				)
			""",
			{
				"stores": 'store_less'
			}
			)
	else:
		store_list = (product['stores']).split(',')
		for store in store_list:
			"""Put stores in store table"""
			cursor.execute(
				"""
				INSERT INTO
					store (id, name)
				VALUES
					(
						null, %(stores)s
					)
				ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
				""",
				{
			    	"stores": (store.strip()).capitalize()
				}
				)
			"""product_store association"""
			cursor.execute(
				"""
				INSERT INTO
					product_store (product_bar_code, store_id)
				VALUES
					(
						%(code)s,
						(
							SELECT id FROM store
							WHERE name = %(store_name)s
						)
					)
				""",
				{
					"code": product['code'],
					"store_name": (store.strip()).capitalize()
				}	
			)
			cnx.commit()

		
	"""Product categories enumeration"""
	category_list = (product['categories']).split(',')
	for category in category_list:
		#print("category en cours ...")
		cursor.execute(
			"""
			INSERT INTO
				category (id, name)
			VALUES
				(
					null, %(categories)s)
			ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
			""",
			{
				"categories": (category.strip()).capitalize()
			}
			)
		cnx.commit()
		
		"""product_category association"""
		cursor.execute(
            """
            INSERT INTO
                product_category (product_bar_code, category_id)
            VALUES
                (
                    %(code)s,
                    (
                        SELECT id FROM category
                        WHERE name = %(category_name)s
                    )
                )
            """,
            {
            	"code": product['code'],
            	"category_name": (category.strip()).capitalize()
            }
		)
		cnx.commit()

	print(f"Fin de traitement du produit n°{i}")

"""Results"""
print(f"Produits listés : {i + 1}, produits supprimés : {deleted_product}")


