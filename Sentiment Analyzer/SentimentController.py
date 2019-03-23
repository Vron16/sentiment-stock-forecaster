from SentimentCalculator import SentimentCalculator
from SentimentPredictor import SentimentPredictor
from Webscraper import Webscraper
import mysql.connector as ms

def main():
    sentCalculator = SentimentCalculator()
    webScraper = Webscraper()
    sentPredictor = SentimentPredictor()

    headlines = requestHeadlines(webScraper, "AAPL")
    avgScore = calcAvgSentScore(sentCalculator, headlines)
    print('Average Score of all Headlines Analyzed is: ' + str(avgScore))
    print(requestPrediction(sentPredictor, avgScore))
    updateDB(avgScore)
    #print sentCalculator.calculate("Microsoft's stock riding 7-day win streak toward another record close")
    #print sentCalculator.calculate("Alphabet (GOOGL) Dips More Than Broader Markets: What You Should Know")

def requestHeadlines(webScraper, ticker):
    return webScraper.getHeadlines(ticker)

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






if __name__ == '__main__':
    main()