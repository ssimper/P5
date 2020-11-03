"""Module responsible of creating a single database connection to MySQL."""

import mysql.connector

import config

# Database connection informations
cnx = mysql.connector.connect(
    user=config.USER,
    password=config.PASSWORD,
    host=config.HOST,
    database=config.DATABASE,
    charset=config.CHARSET
)
