import techController
import mm
import csv


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
            #weight ar     #weight_four
    return [prediction[0], prediction[1], arima_prediction, fourier_predictions,lastCloses]

def getPerr(predicted, actual):
    return abs((predicted - actual)/actual*100)


def getAvgError(perrs):
    total = 0
    for num in perrs:
        total += num
    total /= len(perrs)
    return total


def getDifference(predicted, actual):
    return abs(predicted-actual)


listOfStockNames =  ["AAPL","AA", "A", "AAL", "AABA", "AAC",  "AAOI", "AAN", "AAON", "AAP",
                    "AAT", "AAU", "AAWW", "AAXJ", "AAXN", "AB", "ABB", "ABBV", "ABC", "ABCB",
                    "ABDC", "ABEO", "ABG", "ABIL", "ABM", "ABMD", "ABR", "AADR", #took out ABIO
                    "ACST", "ACRX", "ACRS", "ACRE", "ACP", "NFLX", #took out ACSG
                    "ACOR", "ACNB", "ACN", "ACMR", "ACM", "ACLS","ACIW", "ACIU", "ACIM",
                    "ACIA", "ACHV", "ACHN", "ACHC", "ACH", "ACGLO", "ACGL", "ACET",
                    "ACER", "ACCO", "ACC", "ACBI", "ACB"]
#ROC Errors from AAAU, AAME, ACSI, ACT, ACGPL, ACES, AAMC

#listOfStockNames = []

#with open('stocksindb.csv') as csv_file:
#    csv_reader = csv.reader(csv_file, delimiter = ',')
#    for line in csv_reader:
#        listOfStockNames.append(line[0])

#print(listOfStockNames)

#listOfStockNames.pop(0)

#listOfDuds = []

weight_ar_predictions = []
weight_four_predictions = []
arima_predictions = []
fourier_predictions = []
actualPrices = []

for name in listOfStockNames:
    print(name)
    data = getOutputtedPrediction(name)
    weight_ar_predictions.append(data[0])
    weight_four_predictions.append(data[1])
    arima_predictions.append(data[2])
    fourier_predictions.append(data[3])
    actualPrices.append(data[4])

print("predictions are.........")
print(weight_ar_predictions)
print(weight_four_predictions)
print(arima_predictions)
print(fourier_predictions)
print("actual prices are.....")
print(actualPrices)

arima_perrs = []
fourier_perrs = []

arima_abs_errors = []
fourier_abs_errors = []

for i in range(len(actualPrices)):
    arima_perrs.append(getPerr(arima_predictions[i],actualPrices[i][-1]))
    #fourier_perrs.append(getPerr(fourier_predictions[i],actualPrices[i]))
    arima_abs_errors.append(getDifference(arima_predictions[i],actualPrices[i][-1]))
    #fourier_abs_errors.append(getDifference(fourier_predictions[i],actualPrices[i]))

for i in range(len(actualPrices)):
    fourier_perrs_for_this_stock = []
    fourier_abs_errors_for_this_stock = []
    for j in range(len(actualPrices[0])):
        fourier_perrs_for_this_stock.append(getPerr(fourier_predictions[i][j],actualPrices[i][j]))
        fourier_abs_errors_for_this_stock.append(getDifference(fourier_predictions[i][j],actualPrices[i][j]))
    fourier_perrs.append(fourier_perrs_for_this_stock)
    fourier_abs_errors.append(fourier_abs_errors_for_this_stock)

fourier_avg_perrs = []
fourier_avg_abserrs = []

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

print("percent errors are...")
#print(w_ar_percentErrors)
#print(w_four_percentErrors)
print(arima_perrs)
#print(fourier_perrs)
#print ("average weighted Arima percent error")
#print(getAvgError(w_ar_percentErrors))
#print("average weighted Fourier percent error")
#print(getAvgError(w_four_percentErrors))
print("average ARIMA percent error")
print(getAvgError(arima_perrs))
print("average Fourier first extrapolation percent error")
print(fourier_avg_perrs)
#print(getAvgError(fourier_perrs))

print()
print("average ARIMA absolute error is")
print(getAvgError(arima_abs_errors))
print("average Fourier extrapolation absolute error is")
print(fourier_avg_abserrs)
#print(getAvgError(fourier_abs_errors))

#print("number of empty stocks:")
#print(len(listOfDuds))