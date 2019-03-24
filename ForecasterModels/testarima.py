import matplotlib.pyplot as plt
import random
import sys
#from pandas.tools.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA

def getARIMA(stock_data):
    
    fc = -1
    if(len(stock_data) < 1):
        return fc
    
    p = 5
    while(1):
        try:
            if(p == 0):
                return -2
            print("p: ", p)
            model = ARIMA(stock_data, order=(p,1,0))
            model_fit = model.fit(disp=0)
    
            fc = model_fit.forecast()[0][0]
            return fc
        except:
            #print("Unexpected error:", sys.exc_info()[0])
            p-=1
        
    return fc

def testARIMA():
    
    probs = []
    total = 50

    for i in range(10):
        total += random.gauss(0,2)
        probs.append(total)

    #autocorrelation_plot(probs)
    #plt.show()
    plt.plot(probs)
    plt.show()

    fc = getARIMA(probs)

    print("Predicted Price: ", fc)


#testARIMA()