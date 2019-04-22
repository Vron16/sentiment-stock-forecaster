from flask import Flask, get_template_attribute, render_template, url_for, request, redirect, jsonify
from SentimentController import SentimentController
import techcontroller
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
    print('Hello')
    SentController = SentimentController()
    userInput = request.args.get('stockName', 0, type=str) #user input which is the stock ticker
    print(userInput)
    webScrapeInput = SentController.getStockTickers(userInput) #returns the database stock name if it's there
    print(webScrapeInput)
    if webScrapeInput == '':
        return jsonify('Error: Stock ticker not in our database. Please choose a NASDAQ stock.')
    print(webScrapeInput)
    #headlines = SentController.requestHeadlines(webScrapeInput)
    #print(headlines)
    #if len(headlines) < 5:
    patterns = [" Common Stock", ",", " -", " (", " Inc ", " Inc.", " Corp.", " Corp ", " Common Stock ", " Ltd.", " Ltd", " Limited", " LLC", " ESG", "ETF", " REIT", " plc"]
    for pat in patterns: #strip the unnecessary terms from the database stock name
        webScrapeInput = webScrapeInput.split(pat, 1)[0]
    print(webScrapeInput)
    stockNameHeadlines = SentController.requestHeadlines(webScrapeInput) #retrieve all headlines with parsed stock name
    stockTickerHeadlines = SentController.requestHeadlines(userInput) #retrieve all headlines with stock ticker
    totalHeadlines = stockNameHeadlines + stockTickerHeadlines #now we have all the headlines from both stock ticker search and db stock name search!
    print(totalHeadlines)
    #only keep the headlines with either stock ticker or webScrapeInput
    parsedHeadlines = []
    for headline in totalHeadlines:
        if webScrapeInput in headline or userInput in headline:
            parsedHeadlines.append(headline)
    print(parsedHeadlines)
    if len(parsedHeadlines) < 5:
        return jsonify([])
    #headlineDeviations = {} #dict that will contain headlines with deviation from average
    #avgScore = SentController.calcAvgSentScore(parsedHeadlines) #average score of all the headlines
    #for headline in parsedHeadlines:
     #   headlineDeviations[headline] = abs(avgScore - SentController.calculateSingleScore(headline))
    #print(headlineDeviations)
    #sortedHeadlineDeviations = sorted(headlineDeviations.items(), key=itemgetter(1))
    #print(sortedHeadlineDeviations)
    #sortedHeadlines = []
    #for headlineDeviation in sortedHeadlineDeviations:
     #   sortedHeadlines.append(headlineDeviation[0])
    #print(sortedHeadlines)
    k = testFunc1(parsedHeadlines)
    array = [parsedHeadlines, k]
    return jsonify(array)


def testFunc1(scraperInput):
    sentController = SentimentController()
    returned = sentController.finalToUser(scraperInput)
    return returned

@app.route('/techFunc/', methods=['GET', 'POST'])
def techFunc():
    data = request.args.get('stockNameTech', 0, type=str)
    print(data)
    arr = techcontroller.getPrediction(data)
    if not arr:
        return json.dumps([])
    return json.dumps(arr)

@app.route('/loginn/', methods=['GET', 'POST'])
def loginn():
    return render_template('login.html')

@app.route('/loginb/', methods=['GET', 'POST'])
def loginb():
    return render_template('logout.html')

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    return render_template('index.html')


@app.route('/')
def lionel():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
