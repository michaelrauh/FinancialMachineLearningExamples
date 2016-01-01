import datetime
import math

import portfolio as p
import broker as b
import account as a
from market import Market


class Trader:

    @staticmethod
    def split_money(money, ways):
        try:
            return math.floor(money/ways)
        except ZeroDivisionError:
            return 0

    def __init__(self, starting_money, strategy, portfolio_size, horizon, price_change=None, blacklist_duration=None):
        self.starting_money = starting_money
        self.account = a.Account(starting_money)
        self.portfolio = p.Portfolio()
        self.broker = b.Broker()
        self.portfolio_size = portfolio_size
        self.horizon = horizon
        self.price_change = price_change
        self.blacklist_duration = blacklist_duration
        self.strategy = strategy
        self.name = hash(self)
        self.banned_stocks = dict()
        for stock in Market.stocks.values():
            self.banned_stocks[stock] = datetime.date(1900, 1, 1)
        self.all_net_worths = list()

    def trade(self):
        today = Market.date
        time_ago = today - datetime.timedelta(self.horizon)
        top_stocks = Market.sort_by_performance(time_ago)[0:self.portfolio_size]
        desired_stocks = set([i for i in top_stocks if not self.blacklisted(i)])
        self.optimize_even_weight(desired_stocks)

    def optimize_even_weight(self, desired_stocks):
        current_stocks = set(self.portfolio.stocks())
        missing_stocks = desired_stocks.difference(current_stocks)
        extra_stocks = current_stocks.difference(desired_stocks)
        for stock in extra_stocks:
            self.broker.sell(self, stock, self.account, self.portfolio)
        budget = self.split_money(self.account.balance, len(missing_stocks)) - (self.broker.fees * 2)
        for stock in missing_stocks:
            self.broker.buy(self.strategy, budget, stock, self.account, self.portfolio, self, self.price_change, self.blacklist_duration)
        self.all_net_worths.append(self.portfolio.value() + self.account.balance)

    def blacklist(self, stock, blacklist_duration):
        self.banned_stocks[stock] = Market.date + datetime.timedelta(blacklist_duration)

    def blacklisted(self, stock):
        return Market.date < self.banned_stocks[stock]

    def set_performance_horizon(self, horizon):
        self.performance_horizon = horizon

    def performance(self):
        try:
            start = self.all_net_worths[-self.performance_horizon]
            end = self.all_net_worths[-1]
            ans = (end - start)/start
        except IndexError:
            ans = None
        return ans

    def current_stocks(self):
        return self.portfolio.stocks()