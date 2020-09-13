import mysql.connector
import records

def database_connect():
	cnx = mysql.connector.connect(
		user='simper',
		password='eugostodomysql',
		host='localhost',
		database='off_test',
		charset='utf8'
		)
	cursor = cnx.cursor()
	return cnx, cursor

db = records.Database("mysql://simper:eugostodomysql@localhost/off_test")
