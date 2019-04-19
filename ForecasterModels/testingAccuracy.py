import techController
import mm

def getOutputtedPrediction(stock_name):
    stock_data = techController.getStockData(stock_name)

    lastTime = stock_data[0].pop()
    lastOpen = stock_data[1].pop()
    lastClose = stock_data[4].pop()
    lastHigh = stock_data[2].pop()
    lastLow = stock_data[3].pop()

    roc = mm.getRateOfChange(stock_data)  # array
    stoch_os = mm.getStochasticOscillator(stock_data)  # array
    asi = mm.getASI(stock_data)  # array
    arima_prediction = mm.getARIMA(stock_data[4])  # double
    fourier_prediction = mm.getFourier(stock_data[4])[0]

    prediction = mm.aggregatePrediction(roc, stoch_os, asi, arima_prediction, fourier_prediction)
    return [prediction, arima_prediction,fourier_prediction,lastClose]

def getPerr(predicted, actual):
    return abs((predicted - actual)/actual*100)

def getAvgError(perrs):
    total = 0
    for num in perrs:
        total += num
    total /= len(perrs)
    return total

listOfStockNames = ["AAPL","AA", "A", "AAL" , "AABA", "AAC",  "AAOI", "AAON", "AAP",
                    "AAT", "AAU", "AAWW", "AAXN", "AB", "ABB", "ABBV", "ABC", "ABCB",
                    "ABDC", "ABEO", "ABEV", "ABG", "ABIL", "ABIO", "ABM", "ABMD", "ABR",
                    "NFLX"]

predictions = []
arima_predictions = []
fourier_predictions = []
actualPrices = []

for name in listOfStockNames:
    print(name)
    data = getOutputtedPrediction(name)
    predictions.append(data[0])
    arima_predictions.append(data[1])
    fourier_predictions.append(data[2])
    actualPrices.append(data[3])

print("predictions are.........")
print(predictions)
print(arima_predictions)
print(fourier_predictions)
print("actual prices are.....")
print(actualPrices)

percentErrors = []
arima_perrs = []
fourier_perrs = []

for i in range(len(predictions)):
    percentErrors.append(getPerr(predictions[i],actualPrices[i]))
    arima_perrs.append(getPerr(arima_predictions[i],actualPrices[i]))
    fourier_perrs.append(getPerr(fourier_predictions[i],actualPrices[i]))

print("percent errors are...")
print(percentErrors)
print(arima_perrs)
print(fourier_perrs)
print("average ARIMA error")
print(getAvgError(arima_perrs))
print("average Fourier first extrapolation error")
print(getAvgError(fourier_perrs))