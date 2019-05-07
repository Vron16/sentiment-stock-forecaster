#written by: Sunny Feng, Nicholas Heah, Manish Kewalramani
#tested by: Sunny Feng, Nicholas Heah, Manish Kewalramani
#debugged by: Sunny Feng, Nicholas Heah, Manish Kewalramani

import techController
import mm
import csv

#This function modifies our original getPrediction function to output more data
#in a more workable format so we can check accuracies
def getOutputtedPrediction(stock_name):
    stock_data = techController.getStockData(stock_name)
    num_predictions = 36 # HAS TO be at most as much as num_predictions in Fourier Model

    lastCloses = []
    for i in range(num_predictions):
        stock_data[0].pop(0)
        stock_data[1].pop(0)
        lastCloses.append(stock_data[4].pop(0))
        currentClose = stock_data[4][0]
        stock_data[2].pop(0)
        stock_data[3].pop(0)

    roc = mm.getRateOfChange(stock_data)  # array
    stoch_os = mm.getStochasticOscillator(stock_data)  # array
    asi = mm.getASI(stock_data)  # array
    data = []
    for i in stock_data[4]:
        data = [i] + data

    arima_prediction = mm.getARIMA(data)  # double
    fourier_predictions = mm.getFourier(data)

    prediction = mm.aggregatePrediction( roc, stoch_os, asi,currentClose, arima_prediction, fourier_predictions)
    print(prediction)
    
    return [prediction[0], prediction[1], arima_prediction, fourier_predictions,lastCloses]

#this function gets a percentage error between a predicted and an actual data point
def getPerr(predicted, actual):
    return abs((predicted - actual)/actual*100)

#this function gets the average percentage error for an array of percentage errors
def getAvgError(perrs):
    total = 0
    for num in perrs:
        total += num
    total /= len(perrs)
    return total

#get the absolute difference between a prediction and an actual point
def getDifference(predicted, actual):
    return abs(predicted-actual)

# the list of stock names in our database we can use to test our predictions
listOfStockNames =  ["AAPL","AA", "A", "AAL", "AABA", "AAC",  "AAOI", "AAN", "AAON", "AAP",
                    "AAT", "AAU", "AAWW", "AAXJ", "AAXN", "AB", "ABB", "ABBV", "ABC", "ABCB",
                    "ABDC", "ABEO", "ABG", "ABIL", "ABM", "ABMD", "ABR", "AADR", #took out ABIO
                    "ACST", "ACRX", "ACRS", "ACRE", "ACP", "NFLX", #took out ACSG
                    "ACOR", "ACNB", "ACN", "ACMR", "ACM", "ACLS","ACIW", "ACIU", "ACIM",
                    "ACIA", "ACHV", "ACHN", "ACHC", "ACH", "ACGLO", "ACGL", "ACET",
                    "ACER", "ACCO", "ACC", "ACBI", "ACB"]

#ROC Errors from AAAU, AAME, ACSI, ACT, ACGPL, ACES, AAMC
#above stock codes were removed because they did not have enough data points in the database

#initialize empty arrays of predictions for arima model and fourier model
arima_predictions = []
fourier_predictions = []
actualPrices = []

#get the predictions for all stocks in the list of stocks selected for testing
for name in listOfStockNames:
    print(name)
    data = getOutputtedPrediction(name)
    arima_predictions.append(data[2])
    fourier_predictions.append(data[3])
    actualPrices.append(data[4])

#print the predictions to verify everything worked
print("predictions are.........")
print(arima_predictions)
print(fourier_predictions)
print("actual prices are.....")
print(actualPrices)

#initialize empty arrays of percent errors for arima and fourier models
arima_perrs = []
fourier_perrs = []

#initialize empty arrays of absolute errors
arima_abs_errors = []
fourier_abs_errors = []

#fill arima perrs and absolute errors
for i in range(len(actualPrices)):
    arima_perrs.append(getPerr(arima_predictions[i],actualPrices[i][-1]))
    arima_abs_errors.append(getDifference(arima_predictions[i],actualPrices[i][-1]))

#get fourier errors for a particular stock
for i in range(len(actualPrices)):
    fourier_perrs_for_this_stock = []
    fourier_abs_errors_for_this_stock = []
    for j in range(len(actualPrices[0])):
        fourier_perrs_for_this_stock.append(getPerr(fourier_predictions[i][j],actualPrices[i][j]))
        fourier_abs_errors_for_this_stock.append(getDifference(fourier_predictions[i][j],actualPrices[i][j]))
    fourier_perrs.append(fourier_perrs_for_this_stock)
    fourier_abs_errors.append(fourier_abs_errors_for_this_stock)

#initialize average fourier errors for all stocks
#there are multiple predictions so we can see the trend of the error as the extrapolations get farther into the future
fourier_avg_perrs = []
fourier_avg_abserrs = []

#fill arrays of average fourier errors
for i in range(len(fourier_perrs[0])):
    total_fourier_perr = 0
    total_fourier_abserr = 0
    for j in range(len(fourier_perrs)):
        total_fourier_perr += fourier_perrs[j][i]
        total_fourier_abserr += fourier_abs_errors[j][i]
    total_fourier_perr /= len(fourier_perrs)
    total_fourier_abserr /= len(fourier_abs_errors)
    fourier_avg_perrs.append(total_fourier_perr)
    fourier_avg_abserrs.append(total_fourier_abserr)

#print all the results
#percentage error tells us how close the prediction is relative to the price of the stock
print("percent errors are...")
print(arima_perrs)
print("average ARIMA percent error")
print(getAvgError(arima_perrs))
print("average Fourier first extrapolation percent error")
print(fourier_avg_perrs)

print()

#The absolute error tells us how far off from the actual stock price the prediction was, in dollars
print("average ARIMA absolute error is")
print(getAvgError(arima_abs_errors))
#fourier errors are printed such that the prediction farthest in the future is last in the array
print("average Fourier extrapolation absolute error is")
print(fourier_avg_abserrs)
