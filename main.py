from asyncio.windows_events import NULL
from gettext import NullTranslations
from flask import Flask, render_template, url_for, request, redirect, session
from csvReader import csvRead

app = Flask(__name__)

# Index login
@app.route("/", methods=["POST", "GET"])
def index():
    try:
        err = request.args['err']
        print(err)
    except:
        err = ""
    
    print('err=',err)
    return render_template("index.html", err=err)


# Service select
@app.route("/dashboard", methods=["POST", "GET"])
def reviews():
    sessionuser = ""
    usernameCorrect = False
    passwordCorrect = False
    userIndex = 0
    count = 0
    loginData = csvRead("csvLogin.csv")
    mockBorrowData = csvRead("csvData.csv")

    print(mockBorrowData)
    # If user submits login form from index.html
    if request.method == "POST":
        # If user input is not empty
        if request.form["user"] != "":
            print("user not empty")
            print(request.form["user"])
            username = request.form["user"]
            # Checks if user input is in csvLogin
            for user in loginData:
                if user[0] == username:
                    sessionuser = user[0]
                    sessionSN = user[2]
                    usernameCorrect = True
                    userIndex = count
                else:
                    count += 1

            # If password is not empty
            if request.form["pass"] != "":
                print("pass not empty")
                # If username is in csvLogin
                if usernameCorrect == True:
                    print("user correct")
                    password = request.form["pass"]
                    # If password matches username entered in csvLogin
                    if loginData[userIndex][1] == password:
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
            # If password is in csvLogin
            if passwordCorrect == True:
                print(mockBorrowData)
                filteredData = []
                for row in mockBorrowData:
                    print(sessionSN)
                    print(row)
                    if sessionSN in row:
                        filteredData.append(row)
                print(filteredData)
                return render_template("dashboard.html", name=sessionuser, data=filteredData)
            else:
                err = "Password Incorrect"
                return redirect(url_for("index", err=err))
        else:
            err = "Username Field Empty"
            return redirect(url_for('index', err=err))
    else:
        err = ""
        return redirect(url_for('index', err=err))
    
    # here
@app.route("/", methods=["POST", "GET"])
def dashboard():
    try:
        err = request.args['err']
        # print(err)
    except:
        err = ""
    
    # print('err=',err)
    return render_template("index.html", err=err)

if __name__ == "__main__":
    app.run()

# TO-DO: add redirect and pass variables