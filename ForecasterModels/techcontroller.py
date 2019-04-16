import mysql.connector as ms
import datetime
import mm

prediction = 0

def getStockData(stock_name):
    cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com', database='mydb')
    mycursor = cnx.cursor()
    
    query = "SELECT datetime, open, high, low, close FROM day_price WHERE stock_code = '" + stock_name + "'"
    mycursor.execute(query)
    result = mycursor.fetchall()

    time_stamps = [i[0] for i in result]
    open_prices = [i[1] for i in result]
    close_prices = [i[4] for i in result]
    high_prices = [i[2] for i in result]
    low_prices = [i[3] for i in result]
    '''    
    for i in range(len(time_stamps)):
        print(time_stamps[i])
        if(i > 0):
            if(time_stamps[i].day < time_stamps[i-1].day):
                print("Bigger?")
    '''
    cnx.close()
    return (time_stamps, high_prices, low_prices, open_prices, close_prices)

def getPrediction(stock_name):
    stock_data = getStockData(stock_name)    
    roc = mm.getRateOfChange(stock_data) #array
    stoch_os = mm.getStochasticOscillator(stock_data) #array
    asi = mm.getASI(stock_data) #array
    arima_prediction = mm.getARIMA(stock_data[4]) #double
    fourier_prediction = mm.getFourier(stock_data[4])
    
    mm.aggregatePrediction(roc, stoch_os, asi, arima_prediction, fourier_prediction)
    return
  
def storePrediction():
    #cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com', database='mydb')
    #mycursor = cnx.cursor()

    #query = "SELECT datetime, open, high, low, close FROM day_price WHERE stock_code = '" + stock_name + "'"
    #mycursor.execute(query)
    #cnx.close()
    return

#getStockData("AAPL")
getPrediction("AAPL")