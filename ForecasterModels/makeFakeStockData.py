import random

def generateFakeStock(startPrice,lowVar,highVar,numberOfDataPoints):
    stock = []
    stock.append(startPrice)
    i = 0;
    while i < numberOfDataPoints:
        stock.append(stock[i] + random.uniform(lowVar,highVar))
        i += 1
    return stock


#print(generateFakeStock(10000,-200,400,30))