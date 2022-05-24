from flask import Flask, render_template, url_for, request
from csvReader import csvRead

app = Flask(__name__)

# index login
@app.route("/", methods=["POST", "GET"])
def index():
    usernameCorrect = False
    passwordCorrect = False
    userIndex = 0
    count = 0
    loginData = csvRead('csvLogin.csv')
    if request.form["user"] != "":
        username = request.form["user"]
        for user in loginData:
            if user[0] == username:
                usernameCorrect = True
                userIndex = count
            else:
                count += 1

        if request.form["pass"] != "":
            if usernameCorrect == True:
                password = request.form["pass"]
                if loginData[userIndex][1] == request.form["pass"]:
                    passwordCorrect = True
        if passwordCorrect == True:
            pass
    
    return render_template("index.html")

# service select
@app.route("/reviews", methods=["POST", "GET"])
def reviews():

    
if __name__ == "__main__":
    app.run()

# TO-DO: add redirect and pass variables