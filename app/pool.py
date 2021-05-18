import mysql.connector


def connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="djangonew",
        port=3307
    )
    mycursor = mydb.cursor()

    return mydb, mycursor
