import mysql.connector
import records

cnx = mysql.connector.connect(
	user='simper',
	password='eugostodomysql',
	host='localhost',
	database='off_test',
	charset='utf8'
	)

cursor = cnx.cursor()

db = records.Database("mysql://simper:eugostodomysql@localhost/off_test")
