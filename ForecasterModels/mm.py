from statsmodels.tsa.arima_model import ARIMA

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