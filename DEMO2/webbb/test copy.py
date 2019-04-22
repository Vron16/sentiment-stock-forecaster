from flask import Flask, get_template_attribute, render_template, url_for, request, redirect, jsonify
from SentimentController import SentimentController
from flask import *
from Database import Database
import techcontroller
import mysql.connector as ms
import json
from ATController import AutomatedTrader as AT

useremail = ""

app = Flask(__name__)



class DataStore():
    useremail = None

data = DataStore()

@app.route('/addUser/',methods=['GET','POST'])
def addUser():
    db = Database()
    email = request.args.get('useremail', 0, type=str)
    password = request.args.get('userpassword', 0, type=str)
    data.useremail = email
    outputstr = db.addUser(email,password)
    return jsonify(outputstr)

@app.route('/login/',methods=['GET','POST'])
def login():
    db = Database()
    email = request.args.get('loginemail', 0, type=str)
    data.useremail = email

    password = request.args.get('loginpassword', 0, type=str)
    loginstr = db.validateLogin(email,password)
    print("main email is", useremail)
    print(loginstr)
    return jsonify(loginstr)



@app.route('/deposit/',methods=('GET','POST'))
def deposit():
    db = Database()
    email = data.useremail

    amt = request.args.get('depositamt', 0, type=str)
    result = db.deposit(email,amt)
    result.append(email)
    return jsonify(result)

@app.route('/withdraw/',methods=('GET','POST'))
def withdraw():
    db = Database()

    email = data.useremail
    amt = request.args.get('withdrawamt', 0, type=str)

    result = db.withdraw(email,amt)
    result.append(email)

    return jsonify(result)

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
    SentController.trend(userInput)
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
@app.route('/autotrade/',methods=['GET','POST'])
def run_autotrader():
    # '''autotrader method'''
    print("print runauto")
    ATStockName = request.args.get('ATStockName', 0, type=str)
    durationDays = request.args.get('durationDays', 0, type=int)
    durationHrs = request.args.get('durationHrs', 0, type=int)
    durationDMin = request.args.get('durationMin', 0, type=int)

    seconds = 60*durationDMin + 3600*durationHrs + 86400*durationDays

    autotrader = AT()
    at_out = autotrader.auto_trade(ATStockName, seconds)
    #autotrader=AT.auto_trade(ATStockName,seconds)
    print(at_out)

    return jsonify(at_out)


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
