from flask import Flask, get_template_attribute, render_template, url_for, request, redirect, jsonify
from SentimentController import SentimentController
from flask import *
import mysql.connector as ms
import json
import hashlib

app = Flask(__name__)
class Database:
    def __init__(self):
        host = "mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com"
        user = "root"
        password = "mypassword"
        db = "mydb"

        self.con = ms.connect(host=host, user=user, password=password, db=db)
        self.cur = self.con.cursor(buffered=True)
    def addUser(self):
        email =  request.args.get('useremail', 0, type=str)
        password = request.args.get('userpassword', 0, type=str)
        self.cur.execute("SELECT * from user WHERE email = (%s)", (email,))
        row_count = self.cur.rowcount
        if row_count == 0:
            hashpass = int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16) % 10 ** 8
            self.cur.execute("INSERT INTO user(email,password,balance) VALUES(%s,%s,%s)",(email,hashpass,'1000'))
            self.con.commit()
            return "Account Created"
        else:
            return "Account Already Exists, Please Log Out And Try Again"
    def validateLogin(self):
        email = request.args.get('loginemail', 0, type=str)
        password = request.args.get('loginpassword', 0, type=str)
        self.cur.execute("SELECT * from user WHERE email = (%s)", (email,))
        result = self.cur.fetchall()
        print(result)
        print(email)
        row_count = self.cur.rowcount
        if row_count == 0:
            return 'Account does not exist, Please Log Out And Try Again'
        hashpass = int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16) % 10 ** 8
        if(int(result[0][2],10) == hashpass):
            #this finds the password element in result, and then converts it to an integer to test against the hashed function
            return 'Successfully logged in'

        else:
            return 'Wrong Password, Please Go To The Home Tab and Re-confirm Your Information'




    def printStockCode(self):
        self.cur.execute("SELECT stock_code from stock LIMIT 5")
        result = self.cur.fetchall()
        return result




@app.route('/addUser/',methods=['GET','POST'])
def addUser():
    db = Database()
    outputstr = db.addUser()
    return jsonify(outputstr)

@app.route('/login/',methods=['GET','POST'])
def login():
    db = Database()
    loginstr = db.validateLogin()
    print(loginstr)
    return jsonify(loginstr)

@app.route('/testFunc/', methods=['GET', 'POST'])
def testFunc():
    SentController = SentimentController()
    data = request.args.get('stockName', 0, type=str)
    headlines = SentController.requestHeadlines(data)
    k = testFunc1()
    array = [headlines, k]
    return jsonify(array)

@app.route('/loginn/', methods=['GET', 'POST'])
def loginn():
    return render_template('login.html')

@app.route('/loginb/', methods=['GET', 'POST'])
def loginb():
    return render_template('logout.html')

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    return render_template('index.html')

def testFunc1():
    sentController = SentimentController()
    data = request.args.get('stockName', 0, type=str)
    returned = sentController.finalToUser(data)
    return returned


@app.route('/')
def lionel():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
