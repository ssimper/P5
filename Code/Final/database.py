import mysql.connector

"""Database connection informations"""
cnx = mysql.connector.connect(
    user='simper',
    password='eugostodomysql',
    host='localhost',
    database='off_test',
    charset='utf8'
)
