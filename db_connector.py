import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="DbMysql15", # need to change
  password="DbMysql15", # need to change
  database="DbMysql15",
  port="3305",
  raise_on_warnings=True
)