import mysql.connector

cnx = mysql.connector.connect(
  host='localhost',
  user='root',
  password='',
  database='activity'
)

cursor = cnx.cursor()
query = "DELETE FROM `accl_data`"
cursor.execute(query)
cnx.commit()

cursor.close()
cnx.close()