import mysql.connector
import records

cnx = mysql.connector.connect(
	user='simper',
	password='eugostodomysql',
	host='localhost',
	database='off_test3',
	charset='utf8'
	)



db = records.Database("mysql://simper:eugostodomysql@localhost/off_test")
