from SentimentCalculator import SentimentCalculator
from SentimentPredictor import SentimentPredictor
from Webscraper import Webscraper
import mysql.connector as ms

class SentimentController:
    def handleAutoTradeRequest(self, ticker):
        sentCalculator = SentimentCalculator()
        webScraper = Webscraper()
        #sentPredictor = SentimentPredictor()

        headlines = self.requestHeadlines(webScraper, ticker)
        avgScore = self.calcAvgSentScore(sentCalculator, headlines)
        #print('Average Score of all Headlines Analyzed is: ' + str(avgScore))
        #print(requestPrediction(sentPredictor, avgScore))
        self.updateDB(avgScore)
        return avgScore
        #print sentCalculator.calculate("Microsoft's stock riding 7-day win streak toward another record close")
        #print sentCalculator.calculate("Alphabet (GOOGL) Dips More Than Broader Markets: What You Should Know")

    #def buttonFunc():
        #main()


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