import mysql.connector as mariadb
import datetime

# Open database connection
db = mariadb.connect(user="root", password="c3#09repo", database="Raspi")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT start FROM pump")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print("Database version : %s " % data)

print(data[0])

waktu = datetime.datetime.now()
Start = datetime.time(waktu.hour, waktu.minute, waktu.second).strftime("%H:%M:%S")

print(Start)
if Start > data[0]:
    print("SUKSES")
# disconnect from server
db.close()
