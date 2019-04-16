### PLEASE MAKE SURE YOU HAVE THE FOLlOWING PACKAGES:
### - STATSMODELS
### - SCIPY
### DATELINE SHOULD BE A DEFAULT PACKAGE
from statsmodels.tsa.arima_model import ARIMA
import datetime
import numpy as np

from numpy import fft

# ----------------- Rate of Change ------------------#

numDays = 5


def calculateROC(closing, now, nAgo):
    # calculate the ROC between two times (Formulas in report)
    diff = closing[now] - closing[nAgo]
    roc = (diff / closing[nAgo]) * 100
    return roc


def nDayRateOfChange(now, closing):
    # get all of the ROCs for all numDays periods into a list, return it
    rocs = []
    i = 0
    while i < len(closing) - numDays:
        answer = calculateROC(closing, i, i + numDays)
        rocs.append(answer)
        i += numDays
    return rocs


def printRocs(rocs):
    # helper function for unit tests
    print("ROCS:")
    for r in rocs:
        print(r)


# TODO: get closing by parsing through 5 min intervals list
def getClosingPrices(times, list):
    # get the closing prices for all days
    # because the stock market closes at 4pm, check if times[i].hour == 16
    prices = []
    for i in range(len(times)):
        if times[i].hour == 16:
            prices.append(list[i])
    return prices


def getRateOfChange(stockData):
    # store the time stamps and the closing prices
    times = stockData[0]
    fiveMinList = stockData[4]

    # get the rocs for a given period
    closing = getClosingPrices(times, fiveMinList)
    rocs = nDayRateOfChange(0, closing)
    return rocs


# ----------------- Stochastic Oscillator ------------------#

def calculateSO(closing, high, low, cur, now, nAgo):
    # calculate the stochastic oscillator for a given period (Formulas in report)
    highPrice = findHighest(high, now, nAgo)
    lowPrice = findLowest(low, now, nAgo)

    numer = cur - lowPrice
    denom = highPrice - lowPrice
    return (numer / denom) * 100


def findHighest(high, now, nAgo):
    # find the highest price in a list
    highPrice = 0
    i = nAgo
    while i >= now:
        if high[i] > highPrice:
            highPrice = high[i]

        i -= 1
    return highPrice


def findLowest(low, now, nAgo):
    # find the lowest price in a list
    lowPrice = float("inf")
    i = nAgo
    while i >= now:
        if low[i] < lowPrice:
            lowPrice = low[i]

        i -= 1
    return lowPrice


def nDayOscillation(num, closing, high, low, cur):
    # for every numDay period, get the stochastic oscillator, store in a list
    sos = []
    i = 0
    while i < len(closing) - num:
        answer = calculateSO(closing, high, low, cur, i, i + num)
        sos.append(answer)
        i += num
    return sos


def printSO(so):
    # helper function for unit tests
    print("SO:")
    for s in so:
        print(s)


def getClosingPrices(times, list):
    # get the closing price for all days
    prices = []
    for i in range(len(times)):
        if times[i].hour == 16:
            prices.append(list[i])
    return prices


def getHighPrices(times, list):
    # get the highest price for all days
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
    # get the lowest price for all days
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
    # store the time stamps, high prices, low prices, and closing prices for every five minute interval
    times = stockData[0]
    highFiveMinList = stockData[1]
    lowFiveMinList = stockData[2]
    fiveMinList = stockData[4]

    # prices list and current price
    closing = getClosingPrices(times, fiveMinList)
    high = getHighPrices(times, highFiveMinList)
    low = getLowPrices(times, lowFiveMinList)
    cur = getCurPrice(fiveMinList)

    # get list of stock oscillations for all numDay peridss
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

    # Perform the ASI calculations (Formulas in report)
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
    # store the time stamps and the high prices
    times = stock_Data[0]
    high_prices = stock_Data[1]

    todaySamples = 0
    yesterdaySamples = 0

    ASI = []

    # Find all of the prices for a single day, call getSwing() to get Swing Index for that day
    # Append the swing for each day into ASI
    for k in range(len(times) - 1):
        todaySamples += 1
        if times[k + 1].hour == 16:
            if yesterdaySamples != 0 and todaySamples != 0:
                ASI.append(getSwing(high_prices[0: k], yesterdaySamples, todaySamples))
            yesterdaySamples = todaySamples
            todaySamples = 0

    ASI.reverse()

    return ASI


