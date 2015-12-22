import datetime
import portfolio as p
import broker as b
import account as a
from parser import DataOrder
import math


class Trader:

    @staticmethod
    def split_money(money, ways):
        try:
            return math.floor(money/ways)
        except ZeroDivisionError:
            return 0

    def __init__(self, starting_money, market, strategy, portfolio_size, horizon, loss=None, blacklist_duration=None):
        self.starting_money = starting_money
        self.market = market
        self.account = a.Account(starting_money)
        self.portfolio = p.Portfolio()
        self.broker = b.Broker(self.market)
        self.portfolio_size = portfolio_size
        self.horizon = horizon
        self.loss = loss
        self.blacklist_duration = blacklist_duration
        self.strategy = strategy
        self.name = hash(self)
        self.banned_stocks = dict()
        for stock in market.stocks.values():
            self.banned_stocks[stock] = datetime.date(1900, 1, 1)

    def trade(self):
        today = self.market.date
        if self.market.time == DataOrder.close:
            time_ago = today - datetime.timedelta(self.horizon)
            top_stocks = self.market.sort_by_performance(time_ago)[0:self.portfolio_size]
            desired_stocks = set([i for i in top_stocks if not self.blacklisted(i)])
            current_stocks = set(self.portfolio.stocks())
            missing_stocks = desired_stocks.difference(current_stocks)
            extra_stocks = current_stocks.difference(desired_stocks)
            for stock in extra_stocks:
                self.broker.sell(self, stock, self.account, self.portfolio)
            budget = self.split_money(self.account.balance, len(missing_stocks)) - (self.broker.fees * 2)
            for stock in missing_stocks:
                self.broker.buy(self.strategy, budget, stock, self.account, self.portfolio, self, self.loss, self.blacklist_duration)

    def blacklist(self, stock, blacklist_duration):
        self.banned_stocks[stock] = self.market.date + datetime.timedelta(blacklist_duration)

    def blacklisted(self, stock):
        return self.market.date < self.banned_stocks[stock]