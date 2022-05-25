from flask import Flask, render_template, url_for, request, redirect, session
from csvReader import csvRead

app = Flask(__name__)

# index login
@app.route("/", methods=["POST", "GET"])
def index():
    try:
        err = request.args['err']
        print(err)
    except:
        err = ""
    
    print('err=',err)
    return render_template("index.html", err=err)

    

# service select
@app.route("/reviews", methods=["POST", "GET"])
def reviews():
    sessionuser = ""
    usernameCorrect = False
    passwordCorrect = False
    userIndex = 0
    count = 0
    loginData = csvRead("csvLogin.csv")

    if request.method == "POST":
        if request.form["user"] != "":
            print("user not empty")
            username = request.form["user"]
            for user in loginData:
                if user[0] == username:
                    sessionuser = user[0]
                    usernameCorrect = True
                    userIndex = count
                else:
                    count += 1

            if request.form["pass"] != "":
                print("pass not empty")
                if usernameCorrect == True:
                    print("user correct")
                    password = request.form["pass"]
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
                return redirect(url_for('index', err=err))

            if passwordCorrect == True:
                return render_template("dashboard.html", name=sessionuser)

            else:
                err = "Password Incorrect"
                return redirect(url_for('index', err=err))
        else:
            err = "Username Field Empty"
            return redirect(url_for('index', err=err))
    else:
        err = ""
        return redirect(url_for('index', err=err))
    
if __name__ == "__main__":
    app.run()

# TO-DO: add redirect and pass variables