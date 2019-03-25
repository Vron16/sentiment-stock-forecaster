import mysql.connector as ms
import datetime
import mm

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


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
        messagebox.showinfo("Invalid stock name", "Invalid stock name, please try again")
        return []

    roc = mm.getRateOfChange(stock_data)  # array
    stoch_os = mm.getStochasticOscillator(stock_data)  # array
    #asi = mm.getASI(stock_data)  # array
    asi = [0,1]
    arima_prediction = mm.getARIMA(stock_data[4])  # double

    prediction = mm.aggregatePrediction(roc, stoch_os, asi, arima_prediction)
    #messagebox.showinfo(stock_name, stock_name + "\n\nRate of Change: " + str(round(roc[0],5)) + "%\n" +
    #                    "Stochastic Oscillator: " + str(round(stoch_os[0],5)) + "%\n" +
    #                    "Accumulated Swing Index: " + str(asi[0]) + "\n" + "ARIMA Prediction: $"
    #                    + str(round(arima_prediction,5)) + "\n\n" + "Overall Predicted Price: $" + str(round(prediction,5)))
    ret = []
    ret.append(stock_name)
    ret.append(str(round(roc[0],5)))
    ret.append(str(round(stoch_os[0],5)))
    ret.append(str(asi[0]))
    ret.append(str(round(arima_prediction,5)))
    ret.append(str(round(prediction,5)))
    return ret


def storePrediction():
    # cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com', database='mydb')
    # mycursor = cnx.cursor()

    # query = "SELECT datetime, open, high, low, close FROM day_price WHERE stock_code = '" + stock_name + "'"
    # mycursor.execute(query)
    # cnx.close()
    return

# ---------- Tinker setup ---------

top = Tk()
top.wm_title("Technical Forecaster")
top.geometry("1400x800")
top.configure(background='white')


#image
path = "./venv/stock.jpg"
path1 = Image.open(path)
resized = path1.resize((1400, 450), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(resized)
labelText = StringVar()
labelText.set("Welcome !!!!")

label1 = Label(top, image=image1, textvariable=labelText,
               font=("Times New Roman", 24),
               justify=LEFT, height=450, fg="red", text="Enter Stock").place(x=0, y=0)

#labels
Label(top, text="Enter Stock").place(x=600, y=475)
e1 = Entry(top)
e1.place(x=680,  y=475)

stockname = StringVar()
roc = StringVar()
stoch_os = StringVar()
asi = StringVar()
arima = StringVar()
pred = StringVar()
Label(top ,textvariable=stockname).place(x=600, y=550)
Label(top ,textvariable=roc).place(x=600, y=575)
Label(top ,textvariable=stoch_os).place(x=600, y=600)
Label(top ,textvariable=asi).place(x=600, y=625)
Label(top ,textvariable=arima).place(x=600, y=650)
Label(top ,textvariable=pred).place(x=600, y=675)


def buttonFunc():
    list = getPrediction(e1.get())
    if len(list) == 0:
        return
    stockname.set(list[0])
    roc.set("Rate of Change: " + list[1] + "%")
    stoch_os.set("Stochastic Oscillator: " + list[2] + "%")
    asi.set("Accumulated Swing Index: " + list[3])
    arima.set("ARIMA: $" + list[4])
    pred.set("Overall Prediction: $" + list[5])

#button
B1 = Button(top, text="Get Prediction", bg="green", fg="black", command=buttonFunc).place(x=650, y=525)
top.mainloop()
