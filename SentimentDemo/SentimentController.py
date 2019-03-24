from SentimentCalculator import SentimentCalculator
from SentimentPredictor import SentimentPredictor
from Webscraper import Webscraper
import mysql.connector as ms


from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

top = Tk()
top.wm_title("Sentiment Analyzer")
top.geometry("1400x800")
top.configure(background='grey')

######big label
path = "imagee.jpg"
path1 = Image.open(path)
resized = path1.resize((1400, 500), Image.ANTIALIAS)

image1 = ImageTk.PhotoImage(resized)
labelText = StringVar()
labelText.set("Welcome !!!!")

label1 = Label(top, image=image1, textvariable=labelText,
               font=("Times New Roman", 24),
               justify=LEFT, height=500, fg="red", text="Enter Stock").place(x=0, y=0)


#######small label
Label(top, text="Enter Stock").place(x=600, y=553)
e1 = Entry(top)
e1.place(x=680,  y=550)


##########################################################
def main():
    #messagebox.showinfo("Result", "Hello World")

    sentCalculator = SentimentCalculator()
    webScraper = Webscraper()
    sentPredictor = SentimentPredictor()

    headlines = requestHeadlines(webScraper, e1.get())
    avgScore = calcAvgSentScore(sentCalculator, headlines)



    #print('Average Score of all Headlines Analyzed is: ' + str(avgScore))
    #print(requestPrediction(sentPredictor, avgScore))

    messagebox.showinfo("Result",
                        " The first 5 headlines are: " + "\n" + printHeadlines(headlines)
                        + "\n\n" + "Average Score of all Headlines Analyzed is: " + str(avgScore)
                        + "\n\n" + requestPrediction(sentPredictor, avgScore))

    #messagebox.showinfo("Say Hello", 'Average Score of all Headlines Analyzed is: ' + str(avgScore) + '\n' + '\n' + requestPrediction(sentPredictor, avgScore) + '\n')
    #updateDB(avgScore)
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
        print(headline)
        score = sentimentCalculator.calculate(headline)
        print(score)
        #if (score != 2.0):
            #isValid = 1
        totalScore += score
        numHeadlines += 1
    return (totalScore/numHeadlines)

def requestPrediction(sentimentPredictor, averageSent):
    return sentimentPredictor.predict(averageSent)

def updateDB(sentiment):
    cnx = ms.connect(user='root', password='mypassword',
                     host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com',
                     database='mydb')
    mycursor = cnx.cursor()

    query = "SELECT stock_code FROM stock"

    mycursor.execute(query)
    result = mycursor.fetchall()

    for x in result:
        print(x)


#if __name__ == '__main__':
 #   main()


##########################################################


#e1.get() -- gets the stock name

B1 = Button(top, text="Calculate Sentiment", bg="green", fg="black", command=buttonFunc).place(x=670, y=600)
top.mainloop()
