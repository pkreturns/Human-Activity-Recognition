import csv
import mysql.connector

cnx = mysql.connector.connect(
  host='localhost',
  user='root',
  password='',
  database='activity'
)

cursor = cnx.cursor()
query = "SELECT x,y,z FROM accl_data"
cursor.execute(query)

rows = cursor.fetchall()

output_file = 'activity.csv'

with open(output_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # csv_writer.writerow([i[0] for i in cursor.description])  #column headers
    csv_writer.writerows(rows)  #data rows

cursor.close()
cnx.close()
