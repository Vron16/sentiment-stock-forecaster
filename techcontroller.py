import mysql.connector as ms
import datetime
import mm

from tkinter import *
from tkinter import messagebox

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
    if len(stock_data[0]) == 0:
        messagebox.showinfo(stock_name, "Invalid stock name, no data available")
        return

    roc = mm.getRateOfChange(stock_data)  # array
    stoch_os = mm.getStochasticOscillator(stock_data)  # array
    #asi = mm.getASI(stock_data)  # array
    asi = [0,1]
    arima_prediction = mm.getARIMA(stock_data[4])  # double

    prediction = mm.aggregatePrediction(roc, stoch_os, asi, arima_prediction)
    messagebox.showinfo(stock_name, stock_name + "\n\nRate of Change: " + str(round(roc[0],5)) + "%\n" +
                        "Stochastic Oscillator: " + str(round(stoch_os[0],5)) + "%\n" +
                        "Accumulated Swing Index: " + str(asi[0]) + "\n" + "ARIMA Prediction: $"
                        + str(round(arima_prediction,5)) + "\n\n" + "Overall Predicted Price: $" + str(round(prediction,5)))
    return


def storePrediction():
    # cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com', database='mydb')
    # mycursor = cnx.cursor()

    # query = "SELECT datetime, open, high, low, close FROM day_price WHERE stock_code = '" + stock_name + "'"
    # mycursor.execute(query)
    # cnx.close()
    return


def buttonFunc():
    getPrediction(e1.get())


# ---------- Tinker setup ---------

top = Tk()
top.wm_title("Technical Forecaster")
top.geometry("1400x800")
top.configure(background='grey')

labelText = StringVar()
labelText.set("Welcome !!!!")

Label(top, text="Enter Stock").place(x=600, y=553)
e1 = Entry(top)
e1.place(x=680,  y=550)

B1 = Button(top, text="Get Prediction", bg="green", fg="black", command=buttonFunc).place(x=670, y=600)
top.mainloop()
