import RateOfChange


def calculateROC_test():
    closing = [0, 1, 2, 3]
    now = 1
    nAgo = 2
    assert RateOfChange.calculateROC(closing, now, nAgo) == -50


def test():
     calculateROC_test()
     print("If no errors, tests passed!")

test()