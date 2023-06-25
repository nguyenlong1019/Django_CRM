# Install MySQL on Computer
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python


import mysql.connector


database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '@Long170502'
)

# prepare a cursor object
cursorObject = database.cursor()

# create a database
cursorObject.execute("CREATE DATABASE mydatabase")

print("All Done!")
