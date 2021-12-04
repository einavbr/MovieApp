# This DB is based on the open source data provided in the following dataset:
# https://www.kaggle.com/rounakbanik/the-movies-dataset
# and on this API:
# https://rapidapi.com/SAdrian/api/data-imdb1/

import mysql.connector

mydb = mysql.connector.connect(
  host="mysqlsrv1.cs.tau.ac.il",
  user="DbMysql15", # need to change
  password="DbMysql15" # need to change
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE DbMysql15")


###############################  HOW TO CREATE THE DB  #################################

## Creating tables:
# mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

## Updating tables:
# mycursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

## Deleting tables:
# mycursor.execute("DROP TABLE IF EXISTS customers")

## Show existing tables:
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#      print(x)

## Import csv file into a python DB
# https://datatofish.com/import-csv-sql-server-python/