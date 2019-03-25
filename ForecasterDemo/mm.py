from statsmodels.tsa.arima_model import ARIMA
import datetime

# ----------------- Rate of Change ------------------#

numDays = 5


def calculateROC(closing, now, nAgo):
    diff = closing[now] - closing[nAgo]
    roc = (diff / closing[nAgo]) * 100
    return roc


def nDayRateOfChange(now, closing):
    rocs = []
    i = 0
    while i < len(closing) - numDays:
        answer = calculateROC(closing, i, i + numDays)
        rocs.append(answer)
        i += numDays
    return rocs


def printRocs(rocs):
    print("ROCS:")
    for r in rocs:
        print(r)


# TODO: get closing by parsing through 5 min intervals list
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


# ----------------- Stochastic Oscillator ------------------#

def calculateSO(closing, high, low, cur, now, nAgo):
    highPrice = findHighest(high, now, nAgo)
    lowPrice = findLowest(low, now, nAgo)

    numer = cur - lowPrice
    denom = highPrice - lowPrice
    return (numer / denom) * 100


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


def nDayOscillation(num, closing, high, low, cur):
    sos = []
    i = 0
    while i < len(closing) - num:
        answer = calculateSO(closing, high, low, cur, i, i + num)
        sos.append(answer)
        i += num
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
    # newest price at the beginning of list
    return list[0]


def getStochasticOscillator(stockData):
    times = stockData[0]
    highFiveMinList = stockData[1]
    lowFiveMinList = stockData[2]
    fiveMinList = stockData[4]

    # prices list and current price
    closing = getClosingPrices(times, fiveMinList)
    high = getHighPrices(times, highFiveMinList)
    low = getLowPrices(times, lowFiveMinList)
    cur = getCurPrice(fiveMinList)

    so = nDayOscillation(numDays, closing, high, low, cur)
    return so



# -------------------ASI--------------------

def getSwing(stock_Data, priceSamplesPerDay, priceSamplesToday):
    length = len(stock_Data)
    t = 100  # t has to be user defined, not sure what a good number is
    O = stock_Data[length - 1]  # today's closing price
    Oy = stock_Data[length - 1 - priceSamplesToday]  # yesterdays closing price
    C = stock_Data[length - priceSamplesToday]  # today's opening price
    Cy = stock_Data[length - priceSamplesToday - priceSamplesPerDay]  # yesterdays opening price

    yesterdaysPrices = []  # make a list of yesterdays prices
    i = 0  # counter
    Hy = 0  # yesterdays high price
    Ly = Cy  # yesterdays low price
    while i < priceSamplesPerDay:
        yesterdaysPrices.append(stock_Data[length - priceSamplesToday - priceSamplesPerDay + i])
        if yesterdaysPrices[i] > Hy:
            Hy = yesterdaysPrices[i]
        if yesterdaysPrices[i] < Ly:
            Ly = yesterdaysPrices[i]
        i += 1

    todaysPrices = []
    i = 0
    H = 0
    L = C
    while i < priceSamplesToday:
        todaysPrices.append(stock_Data[length - priceSamplesToday + i])
        if todaysPrices[i] > H:
            H = todaysPrices[i]
        if todaysPrices[i] < L:
            L = todaysPrices[i]
        i += 1

    K = max(H - Cy, Cy - L)
    TR = max(H - Cy, L - Cy, H - L)

    if TR == H - Cy:
        R = (H - C) - .5 * (L - C) - .25 * (Cy - Oy)
    elif TR == L - Cy:
        R = L - Cy - .5 * (H - O) + .25 * (Cy - Oy)
    else:
        R = H - L + .25 * (Cy - Oy)

    swing = 50 * (Cy - C + .5 * (Cy - Oy) + .25 * (C - O) / R) * K / t

    return swing


# To get ASI you get the swing for every day in the dataset

def getASI(stock_Data):
    times = stock_Data[0]
    high_prices = stock_Data[1]

    todaySamples = 0
    yesterdaySamples = 0

    ASI = []
    for k in range(len(times)-1):
        todaySamples += 1
        if times[k + 1].hour == 16:
            if yesterdaySamples != 0 and todaySamples != 0:
                ASI.append(getSwing(high_prices[0 : k], yesterdaySamples, todaySamples))
            yesterdaySamples = todaySamples
            todaySamples = 0

    ASI.reverse()

    return ASI

# ----------------- ARIMA ------------------#


def getARIMA(stock_data):
    #stock_data.reverse()
    data = []
    for i in stock_data:
        data = [i] + data

    fc = -1
    if (len(data) < 1):
        return fc

    p = 5
    while (1):
        try:
            if (p == 0):
                return -2
            model = ARIMA(data, order=(p, 1, 0))
            model_fit = model.fit(disp=0)
            fc = model_fit.forecast()[0][0]
            return fc
        except:
            p -= 1

    return fc


def aggregatePrediction(roc, stoch_os, asi, arima_prediction):

    print("Rate of change: ", roc[0])
    print("Stochastic Oscillator: ", stoch_os[0])
    print("Accumulative Swing Index: ", asi[0])
    print("ARIMA Prediction: ", arima_prediction)

    return arima_prediction
