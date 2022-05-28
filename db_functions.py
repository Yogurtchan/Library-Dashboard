# Uses XAMPP
#   pip install pandas
#   pip install mysql-connector-python

from datetime import datetime
import mysql.connector
from mysql.connector import Error
import pandas as pd
from dateutil.relativedelta import relativedelta

dbname = "libdb"
test_username = "testuser"
test_password = "testpass"
test_studID = "301820946"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database=dbname
)

mycursor = db.cursor()


def dbInit():
    mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname};")

    try:
        mycursor.execute("CREATE TABLE UserData (name VARCHAR(50), password VARCHAR(50), studentID int);")
    except:
        pass

    try:
        mycursor.execute("CREATE TABLE BorrowHistory (borrowID int, studentID int, bookID int, borrowed datetime NOT NULL, duedate datetime NOT NULL);")
    except:
        pass

    try:
        mycursor.execute("CREATE TABLE ReturnHistory (borrowID int, studentID int, bookID int, returned datetime NOT NULL);")
    except:
        pass

    
    mycursor.execute(f"INSERT INTO UserData (name, password, studentID) VALUES ('{test_username}', '{test_password}', '{test_studID}')")

    db.commit()

    mycursor.execute("SELECT * FROM UserData")
    
    for x in mycursor:
        print(x)


def dbGetUser(username):
    final = []
    mycursor.execute(f"""
    SELECT name, password, studentID
    FROM UserData
    WHERE name = '{username}'
    """)

    for x in mycursor:
        final.append(x)

    return final[0]


def dbSetUser(user,password,studentID):
    mycursor.execute(f"""
    INSERT INTO UserData (name, password, studentID)
    VALUES ('{user}', '{password}', '{studentID}')
    """)
    db.commit()

def dbCreateBorrowOrder(borrowID, studentID, bookID, borrowed=datetime.now(), duedate=datetime.now()+relativedelta(months=+1)):
    mycursor.execute("""
        INSERT INTO BorrowHistory (borrowID, studentID, bookID, borrowed, duedate)
        VALUES (%s,%s,%s,%s,%s) """, (borrowID, studentID, bookID, borrowed, duedate))
    db.commit()

def dbCreateReturnOrder(borrowID, studentID, bookID, returned=datetime.now()):
    mycursor.execute("""
        INSERT INTO ReturnHistory (borrowID, studentID, bookID, returned)
        VALUES (%s,%s,%s,%s) """, (1, 202212347, 101, datetime.now()))
    db.commit()

def dbReadBorrowOrder(borrowID):
    final = []
    mycursor.execute(f"""
    SELECT borrowID, studentID, bookID, borrowed, duedate
    FROM BorrowHistory
    WHERE borrowID = '{borrowID}'
    """)

    for x in mycursor:
        final.append(x)

    return final[0]

def dbReadReturnOrder(borrowID):
    final = []
    mycursor.execute(f"""
    SELECT borrowID, studentID, bookID, returned
    FROM ReturnHistory
    WHERE borrowID = '{borrowID}'
    """)

    for x in mycursor:
        final.append(x)

    return final[0]