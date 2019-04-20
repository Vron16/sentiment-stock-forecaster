import nltk
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentCalculator:
    def __init__(self):
        self.newsAnalyzer = SentimentIntensityAnalyzer()
        self.financeLexicon = {}
        with open("FinanceLexicon.txt") as dictFile:
            for line in dictFile:
                line = line.rstrip(',')
                (word, score) = line.split(',')
                self.financeLexicon[word] = int(eval(score))
        self.newsAnalyzer.lexicon.update(self.financeLexicon)
    def calculate(self, message):
        #message = "Alphabet (GOOGL) Dips More Than Broader Markets: What You Should Know"
        #isValid = 0
        #regex = re.compile("(\w[\w']*\w|\w)")
        #for msgWord in regex.findall(message):
         #   for lexWord in self.newsAnalyzer.lexicon:
          #      if (msgWord == lexWord):
           #         isValid = 1
            #        break
        #if (isValid == 0):
         #   return 2.0 #return 2 on error/none of the numbers match up
        ss = self.newsAnalyzer.polarity_scores(message)
        return ss["compound"] #otherwise, we know that at least one word in lexicon is in the input text and can assign proper score