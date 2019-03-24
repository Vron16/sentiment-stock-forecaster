class SentimentPredictor:
    def __init__(self):
        self.prediction = ''

    def predict(self, score):
        if (score == 2.0):
            self.prediction = 'The Sentiment Analyzer did not have enough data to make an accurate prediction for the provided stock.'
        elif (score >= 0.65 and score <= 1.0):
            self.prediction = 'Due to strong positive sentiment about this stock, the price of the stock is expected to experience a STRONG RISE based on sentiment only.'
        elif (score >= 0.3 and score < 0.65):
            self.prediction = 'Due to weak positive sentiment about this stock, the price of the stock is expected to experience a WEAK RISE based on sentiment only.'
        elif (score < 0.3 and score > -0.3):
            self.prediction = 'Due to neutral sentiment about this stock, the price of the stock is expected to remain relatively stagnant based on sentiment only.'
        elif (score <= -0.3 and score > -0.65):
            self.prediction = 'Due to weak negative sentiment about this stock, the price of the stock is expected to experience a WEAK FALL based on sentiment only.'
        else:
            self.prediction = 'Due to strong negative sentiment about this stock, the price of the stock is expected to experienced a STRONG FALL based on sentiment only.'
        return self.prediction
