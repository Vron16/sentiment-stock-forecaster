import mysql.connector as ms
import datetime
import mm

prediction = 0


def getStockData(stock_name):
    cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com',
                     database='mydb')
    mycursor = cnx.cursor()

    query = "SELECT datetime, open, high, low, close FROM day_price WHERE stock_code = '" + stock_name + "'"
    mycursor.execute(query)
    result = mycursor.fetchall()

    time_stamps = [i[0] for i in result]
    open_prices = [i[1] for i in result]
    close_prices = [i[4] for i in result]
    high_prices = [i[2] for i in result]
    low_prices = [i[3] for i in result]

    cnx.close()
    return (time_stamps, high_prices, low_prices, open_prices, close_prices)


def getPrediction(stock_name):
    print("In get prediction")
    stock_data = getStockData(stock_name)
    roc = mm.getRateOfChange(stock_data)  # array
    stoch_os = mm.getStochasticOscillator(stock_data)  # array
    asi = mm.getASI(stock_data)  # array
    curPrice = mm.getCurPrice(stock_data[4])
    arima_prediction = mm.getARIMA(stock_data[4])  # double
    fourier_prediction = mm.getFourier(stock_data[4])

    json_result = mm.aggregatePrediction(roc, stoch_os, asi, curPrice, arima_prediction, fourier_prediction)
    return json_result


def storePrediction():
    # cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com', database='mydb')
    # mycursor = cnx.cursor()

    # query = "SELECT datetime, open, high, low, close FROM day_price WHERE stock_code = '" + stock_name + "'"
    # mycursor.execute(query)
    # cnx.close()
    return

#getPrediction("AAPL")