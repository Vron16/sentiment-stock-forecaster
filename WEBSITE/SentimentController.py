from WEBSITE.SentimentCalculator import SentimentCalculator
from WEBSITE.SentimentPredictor import SentimentPredictor
from WEBSITE.Webscraper import Webscraper
import mysql.connector as ms
import csv

class SentimentController:
    def handleAutoTradeRequest(self, ticker):
        headlines = self.requestHeadlines(ticker)
        avgScore = self.calcAvgSentScore( headlines)
        self.updateDB(avgScore)
        return avgScore

    def finalToUser(self, ticker):
        headlines = self.requestHeadlines(ticker)
        avgScore = self.calcAvgSentScore(headlines)
        k = 'Average Sentiment Score of all Headlines Analyzed is: ' + str(avgScore)
        l = self.requestPrediction(avgScore)
        array = [k, l]
        return array

    def requestHeadlines(self, ticker):
        webScraperr = Webscraper()
        return webScraperr.getHeadlines(ticker)

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
        print(sentiment)
        mycursor.execute("UPDATE stock SET sentiment = (%s) WHERE stock_code = (%s)", (sentiment, stockname))

        cnx.commit()
        #print(stockname)

        cnx.close()

        #for x in result:
            #print(x)

    def getStockTickers(self):
        with open("stocksindb.csv", "r") as dbcsvFile:
            dbTickers = csv.reader(dbcsvFile, dialect='excel', delimiter=',', quotechar='"')
            tickers = []
            count = 0
            for row in dbTickers:
                if count == 0:
                    count = count + 1
                    continue
                ticker = row[1] + ' (' + row[0] + ')'
                tickers.append(ticker)
        return tickers


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
