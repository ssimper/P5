import mysql.connector

cnx = mysql.connector.connect(
	user='simper',
	password='eugostodomysql',
	host='localhost',
	database='off_test',
	charset='utf8'
	)

cursor = cnx.cursor()
cursor.execute(
	"""
	SELECT
		product.name
	FROM
		product
	INNER JOIN
		nutriscore
	ON
		nutriscore_id = nutriscore.id
	WHERE
		nutriscore.name = 'a'
	"""
	)

results = cursor.fetchall()
for result in results:
	print(result[0]) #Attention les résultats sont des tuples