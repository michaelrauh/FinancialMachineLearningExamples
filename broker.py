import market as m
import math


class Broker:

    def __init__(self):
        self.fees = 9

    def sell(self, stocks, account, portfolio, date):
        market = m.Market()
        for stock in stocks:
            p = market.get_price(stock, date)
            q = portfolio.quantity(stock.symbol)
            value = p * q
            value -= self.fees
            portfolio.sell(stock.symbol)
            account.credit(value, date)

    def buy_even_weight(self, stocks, account, portfolio, date):
        market = m.Market()
        balance = account.available_balance
        desired_number = len(stocks)
        budget = balance/desired_number
        budget -= self.fees
        for stock in stocks:
            price = market.get_price(stock, date)
            quantity = math.floor(budget/price)
            purchase_price = (price * quantity) - self.fees
            account.debit(purchase_price, date)
            portfolio.buy(stock.symbol, quantity)