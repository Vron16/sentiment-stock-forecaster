from SentimentCalculator import SentimentCalculator
from SentimentPredictor import SentimentPredictor
from Webscraper import Webscraper
import mysql.connector as ms
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


#######Create the GUI#######
top = Tk()
top.wm_title("Sentiment Analyzer")
top.geometry("1400x800")
top.configure(background='grey')

#######Import the picture to the GUI#######
path = "imagee.jpg"
path1 = Image.open(path)
resized = path1.resize((1400, 500), Image.ANTIALIAS)

image1 = ImageTk.PhotoImage(resized)
labelText = StringVar()
labelText.set("Welcome !!!!")

label1 = Label(top, image=image1, textvariable=labelText,
               font=("Times New Roman", 24),
               justify=LEFT, height=500, fg="red", text="Enter Stock").place(x=0, y=0)

#######Create the Enter Stock label on the GUI#######
Label(top, text="Enter Stock").place(x=600, y=553)
e1 = Entry(top)
e1.place(x=680,  y=550)


##########################################################
def main():
    sentCalculator = SentimentCalculator()
    webScraper = Webscraper()
    sentPredictor = SentimentPredictor()

    x = search_stock_symbol(e1.get())

    if x == 1:
        headlines = requestHeadlines(webScraper, e1.get())
        avgScore = calcAvgSentScore(sentCalculator, headlines)

        avgScore1 = str(avgScore)
        e11 = str(e1.get())

        updateDB(avgScore1, e11)

        messagebox.showinfo("Result",
                            " The first 5 headlines are: " + "\n" + printHeadlines(headlines)
                            + "\n\n" + "Average Score of all Headlines Analyzed is: " + str(avgScore)
                            + "\n\n" + requestPrediction(sentPredictor, avgScore))

    else:
        messagebox.showinfo("Result", "Stock name is not valid")


    #print sentCalculator.calculate("Microsoft's stock riding 7-day win streak toward another record close")
    #print sentCalculator.calculate("Alphabet (GOOGL) Dips More Than Broader Markets: What You Should Know")

def buttonFunc():
    main()


def requestHeadlines(webScraper, ticker):
    return webScraper.getHeadlines(ticker)


def printHeadlines(headlines):
    h = " "
    for i in range(5):
        h = h + "\n" + "- “" + headlines[i] + '”'
    return h


def calcAvgSentScore(sentimentCalculator, headlines):
    totalScore = 0
    numHeadlines = 0
    #isValid = 0 #initialized as false/assumes that all headlines get score of 2.0, aka no words from lexicon were in headline
    for headline in headlines:
        #print(headline)
        score = sentimentCalculator.calculate(headline)
        #print(score)
        #if (score != 2.0):
            #isValid = 1
        totalScore += score
        numHeadlines += 1
    return (totalScore/numHeadlines)


def requestPrediction(sentimentPredictor, averageSent):
    return sentimentPredictor.predict(averageSent)


def updateDB(sentiment, stockname):
    cnx = ms.connect(user='root', password='mypassword',
                     host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com',
                     database='mydb')

    mycursor = cnx.cursor()

    query = "SELECT stock_code FROM stock"

    mycursor.execute(query)
    result = mycursor.fetchall()
    print(sentiment)
    mycursor.execute("UPDATE stock SET sentiment = (%s) WHERE stock_code = (%s)", (sentiment, stockname))

    cnx.commit()
    print(stockname)

    cnx.close()

    #for x in result:
        #print(x)


def search_stock_symbol(stock_symbol):
    # connect to database
    cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com',
                     database='mydb')
    my_cursor = cnx.cursor()
    query = "SELECT stock_code FROM stock"
    my_cursor.execute(query)
    result = my_cursor.fetchall()

    for x in result:
        if x[0] == stock_symbol:
            return 1
    return 0
##########################################################


#######Create a calculate sentiment button#######
B1 = Button(top, text="Calculate Sentiment", bg="green", fg="black", command=buttonFunc).place(x=670, y=600)

#######Run the GUI#######
top.mainloop()
