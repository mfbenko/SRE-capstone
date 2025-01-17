#necessary import to get pull information out of the database
import mysql.connector

#create the sql connection
MySQL = mysql.connector.connect(
	host='localhost',
	user='root',
	password='root'
)

#create a cursor write the queries
cursor = MySQL.cursor()

#This script is strictly for the capstone_db and summary table
cursor.execute("""USE capstone_db""")

#print the hard coded host count to the screen
cursor.execute("""SELECT host_count FROM summary;""")
results = cursor.fetchall()
type = "get: "
for row in results:
	print(f"{type}{row[0]}")
	type = "post: "
print("\n")

#print the hard coded url count to the screen
cursor.execute("""SELECT unique_URLS FROM summary;""")
results = cursor.fetchall()
type = "get: "
for row in results:
	print(f"{type}{row[0]}")
	type = "post: "
print("\n")
	
#print the hard coded accept boolean to the screen
cursor.execute("""SELECT Accept_exists FROM summary;""")
results = cursor.fetchall()
type = "get: "
for row in results:
	print(f"{type}{row[0]}")
	type = "post: "
print("\n")

#allow the user to query anything else
while(True):
	user_query = input("Please Type your query.\n")
	cursor.execute(user_query)
	results = cursor.fetchall()
	type = "get: "
	for row in results:
		print(f"{type}{row[0]}")
		type = "post: "
	print("\n")
	
#Make the commit and exit MySQL
cursor.close()
MySQL.close()



