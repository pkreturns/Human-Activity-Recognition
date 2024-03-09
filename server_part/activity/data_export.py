import csv
import mysql.connector

# Connect to the MySQL database
cnx = mysql.connector.connect(
  host='localhost',
  user='root',
  password='',
  database='activity'
)

# Create a cursor to execute SQL queries
cursor = cnx.cursor()

# Execute SELECT query
query = "SELECT x,y,z FROM accl_data"
cursor.execute(query)

# Fetch all rows from the query result
rows = cursor.fetchall()

# Define the output CSV file path
output_file = 'output.csv'

# Write the data to the CSV file
with open(output_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description])  # Write column headers
    csv_writer.writerows(rows)  # Write data rows

# Close the cursor and database connection
cursor.close()
cnx.close()
