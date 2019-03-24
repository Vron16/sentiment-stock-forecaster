from statsmodels.tsa.arima_model import ARIMA


#----------------- Rate of Change ------------------#

numDays = 1

def calculateROC(closing, now, nAgo):
    diff = closing[now]-closing[nAgo]
    roc = (diff/closing[nAgo])*100
    return roc

def nDayRateOfChange(now, closing):
    rocs = []
    i = 0
    while i < len(closing) - numDays:
        answer = calculateROC(closing, i, i+numDays)
        rocs.append(answer)
        i += numDays
    return rocs

def printRocs(rocs):
    print("ROCS:")
    for r in rocs:
        print(r)

#TODO: get closing by parsing through 5 min intervals list
def getClosingPrices(times, list):
    prices = []
    for i in range(len(times)):
        if times[i].hour == 16:
            prices.append(list[i])
    return prices

def getRateOfChange(stockData):
    times = stockData[0]
    fiveMinList = stockData[4]

    closing = getClosingPrices(times, fiveMinList)
    rocs = nDayRateOfChange(0, closing)
    return rocs


#----------------- Stochastic Oscillator ------------------#

numDays = 1

def calculateSO(closing, high, low, cur, now, nAgo):
    highPrice = findHighest(high, now, nAgo)
    lowPrice = findLowest(low, now, nAgo)

    numer = cur - lowPrice
    denom = highPrice - lowPrice
    return (numer/denom) * 100


def findHighest(high, now, nAgo):
    highPrice = 0
    i = nAgo
    while i >= now:
        if high[i] > highPrice:
            highPrice = high[i]

        i -= 1
    return highPrice


def findLowest(low, now, nAgo):
    lowPrice = float("inf")
    i = nAgo
    while i >= now:
        if low[i] < lowPrice:
            lowPrice = low[i]

        i -= 1
    return lowPrice


def nDayOscillation(num,closing,high,low,cur):
    sos = []
    i = 0
    while i < len(closing):
        answer = calculateSO(closing, high, low, cur, i, i+num)
        sos.append(answer)
        i+=num
    return sos


def printSO(so):
    print("SO:")
    for s in so:
        print(s)

def getClosingPrices(times, list):
    prices = []
    for i in range(len(times)):
        if times[i].hour == 16:
            prices.append(list[i])
    return prices

#TODO: get high by parsing through 5 min intervals list
def getHighPrices(times, list):
    prices = []
    highest = 0
    for i in range(len(times)):
        if list[i] > highest:
            highest = list[i]
        if times[i].hour == 16:
            prices.append(highest)
            highest = 0
    return prices

#TODO: get low by parsing through 5 min intervals list
def getLowPrices(times, list):
    prices = []
    lowest = float("inf")
    for i in range(len(times)):
        if list[i] < lowest:
            lowest = list[i]
        if times[i].hour == 16:
            prices.append(lowest)
            lowest = float("inf")
    return prices

def getCurPrice(list):
    #newest price at the beginning of list
    return list[0]

def getStochasticOscillator(stockData):
    times = stockData[0]
    highFiveMinList = stockData[1]
    lowFiveMinList = stockData[2]
    fiveMinList = stockData[4]

    #prices list and current price
    closing = getClosingPrices(times, fiveMinList)
    high = getHighPrices(times, highFiveMinList)
    low = getLowPrices(times, lowFiveMinList)
    cur = getCurPrice(fiveMinList)

    so = nDayOscillation(numDays, closing, high, low, cur)
    return so


#----------------- ARIMA ------------------#


def getARIMA(stock_data):
    
    stock_data.reverse();
    fc = -1
    if(len(stock_data) < 1):
        return fc
    
    p = 5
    while(1):
        try:
            if(p == 0):
                return -2
            #print("p: ", p)
            model = ARIMA(stock_data, order=(p,1,0))
            model_fit = model.fit(disp=0)
    
            fc = model_fit.forecast()[0][0]
            return fc
        except:
            print("Unexpected error:", sys.exc_info()[0])
            p-=1
        
    return fc

def aggregatePrediction(roc, stoch_os, asi, arima_prediction):
    
    print("Rate of change: ", roc[0])
    print("Stochastic Oscillator: ", stoch_os[0])
    print("Accumulative Swing Index: ", asi)
    print("ARIMA Prediction: ", arima_prediction)
    
    return arima_prediction
