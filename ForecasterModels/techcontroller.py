import mysql.connector as ms
import datetime
import webbb.mm as mm
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')


def getStockData(stock_name):
    cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com',
                     database='mydb')
    mycursor = cnx.cursor()

    query = "SELECT datetime, open, high, low, close FROM day_price WHERE stock_code = '" + stock_name + "' ORDER BY datetime DESC"
    mycursor.execute(query)
    result = mycursor.fetchall()

    time_stamps = [i[0] for i in result]
    open_prices = [i[1] for i in result]
    close_prices = [i[4] for i in result]
    high_prices = [i[2] for i in result]
    low_prices = [i[3] for i in result]

    cnx.close()
    return (time_stamps, high_prices, low_prices, open_prices, close_prices)


def graph_data(time_stamps, stock_data, stock_name):
    prediction = stock_data[-1]
    print(prediction)

    ts = []
    latest = []
    ticks = range(101)
    for i in range(101):
        latest.append(stock_data[-1 * (102 - i)])
        ts.append(time_stamps[101 - (i + 1)].strftime("%b-%d %I:%M%p"))

    print("length: ", len(latest))
    np_stock_data = np.array(latest)
    plt.plot(ticks, np_stock_data, 'b', linewidth=2)
    print(latest[-1])
    if prediction >= latest[-1]:
        plt.plot(102, prediction, 'g+', linestyle='dashed')
    else:
        plt.plot(102, prediction, 'r-', linestyle='dashed')

    plt.xticks(ticks[::20], ts[::20], rotation=45)
    plt.grid(color='k', linestyle='--', linewidth=1, axis='x')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(stock_name)
    plt.tight_layout()
    plt.savefig('static/a.jpg')
    return


def getPrediction(stock_name):
    stock_data = getStockData(stock_name)

    if not stock_data[0]:
        print("Sorry, the stock you requested is not in our database.")
        print("Please enter another stock.")
        return []
    roc = mm.getRateOfChange(stock_data)  # array
    stoch_os = mm.getStochasticOscillator(stock_data)  # array
    asi = mm.getASI(stock_data)  # array
    curPrice = mm.getCurPrice(stock_data[4])

    data = []
    for i in stock_data[4]:
        data = [i] + data

    arima_prediction = mm.getARIMA(data)  # double
    fourier_prediction = mm.getFourier(data)

    prediction = mm.aggregatePrediction(roc, stoch_os, asi, curPrice, arima_prediction, fourier_prediction)

    data.append(prediction[0])
    graph_data(stock_data[0], data, stock_name)

    return [roc[0], stoch_os[0], asi[0], curPrice, arima_prediction, fourier_prediction[0], prediction[0], prediction[1]]
