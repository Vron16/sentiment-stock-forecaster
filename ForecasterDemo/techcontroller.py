import mysql.connector as ms
import datetime
import mm

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


prediction = 0


# Connects to the database and get times and prices
def getStockData(stock_name):
    # connect to database
    cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com',
                     database='mydb')
    mycursor = cnx.cursor()

    # query the information
    query = "SELECT datetime, open, high, low, close FROM day_price WHERE stock_code = '" + stock_name + "'"
    mycursor.execute(query)
    result = mycursor.fetchall()

    # Return information
    time_stamps = [i[0] for i in result]
    open_prices = [i[1] for i in result]
    close_prices = [i[4] for i in result]
    high_prices = [i[2] for i in result]
    low_prices = [i[3] for i in result]

    cnx.close()
    return (time_stamps, high_prices, low_prices, open_prices, close_prices)

# Gets predictions from various models
def getPrediction(stock_name):
    stock_data = getStockData(stock_name)

    # if no prices information, invalid stock
    if len(stock_data[0]) == 0:
        messagebox.showinfo("Invalid stock name", "Invalid stock name, please try again")
        return []

    # get model values
    roc = mm.getRateOfChange(stock_data)  # array
    stoch_os = mm.getStochasticOscillator(stock_data)  # array
    asi = mm.getASI(stock_data)  # array
    arima_prediction = mm.getARIMA(stock_data[4])  # double
    currentprice = stock_data[4][0]

    # send to model averager and receive final prediction
    prediction = mm.aggregatePrediction(roc, stoch_os, asi, arima_prediction)

    # return information to be displayed to the user
    ret = []
    ret.append(stock_name)
    ret.append(str(round(roc[0],5)))
    ret.append(str(round(stoch_os[0],5)))
    ret.append(str(round(asi[0],5)))
    ret.append(str(round(currentprice)))
    ret.append(str(round(arima_prediction,5)))
    ret.append(str(round(prediction,5)))
    return ret

# Stores our prediction in the database
# TODO: complete this
def storePrediction():
    # cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com', database='mydb')
    # mycursor = cnx.cursor()

    # query = "SELECT datetime, open, high, low, close FROM day_price WHERE stock_code = '" + stock_name + "'"
    # mycursor.execute(query)
    # cnx.close()
    return


# main, integration test

# set up tkinter GUI
top = Tk()
top.wm_title("Technical Forecaster")
top.geometry("1400x800")
top.configure(background='white')


# image on
path = "./venv/stock.jpg"
path1 = Image.open(path)
resized = path1.resize((1400, 450), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(resized)
labelText = StringVar()
labelText.set("Welcome !!!!")

label1 = Label(top, image=image1, textvariable=labelText,
               font=("Times New Roman", 24),
               justify=LEFT, height=450, fg="red", text="Enter Stock").place(x=0, y=0)

# labels
Label(top, text="Enter Stock", font="Helvetica 14", ).place(x=650, y=460)
e1 = Entry(top)
e1.place(x=650,  y=485)

# set up labels and variables to be filled in
stockname = StringVar()
roc = StringVar()
stoch_os = StringVar()
asi = StringVar()
cur = StringVar()
arima = StringVar()
pred = StringVar()
color = StringVar()
Label(top, textvariable=stockname, font="Helvetica 16 bold").place(x=600, y=550)
Label(top, textvariable=roc, font="Helvetica 14").place(x=600, y=575)
Label(top, textvariable=stoch_os, font="Helvetica 14").place(x=600, y=600)
Label(top, textvariable=asi, font="Helvetica 14").place(x=600, y=625)
Label(top, textvariable=cur, font="Helvetica 14").place(x=600, y=650)
Label(top, textvariable=arima, font="Helvetica 14").place(x=600, y=675)
Label(top, textvariable=pred, font="Helvetica 14").place(x=600, y=700)


# when button clicked
def buttonFunc():
    # get prediction information to be displayed
    list = getPrediction(e1.get())

    if len(list) == 0:
        return

    # fill in stock name
    stockname.set(list[0].upper())

    # ROC, red if less than zero, green if greater than zero
    roc.set("Rate of Change: " + list[1] + "%")
    if float(list[1]) < 0:
        Label(top, textvariable=roc, font="Helvetica 14", fg="red").place(x=600, y=575)
    else:
        Label(top, textvariable=roc, font="Helvetica 14", fg="green").place(x=600, y=575)

    # Stochastic Oscillator, red if greater than 50, green if less than 50
    stoch_os.set("Stochastic Oscillator: " + list[2] + "%")
    if float(list[2]) > 50:
        Label(top, textvariable=stoch_os, font="Helvetica 14", fg="red").place(x=600, y=600)
    else:
        Label(top, textvariable=stoch_os, font="Helvetica 14", fg="green").place(x=600, y=600)

    # ASI, red if less than zero, green if greater than zero
    asi.set("Accumulated Swing Index: " + list[3])
    if float(list[3]) < 0:
        Label(top, textvariable=asi, font="Helvetica 14", fg="red").place(x=600, y=625)
    else:
        Label(top, textvariable=asi, font="Helvetica 14", fg="green").place(x=600, y=625)

    cur.set("Current Price: $" + list[4])

    # ARIMA, red if less than cur price, green if greater than cur price
    arima.set("ARIMA Prediction: $" + list[5])
    if float(list[4]) > float(list[5]):
        Label(top, textvariable=arima, font="Helvetica 14", fg="red").place(x=600, y=675)
    else:
        Label(top, textvariable=arima, font="Helvetica 14", fg="green").place(x=600, y=675)

    # overall prediction, red if less than cur price, green if greater than cur price
    pred.set("Overall Prediction: $" + list[6])
    if float(list[4]) > float(list[6]):
        Label(top, textvariable=pred, font="Helvetica 14", fg="red").place(x=600, y=700)
    else:
        Label(top, textvariable=pred, font="Helvetica 14", fg="green").place(x=600, y=700)


# button setting
B1 = Button(top, text="Get Prediction", bg="green", fg="black", command=buttonFunc).place(x=650, y=515)

# run GUI
top.mainloop()
