from flask import Flask, get_template_attribute, render_template, url_for, request, redirect, jsonify
from SentimentController import SentimentController
from flask import *
from SentimentController import SentimentController
import json

app = Flask(__name__)


@app.route('/testFunc/', methods=['GET', 'POST'])
def testFunc():
    SentController = SentimentController()
    data = request.args.get('stockName', 0, type=str)
    headlines = SentController.requestHeadlines(data)
    k = testFunc1()
    array = [headlines, k]
    return jsonify(array)


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
