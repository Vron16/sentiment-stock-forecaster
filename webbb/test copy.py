from flask import *
from webbb.SentimentController import SentimentController
import webbb.techcontroller

app = Flask(__name__)

@app.route('/tickerRequest/', methods=['GET'])
def dropdown():
    SentController = SentimentController()
    return jsonify(SentController.getStockTickers())

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


@app.route('/techFunc/', methods=['GET', 'POST'])
def techFunc():
    data = request.args.get('stockNameTech', 0, type=str)
    arr = webbb.techcontroller.getPrediction(data)
    if not arr:
        return []
    return json.dumps(arr)


@app.route('/')
def lionel():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
