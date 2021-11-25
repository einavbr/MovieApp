import mysql.connector

mydb = mysql.connector.connect(
  host="mysqlsrv1.cs.tau.ac.il",
  user="yourusername", # need to change
  password="yourpassword", # need to change
  database="movies_db"
)