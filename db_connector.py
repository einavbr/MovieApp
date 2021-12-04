import mysql.connector

mydb = mysql.connector.connect(
  host="mysqlsrv1.cs.tau.ac.il",
  user="DbMysql15", # need to change
  password="DbMysql15", # need to change
  database="DbMysql15",
  port="3306",
  raise_on_warnings=True
)