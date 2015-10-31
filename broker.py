import market as m
import math


class Broker:

    def __init__(self, market):
        self.fees = 9
        self.market = market

    def sell(self, stocks, account, portfolio, date):
        for stock in stocks:
            p = self.market.get_price(stock, date)
            q = portfolio.quantity(stock)
            value = p * q
            value -= self.fees
            portfolio.sell(stock)
            account.credit(value, date)
            print("selling", q, "shares of", list(stocks)[0], "at", value, "on", date)

    def buy_even_weight(self, stocks, account, portfolio, date):
        balance = account.balance
        desired_number = len(stocks)
        if desired_number > 0:
            budget = balance/desired_number
            budget -= (self.fees * desired_number)
            for stock in stocks:
                price = self.market.get_price(stock, date)
                quantity = math.floor(budget/price)
                purchase_price = (price * quantity) - self.fees
                account.debit(purchase_price, date)
                portfolio.buy(stock, quantity)
                print("buying", quantity, "shares of", list(stocks)[0], "at", purchase_price, "on", date)