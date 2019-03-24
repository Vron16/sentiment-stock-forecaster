import StochasticOscillator


def findHighest():
    numDays = 1
    high = [1, 2, 3, 4, 3, 2, 1]
    price = StochasticOscillator.findHighest(high, 0, len(high)-1)
    print(price)
    assert price == 4


def findLowest():
    numDays = 1
    low = [1, 2, 3, 4, 3, 2, 1]
    price = StochasticOscillator.findLowest(low, 0, len(low)-1)
    print(price)
    assert price == 1


def test():
    findHighest()
    findLowest()
    print("If no errors, tests passed!")

test()