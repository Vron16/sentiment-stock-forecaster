from SentimentCalculator import SentimentCalculator
from SentimentPredictor import SentimentPredictor
from Webscraper import Webscraper
import mysql.connector as ms
import csv
import matplotlib.pyplot as plt


class SentimentController:

    def trend(self, ticker):
        headlines5 = self.requestHeadlines(ticker)
        headlines20 = self.requestHeadlines20(ticker)
        headlines30 = self.requestHeadlines30(ticker)
        avgScore5 = self.calcAvgSentScore(headlines5)
        avgScore20 = self.calcAvgSentScore(headlines20)
        avgScore30 = self.calcAvgSentScore(headlines30)
        x = [5, 20, 30]
        y = [avgScore5, avgScore20, avgScore30]
        plt.plot(x, y)
        plt.xlabel('Time in days')
        plt.ylabel('Sentiment score')
        plt.title('Sentiment Trend!')

        plt.tight_layout()
        plt.savefig('static/assets/img/testplot.png')


        # im = Image.open("static/assets/img/testplot.png")
        # rgb_im = im.convert('RGB')
        # rgb_im.save('static/assets/img/testplot.jpg')
        plt.clf()
        return

    def handleAutoTradeRequest(self, ticker):
        headlines = self.requestHeadlines(ticker)
        avgScore = self.calcAvgSentScore( headlines)
        #self.updateDB(avgScore)
        return avgScore

    def finalToUser(self, parsedHeadlines):
        #headlines = self.requestHeadlines(ticker)
        avgScore = self.calcAvgSentScore(parsedHeadlines)
        k = 'Average Sentiment Score of all Headlines Analyzed is: ' + str(avgScore)
        l = self.requestPrediction(avgScore)
        array = [k, l]
        return array

    def requestHeadlines(self, ticker):
        webScraperr = Webscraper()
        return webScraperr.getHeadlines(ticker)

    def requestHeadlines20(self, ticker):
        webScraperr = Webscraper()
        return webScraperr.getHeadlines20(ticker)

    def requestHeadlines30(self, ticker):
        webScraperr = Webscraper()
        return webScraperr.getHeadlines30(ticker)

    def printHeadlines(self, headlines):
        h = " "
        for i in range(3):
            h = h + "\n" + "- “" + headlines[i] + '”'
        print(h)

    def calcAvgSentScore(self, headlines):
        senttCalculator = SentimentCalculator()
        totalScore = 0
        numHeadlines = 0
        for headline in headlines:
            score = senttCalculator.calculate(headline)
            totalScore += score
            numHeadlines += 1
        return (totalScore/numHeadlines)

    def calculateSingleScore(self, ticker):
        sentCalculator = SentimentCalculator()
        return sentCalculator.calculate(ticker)

    def requestPrediction(self, averageSent):
        senttPredictor = SentimentPredictor()
        return senttPredictor.predict(averageSent)

    def updateDB(sentiment, stockname):
        cnx = ms.connect(user='root', password='mypassword',
                     host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com',
                     database='mydb')

        mycursor = cnx.cursor()

        query = "SELECT stock_code FROM stock"

        mycursor.execute(query)
        result = mycursor.fetchall()
        #print(sentiment)
        #mycursor.execute("UPDATE stock SET sentiment = (%s) WHERE stock_code = (%s)", (sentiment, stockname))

        cnx.commit()
        #print(stockname)

        cnx.close()

        #for x in result:
            #print(x)

    def getStockTickers(self, symbol):
        with open("stocksindb.csv", "r") as dbcsvFile:
            dbTickers = csv.reader(dbcsvFile, dialect='excel', delimiter=',', quotechar='"')
            count = 0
            ticker = ''
            for row in dbTickers:
                if count == 0:
                    count = count + 1
                    continue
                if row[0] == symbol:
                    ticker = row[1]
                    break
        return ticker




    # def search_stock_symbol(stock_symbol):
    #     # connect to database
    #     cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com',
    #                  database='mydb')
    #     my_cursor = cnx.cursor()
    #     query = "SELECT stock_code FROM stock"
    #     my_cursor.execute(query)
    #     result = my_cursor.fetchall()
    #
    #     for x in result:
    #         if x[0] == stock_symbol:
    #             return 1
    #     return 0