# ----------------- ARIMA ------------------#


def getARIMA(stock_data):
    # Because the stock prices are reveresed, we push each price to the front of data
    data = []
    for i in stock_data:
        data = [i] + data

    # fc will hold the forecast made by ARIMA
    fc = -1
    if (len(data) < 1):  # if the list is empty, return -1
        return fc

    # p is a parameter for the ARIMA model, and can act as a looping iterator
    p = 5
    while (1):
        try:  # we try to fit the data to the ARIMA model, with p initially at 5
            if (p == 0):  # base case condition: if we looped five times already,
                # there wasn't enough stock data to make a meaningful prediction, return -2
                return -2
            model = ARIMA(data, order=(p, 1, 0))
            model_fit = model.fit(disp=0)
            # if the model fits, we can ask it to make a prediction, and return it
            fc = model_fit.forecast()[0][0]
            return fc
        except:  # the model could not fit, so we try again by decrementing p
            p -= 1

    return fc


def fourierExtrapolation(stock_data, n_predict):
    n = stock_data.size
    n_harm = 10  # number of harmonics in model
    t = np.arange(0, n)
    p = np.polyfit(t, stock_data, 1)  # find linear trend in x
    stock_data_notrend = stock_data - p[0] * t  # detrended x
    stock_data_freqdom = fft.fft(stock_data_notrend)  # detrended x in frequency domain
    f = fft.fftfreq(n)  # frequencies
    indexes = list(range(n))
    # sort indexes by frequency, lower -> higher
    indexes.sort(key=lambda i: np.absolute(f[i]))

    t = np.arange(0, n + n_predict)
    restored_sig = np.zeros(t.size)
    for i in indexes[:1 + n_harm * 2]:
        ampli = np.absolute(stock_data_freqdom[i]) / n  # amplitude
        phase = np.angle(stock_data_freqdom[i])  # phase
        restored_sig += ampli * np.cos(2 * np.pi * f[i] * t + phase)
    return restored_sig + p[0] * t


def getFourier(stock_data):
    data = []
    for i in stock_data:
        data = [i] + data

    np_stock_data = np.array(data)
    n_predict = 3
    extrapolation = fourierExtrapolation(np_stock_data, n_predict)
    # pl.plot(np.arange(0, extrapolation.size), extrapolation, 'r', label='extrapolation')
    # pl.plot(np.arange(0, np_stock_data.size), np_stock_data, 'b', label='stock_data', linewidth=3)
    # pl.legend()
    # pl.show()
    print(extrapolation)
    print(extrapolation[-3])
    print(extrapolation[-2])
    print(extrapolation[-1])
    # print(np_stock_data.size)
    # print (extrapolation.size)
    predicted = []
    for i in range(n_predict):
        predicted.append(extrapolation[-1 * (n_predict - i)])
    return predicted


def aggregatePrediction(roc, stoch_os, asi, arima_prediction, fourier_prediction):
    # This is our averager. For the purpose of the demo here we printed all of our results and returned the ARIMA prediction
    print("Rate of change: ", roc[0])
    print("Stochastic Oscillator: ", stoch_os[0])
    print("Accumulative Swing Index: ", asi[0])

    print("Unweighted ARIMA Prediction: ", arima_prediction)
    print("Unweighted Fourier Predictions: ", fourier_prediction)

    weight_ar = arima_prediction
    weight_four = fourier_prediction[0]

    weight_ar = weight_ar + 0.1*roc[0]
    weight_four = weight_four + 0.1 * roc[0]

    if stoch_os[0] > 50:
        weight_ar = weight_ar - 0.1
        weight_four = weight_four - 0.1


    weight_ar = weight_ar + 0.1 * asi[0]
    weight_four = weight_four + 0.1 * asi[0]

    print("Weighted ARIMA Prediction: ", weight_ar)
    print("Weighted Fourier Prediction: ", weight_four)

    return arima_prediction
