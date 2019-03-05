import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

newsAnalyzer = SentimentIntensityAnalyzer()
financeLexicon = {}
with open("FinanceLexicon.txt") as dictFile:
    for line in dictFile:
        line = line.rstrip()
        (word, score) = line.split(',')
        financeLexicon[word] = score
print financeLexicon