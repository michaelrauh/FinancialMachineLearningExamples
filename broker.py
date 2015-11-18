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
            account.credit(value)
            print("selling", q, "shares of", stock, "at", value, "on", date, "that's", p, "per share")

    def buy_even_weight(self, stocks, account, portfolio, date):
        balance = account.balance
        desired_number = len(stocks)
        if desired_number > 0:
            budget = balance/desired_number
            budget -= (self.fees * desired_number * 2)
            for stock in stocks:
                p = self.market.get_price(stock, date)
                q = math.floor(budget/p)
                if q > 0:
                    purchase_price = (p * q) - self.fees
                    account.debit(purchase_price)
                    portfolio.buy(stock, q)
                    print("buying", q, "shares of", stock, "at", purchase_price, "on", date, "that's", p,
                          "per share")