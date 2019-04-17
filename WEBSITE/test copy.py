from flask import Flask, get_template_attribute, render_template, url_for, request, redirect, jsonify
from SentimentController import SentimentController

app = Flask(__name__)


@app.route('/')
def lionel():
    return render_template('index.html')


@app.route('/testFunc', methods=['GET', 'POST'])
def testFunc():
    # SentController = SentimentController()
    data = request.args.get('stockName', 0, type=str)
    print(data)
    #returned = SentController.finalToUser(data)
    #headlines = SentController.requestHeadlines(data)
    #printedHeadlines = SentController.printHeadlines(headlines)
    #print(printedHeadlines)
    #return render_template("jsonn.html", result=data)
    #Data = get_template_attribute('index.html', 'Data')
    hello = get_template_attribute('index.html', 'hello')
    k = (hello('World'))
    print (k)
    return k







if __name__ == '__main__':
    app.run(debug=True)