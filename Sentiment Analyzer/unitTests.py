from SentimentCalculator import SentimentCalculator
from SentimentPredictor import SentimentPredictor
from SentimentController import search_stock_symbol

sentCalculator = SentimentCalculator()
sentPredictor = SentimentPredictor()

#Unit Test: SentimentCalculator calculate function
print(sentCalculator.calculate("Netflix Impresses with Abundance of Opportunities")) #strongly positive
print(sentCalculator.calculate("Uber's Incompetent Self-Driving Car Jeopardizes IPO Valuation")) #strongly negative
print(sentCalculator.calculate("Google Meets Expectations During Average Quarter")) #neutral statement

#Unit Test: SentimentPredictor predict function
print(sentPredictor.predict(0.065)) #strong rise
print(sentPredictor.predict(0.03)) #weak rise
print(sentPredictor.predict(0.02999)) #stagnant
print(sentPredictor.predict(-0.03)) #weak fall
print(sentPredictor.predict(-0.065)) #strong fall

#Unit Test: SentimentController search_stock_symbol function
print(search_stock_symbol("AAPL")) #returns 1
print(search_stock_symbol("Apple")) #returns 0
print(search_stock_symbol("aapl")) #returns 0
print(search_stock_symbol("AaPl")) #returns 0
