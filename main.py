#   pip install httpx

from asyncio.windows_events import NULL
from cmath import log
from distutils.log import Log
from gettext import NullTranslations
from flask import Flask, render_template, url_for, request, redirect, session
import db_functions
import httpx

from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'



# Index login
@app.route("/", methods=["POST", "GET"])
def index():
    try:
        err = request.args['err']
        print(err)
    except:
        err = ""
    
    print('err=',err)
    session['login'] = True
    return render_template("index.html", err=err)


# Service select
@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    print()
    sessionuser = ""
    usernameCorrect = False
    passwordCorrect = False
    # If user submits login form from index.html
    print('user:',session['user'])
    print('login:',session['login'])
    print('scan:', session['scan'])



    if request.method == "POST" and session['login']:
        session['login'] = True
        # If user input is not empty
        if request.form["user"] != "":
            print("user not empty")
            print(request.form["user"])
            username = request.form["user"]

            if db_functions.dbGetUser(username) != []:
                sessionuser = db_functions.dbGetUser(username)[0]
                session['user'] = sessionuser
                sessionSN = db_functions.dbGetUser(username)[2]
                session['sn'] = sessionSN
                userCollege = db_functions.dbGetUser(username)[3]
                session['userCollege'] = userCollege
                userCourse = db_functions.dbGetUser(username)[4]
                session['userCourse'] = userCourse
                usernameCorrect = True
            else:
                return redirect(url_for('index', err=err))

            # If password is not empty
            if request.form["pass"] != "":
                print("pass not empty")
                # If username is in csvLogin
                if usernameCorrect == True:
                    print("user correct")
                    password = request.form["pass"]
                    # If password matches username entered in csvLogin
                    if db_functions.dbGetUser(username)[1] == password:
                        print("pass correct")
                        passwordCorrect = True
                    else:
                        passwordCorrect = False
                else:
                    err = "Username Incorrect"
                    return redirect(url_for('index', err=err))
            else:
                err = "Password Field Empty"
                return redirect(url_for("index", err=err))
            if passwordCorrect == True:
                filteredData = db_functions.dbReadBorrowOrder_studentID(sessionSN)
                due = []
                for row in filteredData:
                    if row[5] == None:
                        due.append(row)
                session['login'] = False
                return render_template("dashboard.html", name=session['user'], college=session['userCollege'], course=session['userCourse'], data=filteredData, scandata=[], returnable_book=[], due=due)
            else:
                err = "Password Incorrect"
                return redirect(url_for("index", err=err))
        else:
            err = "Username Field Empty"
            return redirect(url_for('index', err=err))
    
    
    
    elif request.method == "GET" and session['scan']:
        isbn = request.args['isbn']
        title = request.args['title']
        returnable_book = []
        due=[]

        filteredData = db_functions.dbReadBorrowOrder_studentID(session['sn'])
        print('data',filteredData)
        for row in filteredData:
            if int(isbn) == int(row[2]) and row[5] == None:
                for item in row:
                    returnable_book.append(item)
                break
            if row[5] == None:
                due.append(row)
        print('ret', returnable_book)
        session['scan'] = False
        return render_template("dashboard.html", name=session['user'], college=session['userCollege'], course=session['userCourse'], data=filteredData, scandata=[isbn, title, datetime.now(), datetime.now()+relativedelta(months=+1)], returnable_book=returnable_book, due=due)
    
    
   
    elif request.method == "GET" and not session['scan']:
        filteredData = db_functions.dbReadBorrowOrder_studentID(session['sn'])
        due = []
        for row in filteredData:
            if row[5] == None:
                print(row)
                due.append(row)
        return render_template("dashboard.html", name=session['user'], college=session['userCollege'], course=session['userCourse'], data=filteredData, scandata=[], returnable_book=[], due=due)


    elif request.method == "POST" and not session['login']:
        filteredData = db_functions.dbReadBorrowOrder_studentID(session['sn'])
        print(request.form.get('b-check'))
        if request.form.get('b-check') == 'b-check1': #BORROWING
            print('borrowing')
            # Get form details and use dbfunction to create a new row in history
            db_functions.dbCreateBorrowOrder(db_functions.createID(),session['sn'],request.form["b-isbn"])
            due = []
            for row in filteredData:
                if row[5] == None:
                    print(row)
                    due.append(row)
            # return render_template("dashboard.html", name=session['user'], college=session['userCollege'], course=session['userCourse'], data=filteredData, scandata=[], returnable_book=[], due=due)
            return redirect(url_for('dashboard'))

        elif request.form.get('b-check') == 'b-check2': #RETURNING
            print('returning')
            # Get form details and use dbfunction to update existing row in history
            db_functions.dbCreateReturnOrder(request.form['b-id'])
            due = []
            for row in filteredData:
                if row[5] == None:
                    print(row)
                    due.append(row)
            # return render_template("dashboard.html", name=session['user'], college=session['userCollege'], course=session['userCourse'], data=filteredData, scandata=[], returnable_book=[], due=due)
            return redirect(url_for('dashboard'))
        else:        
            print('rendering...')
            return redirect(url_for('dashboard'))
            # return redirect(url_for('dashboard', isbn=None, title=None))


    
    
    
    else:
        err = ""
        return redirect(url_for('index', err=err))
    
    

@app.route("/scan", methods=["POST", "GET"])
def scan():

    inputBook = '214748368' #214748367

    session['scan'] = True
    bookdeets = []
    bookavailable = False
    booklist = httpx.get('https://raw.githubusercontent.com/Yogurtchan/Library-Dashboard/eduard-database-functions/static/books.json')
    
    for book in booklist.json():
        if book['isbn'] == inputBook:
            bookavailable = True
            bookdeets.append(book['isbn'])
            bookdeets.append(book['title'])
            break
        else:
            bookavailable = False

    if bookavailable:
        print('book available')
        return redirect(url_for('dashboard', isbn=bookdeets[0], title=bookdeets[1]))
    else:
        print('book unavailable')
        return redirect(url_for('dashboard', isbn=None, title=None))

if __name__ == "__main__":
    app.run()
