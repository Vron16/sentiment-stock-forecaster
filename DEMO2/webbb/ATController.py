"""
ATController.py - models a user account
"""
from alpha_vantage.timeseries import TimeSeries
import mysql.connector as ms
import NeuralNetwork as nn
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time
import techcontroller
from SentimentController import SentimentController
import SentimentCalculator
import SentimentPredictor

class AutomatedTrader:
    def __init__(self):
        """Creates a new Automated Trader
        :param balance: the user's current account balance
        :param stock_portfolio: list of stock tickers
        """
        #assert isinstance(balance, float)
        self.balance = 1000.0
        self.stock_portfolio = {}
        # key: stock_symbol
        # value: stock_amount

    # request an initial deposit from the user
    def check_initial_deposit(self):
        requires_initial_deposit = True
        while requires_initial_deposit:
            print("\nWelcome! Please enter an initial deposit for your AutoTrader account balance:")
            user_input = input()
            try:
                initial_deposit = float(user_input)
                if initial_deposit < 0:
                    print("Invalid input. Starting balance cannot be negative - please try again!")
                else:
                    print("You have successfully deposited $" + str(initial_deposit) + " to your AutoTrader account.\n")
                    self.balance += initial_deposit
                    requires_initial_deposit = False
            except ValueError:
                print("Invalid input. You must input some starting balance - please try again!")

    # request an initial stock selection from the user
    def initial_stock_selection(self):
        print("Let's begin by building a portfolio of companies that you're interested in investing in.")
        while True:
            print("Enter the stock ticker of a company that you are interested in (or 'done' when finished):\n")
            stock_symbol = input()
            if stock_symbol.lower() == "done":
                return
            self.search_stock_symbol(stock_symbol)

    # search database to check if the stock_symbol exists
    def search_stock_symbol(self, stock_symbol):
        # connect to database
        cnx = ms.connect(user='root', password='mypassword', host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com',
                         database='mydb')
        my_cursor = cnx.cursor()

        query = "SELECT stock_code FROM stock"
        my_cursor.execute(query)
        result = my_cursor.fetchall()

        search_success = False
        for x in result:
            # if x == ('A',):
            if x[0] == stock_symbol:

                search_success = True
                # add stock symbol to portfolio with zero initial stocks

                if stock_symbol in self.stock_portfolio.keys():

                    print("Adding share to portfolio")
                    continue

                else:
                    print("This stock exists. Adding stock to stock portfolio.")
                    self.stock_portfolio[stock_symbol] = 0
                print(self.stock_portfolio)

        if not search_success:
            print("This stock doesn't exist. Please try again.")
        return search_success

    # returns the price of the requested stock
    def get_stock_price(self, stock_symbol):
        for stock_name in self.stock_portfolio.keys():
            if stock_name == stock_symbol:
                # connect to database
                cnx = ms.connect(user='root', password='mypassword',
                                 host='mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com',
                                 database='mydb')
                my_cursor = cnx.cursor()

                ts = TimeSeries(key='9YJC3VY3APE01WTD')
                data, meta_data = ts.get_intraday(symbol='NYSE:' + stock_symbol, interval='5min', outputsize='compact')

                dictvalue = list(data.values())[0]
                open_value = dictvalue.get('1. open')
                current_price = float(open_value)
                cnx.close()
                return current_price

    # display current price information for stocks in portfolio
    def print_portfolio_prices(self):
        for stock_name in self.stock_portfolio.keys():
            print("\n" + stock_name + " ")
            print("The current price of this stock is $" + str(self.get_stock_price(stock_name)))

    # display list of stocks and corresponding shares
    def print_portfolio(self):
        print("Number of companies in your portfolio: " + str(len(self.stock_portfolio)))
        for k, v in self.stock_portfolio.items():
            print("You currently own " + str(v) + " " + str(k) + " share(s).")

    def print_portfolio_2(self):
        print("Number of companies in your portfolio: " + str(len(self.stock_portfolio)))
        arr = []
        for k, v in self.stock_portfolio.items():
            print("You currently own " + str(v) + " " + str(k) + " share(s).")
            arr.append(str(k))
            arr.append(str(v))
        return arr

    def purchase_shares_manually(self):
        print("\nTo begin purchasing shares, first select a stock from your portfolio.")
        # self.print_balance()
        # self.print_portfolio()
        while True:
            print("Enter a stock symbol (or 'done' when finished):")
            stock_symbol = input()
            if stock_symbol.lower() == "done":
                return
            elif stock_symbol not in self.stock_portfolio.keys():
                print("You do not currently have '" + stock_symbol + "' in your portfolio.\n"
                      "Would you like to add " + stock_symbol + " to your portfolio? (yes/no)")
                user_response = input()
                if user_response.lower() == "yes":
                    self.search_stock_symbol(stock_symbol)
                else:
                    continue
            else:
                print("How many shares would you like to purchase for " + stock_symbol + "?")
                user_input = input()
                try:
                    shares_purchased = int(user_input)
                    if shares_purchased < 0:
                        print(
                            "Invalid input. You cannot purchase negative shares - please try again!")
                    else:
                        if round((self.get_stock_price(stock_symbol)) * shares_purchased, 2) > self.balance:
                            print("You don't have enough money to purchase that many shares.")
                        else:
                            print("You have successfully purchased " + str(
                                shares_purchased) + " " + stock_symbol + " shares.")
                            self.stock_portfolio[stock_symbol] = self.stock_portfolio[stock_symbol] + shares_purchased
                            self.balance -= (self.get_stock_price(stock_symbol)) * shares_purchased
                except ValueError:
                    print("Invalid input. You must input a number - please try again!")

    def sell_shares_manually(self):
        print("To begin selling, first select a stock from your portfolio:\n")

        while True:
            print("\nEnter a stock symbol (or 'done' when finished):")
            stock_symbol = input()
            if stock_symbol.lower() == "done":
                return
            elif stock_symbol not in self.stock_portfolio.keys():
                print("You do not currently have " + stock_symbol + " in your portfolio.\n")
                continue
            else:
                print("How many shares would you like to sell for " + stock_symbol + "?")
                user_input = input()
                try:
                    shares_sold = int(user_input)
                    if shares_sold < 0:
                        print(
                            "Invalid input. You cannot sell negative shares - please try again!")
                    else:
                        if shares_sold > self.stock_portfolio[stock_symbol]:
                            print("You do not own that many " + stock_symbol + " shares.")
                        else:
                            print("You have successfully sold " + str(shares_sold) + " " + stock_symbol + " shares.")
                            self.stock_portfolio[stock_symbol] = self.stock_portfolio[stock_symbol] - shares_sold
                            self.balance += (self.get_stock_price(stock_symbol)) * shares_sold
                except ValueError:
                    print("Invalid input. You must input a number - please try again!")

    def print_balance(self):
        print("You have $" + str(self.balance) + " in your account balance.")

    def deposit_money(self):
        print("Enter the amount of money to deposit:")
        user_input = input()
        try:
            deposit = round(float(user_input), 2)
            if deposit < 0:
                print("Invalid input. Deposit cannot be negative - please try again!")
            else:
                print("You have successfully deposited $" + str(deposit) + " to your AutoTrader account.\n")
                self.balance += deposit
        except ValueError:
            print("Invalid input. Deposit is not a number.")

    def withdraw_money(self):
        print("Enter the amount of money to withdraw:")
        user_input = input()
        try:
            withdrawal = round(float(user_input), 2)
            if withdrawal < 0:
                print("Invalid input. Withdrawal cannot be negative - please try again!")
            else:
                if withdrawal > self.balance:
                    print("You do not have that much money to withdraw.")
                else:
                    print("You have successfully withdrawn $" + str(withdrawal) + " from your AutoTrader account.\n")
                    self.balance -= withdrawal
        except ValueError:
            print("Invalid input. Withdrawal is not a number.")

    # ---------------------------- NEW METHODS YAY! -------------------------------------------------------------------

    def request_trading_duration(self):
        print("How long do you want the AutoTrader to run for? Enter in days, hours, and minutes.\n")
        days = int(input("Days: "))
        hours = int(input("Hours: "))
        minutes = int(input("Minutes: "))
        print("The AutoTrader will trade for {} days, {} hours, and {} minutes.".format(days,hours,minutes))
        return 60*minutes + 3600*hours + 86400*days

    def compare_price(self, currprice, predictedprice):
        price = list(currprice)[1]
        print(type(price))
        print(price)
        print(type(predictedprice))
        print(predictedprice)
        if price > predictedprice:
            return 2
        else:
            return 1  # buy

    def make_decision(self, sentiment, price, analyzed_price, stock_symbol):
        # sentiment: number from sentiment team, where >0 is good and <0 is bad
        # price: actual (current) price of the stock -> retrieved from database
        # analyzed_price: number from forecaster team -> an actual value (dollar amount)
        # stock_symbol: stock to be traded
        NN = nn.Neural_Network()
        forcastprice = NN.scaleinput((sentiment, analyzed_price))
        # make them similar orders of magnitude - its just how the NN wants the inputs
        predictedprice = NN.predict(forcastprice) # predictedprice will be the output/prediction of our NN
        buysell = self.compare_price(forcastprice, predictedprice)
        if buysell == 1:
            # we are buying
            if float(price) < self.balance:
                self.balance -= price
                self.balance = round(self.balance)
                print(self.stock_portfolio[stock_symbol])
                self.stock_portfolio[stock_symbol] = self.stock_portfolio[stock_symbol] + 1
                print(self.stock_portfolio[stock_symbol])
                self.print_portfolio()
        else:
            if self.stock_portfolio[stock_symbol] > 0:
                self.balance += price
                self.stock_portfolio[stock_symbol] = self.stock_portfolio[stock_symbol] - 1
                self.print_portfolio()

    # eat up those JSON objects
    def auto_trade(self, stock_symbol, trading_duration):

        time_left = int(trading_duration)
        sentController = SentimentController()
        print("starting autotrade")

        while time_left > 0:
            # Code executed here
            self.search_stock_symbol(stock_symbol)
            print("going around the loop")
            self.make_decision(sentController.handleAutoTradeRequest(stock_symbol), self.get_stock_price(stock_symbol),techcontroller.getPrediction2(stock_symbol)[6],stock_symbol)
            print("made decision")
            #time.sleep(60)
            time_left = time_left - 60
            # every 300 seconds (5 minutes), make a decision

        return self.print_portfolio_2()

    # ---------------------------- END OF SECTION ---------------------------------------------------------------------