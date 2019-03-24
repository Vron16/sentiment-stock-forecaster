def getSwing(stock_Data, priceSamplesPerDay, priceSamplesToday):
    length = len(stock_Data)
    t = 100 #t has to be user defined
    C = stock_Data[length-1] #today's closing price
    Cy = stock_Data[length-1-priceSamplesToday] #yesterdays closing price
    O = stock_Data[length - priceSamplesToday] #today's opening price
    Oy = stock_Data[length - priceSamplesToday - priceSamplesPerDay] #yesterdays opening price

    yesterdaysPrices = [priceSamplesPerDay] #make a list of yesterdays prices
    i = 0 #counter
    Hy = 0 #yesterdays high price
    Ly = Cy #yesterdays low price
    while i < priceSamplesPerDay:
        yesterdaysPrices[i] = stock_Data[length - priceSamplesToday - priceSamplesPerDay + i]
        if yesterdaysPrices[i] > Hy:
            Hy = yesterdaysPrices[i]
        if yesterdaysPrices[i] < Ly:
            Ly = yesterdaysPrices[i]
        i += 1

    todaysPrices = [priceSamplesToday]
    i = 0
    H = 0
    L = C
    while i < priceSamplesToday:
        todaysPrices[i] = stock_Data[length - priceSamplesToday + i]
        if todaysPrices[i] > H:
            H = todaysPrices[i]
        if todaysPrices[i] < L:
            L = todaysPrices[i]
        i += 1

    K = max(H-Cy,Cy-L)
    TR = max(H-Cy, L-Cy, H-L)

    if TR == H - Cy:
        R = (H-C) - .5*(L-C) - .25*(Cy-Oy)
    elif TR == L - Cy:
        R = L - Cy - .5*(H - O) + .25*(Cy-Oy)
    else:
        R = H - L + .25*(Cy-Oy)

    swing = 50 * (Cy - C + .5*(Cy - Oy) + .25*(C - O)/R) * K / t

    return swing

#To get ASI you get the swing for every day in the dataset

def getASI(stock_Data, priceSamplesPerDay, priceSamplesToday):
    ASI = []
    length = len(stock_Data)
    chunkSize = 2*priceSamplesPerDay
    while chunkSize <= length - priceSamplesToday:
        ASI.append(getSwing(stock_Data[0:chunkSize],priceSamplesPerDay,priceSamplesPerDay))
        chunkSize += priceSamplesPerDay
    ASI.append(getSwing(stock_Data, priceSamplesPerDay, priceSamplesToday))

    return ASI
