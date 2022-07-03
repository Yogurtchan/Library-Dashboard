# Uses XAMPP
#   pip install pandas
#   pip install mysql-connector-python

from asyncio.windows_events import NULL
from cmath import log
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import pandas as pd
from dateutil.relativedelta import relativedelta
import random
import string
from random import shuffle

dbname = "libdb1"
test_username = "testuser"
test_password = "testpass"
test_studID = "301820946"
test_college = "CLAC"
test_course = "BS Psychology"

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
        mycursor.execute("CREATE TABLE UserData (name VARCHAR(50), password VARCHAR(50), studentID int, college VARCHAR(50), course VARCHAR(50));")
    except:
        pass

    try:
        mycursor.execute("CREATE TABLE Hist=ory (borrowID int, studentID int, bookISBN int, borrowed datetime NOT NULL, duedate datetime NOT NULL, returndate datetime);")
    except:
        pass
    
    mycursor.execute(f"INSERT INTO UserData (name, password, studentID) VALUES ('{test_username}', '{test_password}', '{test_studID}', '{test_college}', '{test_course}')")

    db.commit()

    mycursor.execute("SELECT * FROM UserData")
    
    for x in mycursor:
        print(x)


def dbGetUser(username):
    final = []
    mycursor.execute(f"""
    SELECT name, password, studentID, college, course
    FROM userdata
    WHERE name = '{username}'
    """)

    for x in mycursor:
        final.append(x)

    try:
        return final[0]
    except IndexError:
        return []

def dbSetUser(user, password, studentID, college, course):
    mycursor.execute(f"""
    INSERT INTO userdata (name, password, studentID, college, course)
    VALUES ('{user}', '{password}', '{studentID}', '{college}', '{course}')
    """)
    db.commit()

def dbCreateBorrowOrder(borrowID, studentID, bookISBN, borrowed=datetime.now(), duedate=datetime.now()+relativedelta(months=+1)):
    mycursor.execute("""
        INSERT INTO history (borrowID, studentID, bookISBN, borrowed, duedate, returndate)
        VALUES (%s,%s,%s,%s,%s,NULL) """, (borrowID, studentID, bookISBN, borrowed, duedate))
    db.commit()

def dbReadAllBorrowOrder():
    final = []
    mycursor.execute(f"""
    SELECT *
    FROM history;
    """)

    for x in mycursor:
        final.append(x)

    return final

def dbReadBorrowOrder_borrowID(borrowID):
    final = []
    mycursor.execute(f"""
    SELECT borrowID, studentID, bookISBN, borrowed, duedate, returndate
    FROM history
    WHERE borrowID = '{borrowID}'
    """)

    for x in mycursor:
        final.append(x)

    return final[0]

def dbReadBorrowOrder_studentID(ID):
    final = []
    mycursor.execute(f"""
    SELECT borrowID, studentID, bookISBN, borrowed, duedate, returndate
    FROM history
    WHERE studentID = {ID}
    """)

    for x in mycursor:
        final.append(x)

    return final

def dbCreateReturnOrder(borrowID, date=datetime.now()):
    mycursor.execute("""
    UPDATE history
    SET returndate = %s
    WHERE borrowID = %s
    """, (date, borrowID))
    db.commit()

def createID():
    letters = string.ascii_letters
    lower = ''.join(random.choice(letters) for i in range(4))
    letters = string.digits
    digs = ''.join(random.choice(letters) for i in range(2))
    joint = lower+digs
    word = list(joint)
    shuffle(word)
    return ''.join(word)

    

print(dbReadBorrowOrder_studentID(202230456))

# dbCreateBorrowOrder("Af93Da", 202230456, 9789562911122, borrowed=datetime(2022, 5, 16, 1, 1, 1), duedate=datetime(2022, 6, 16, 1, 1, 1))
# dbCreateBorrowOrder("d68A1e", 202230457, 9781388266783, borrowed=datetime(2022, 4, 29, 1, 1, 1), duedate=datetime(2022, 5, 29, 1, 1, 1))
# dbCreateBorrowOrder("fF3001", 202230456, 9781107665644, borrowed=datetime(2022, 4, 17, 1, 1, 1), duedate=datetime(2022, 5, 17, 1, 1, 1))
# dbCreateBorrowOrder("b88ed1", 202230458, 9780020547204, borrowed=datetime(2022, 3, 9, 1, 1, 1), duedate=datetime(2022, 4, 9, 1, 1, 1))
# dbCreateBorrowOrder("45c338", 202230458, 9789715507813, borrowed=datetime(2022, 5, 23, 1, 1, 1), duedate=datetime(2022, 6, 23, 1, 1, 1))
# dbCreateBorrowOrder("4aAb56", 202230457, 9781405087247, borrowed=datetime(2022, 4, 30, 1, 1, 1), duedate=datetime(2022, 5, 30, 1, 1, 1))
# dbCreateBorrowOrder("56bb90", 202230456, 9780717803026, borrowed=datetime(2022, 3, 12, 1, 1, 1), duedate=datetime(2022, 4, 12, 1, 1, 1))
# dbCreateBorrowOrder("2E781d", 202230457, 9781784162122, borrowed=datetime(2022, 4, 1, 1, 1, 1), duedate=datetime(2022, 5, 1, 1, 1, 1))
# dbCreateBorrowOrder("33dAe5", 202230456, 9780679734529, borrowed=datetime(2022, 4, 18, 1, 1, 1), duedate=datetime(2022, 5, 18, 1, 1, 1))

# dbCreateReturnOrder("Af93Da", date=datetime(2022, 5, 23, 1, 1, 1))
# dbCreateReturnOrder("d68A1e", date=datetime(2022, 5, 25, 1, 1, 1))
# dbCreateReturnOrder("fF3001", date=datetime(2022, 5, 3, 1, 1, 1))
# dbCreateReturnOrder("b88ed1", date=datetime(2022, 3, 21, 1, 1, 1))
# dbCreateReturnOrder("45c338", date=datetime(2022, 5, 23, 1, 1, 1))
# dbCreateReturnOrder("4aAb56", date=datetime(2022, 5, 11, 1, 1, 1))
# dbCreateReturnOrder("56bb90", date=datetime(2022, 3, 28, 1, 1, 1))
# dbCreateReturnOrder("2E781d", date=datetime(2022, 4, 24, 1, 1, 1))
# dbCreateReturnOrder("33dAe5", date=datetime(2022, 5, 9, 1, 1, 1))