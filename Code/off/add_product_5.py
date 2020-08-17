import requests
import mysql.connector


payload = {
	"action": "process",
	"sort_by": "unique_scan_n",
	"page_size": 20,
	"json": 1
}

res = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?', params = payload)

results = res.json()
products = results["products"]

"""utilisation d'un SET pour supprimer les doublons Nutriscore"""
grade_set = set()
cter = 0
for product in products:
	grade_set.add(products[cter]['nutrition_grades'])
	cter += 1
print(grade_set)

"""utilisation d'un SET pour supprimer les doublons Store"""
store_set = set()
cter = 0
for product in products:
	store_list = (products[cter]['stores']).split(',')
	for store in store_list:
		store_set.add(store.capitalize())
	cter += 1
print(store_set)

"""utilisation d'un SET pour supprimer les doublons Category"""
category_set = set()
cter = 0
for product in products:
	category_list = (products[cter]['categories']).split(',')
	for category in category_list:
		category_set.add(category.capitalize())
	cter += 1
print(category_set)

"""Remplissage de la base"""
cnx = mysql.connector.connect(
	user='simper',
	password='eugostodomysql',
	host='localhost',
	database='off_test',
	charset='utf8'
	)

cursor = cnx.cursor()

print("Nettoyage des tables ...")
cursor.execute(
	"""DELETE FROM Product_category"""
	)
cursor.execute(
	"""DELETE FROM Product_store"""
	)
cursor.execute(
	"""DELETE FROM Product"""
	)
cursor.execute(
	"""DELETE FROM Nutriscore"""
	)
cursor.execute(
	"""DELETE FROM Store"""
	)
cursor.execute(
	"""DELETE FROM Category"""
	)
cnx.commit()

cter = 0
"""Nutriscore table filling"""
for letter in grade_set:
	cursor.execute(
		"""INSERT INTO Nutriscore (name)
		VALUES (%(nutrition_grades)s)"""
		, {
		    "nutrition_grades": letter
		}
		)
	cnx.commit()

"""Store table filling"""
for store in store_set:
	cursor.execute(
		"""INSERT INTO Store (name)
		VALUES (%(stores)s)"""
		, {
		    "stores": store
		}
		)
	cnx.commit()

"""Category table filling"""
for category in category_set:
	cursor.execute(
		"""INSERT INTO Category (name)
		VALUES (%(categories)s)"""
		, {
		    "categories": category
		}
		)
	cnx.commit()

"""Product table filling"""
for product in products:
	print("Produit :", products[cter]['product_name_fr'], "code barre :", products[cter]['code'])
	cursor.execute(
		"""
		INSERT INTO
		    Product (bar_code, name, nutriscore_id)
		VALUES
		    (
		    	%(bar_code)s,
		    	%(name)s,
		    	(
		    	    SELECT id FROM Nutriscore
		    	    WHERE name = %(score)s
		    	)
		    )
		""",
		{"bar_code": products[cter]['code'], "name": products[cter]['product_name_fr'], "score": products[cter]['nutrition_grades']}
	)

	"""Product_category filling"""
	list_categories = (products[cter]['categories']).split(',')
	print("Categories listées :", list_categories)
	for category in list_categories:
		cursor.execute(
            """
            INSERT INTO
                Product_category (product_bar_code, category_id)
            VALUES
                (
                    %(code)s,
                    (
                        SELECT id FROM Category
                        WHERE name = %(category_name)s
                    )
                )
            """,
            {"code": products[cter]['code'], "category_name": category}
		)

	"""Product_store filling"""
	list_stores = (products[cter]['stores']).split(',')
	print("Magasins listés :", list_stores)
	for store in list_stores:
		cursor.execute(
			"""
			INSERT INTO
				Product_store (product_bar_code, store_id)
			VALUES
				(
					%(code)s,
					(
						SELECT id FROM Store
						WHERE name = %(store_name)s
					)
				)
			""",
			{"code": products[cter]['code'], "store_name": store}
		)

	cnx.commit()
	cter += 1



cnx.close()