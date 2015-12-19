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

    def trade(self):
        today = self.market.date
        if self.market.time == DataOrder.close:
            time_ago = today - datetime.timedelta(self.horizon)
            top_stocks = self.sort_by_performance(time_ago)[0:self.portfolio_size]
            desired_stocks = set([i for i in top_stocks if not i.blacklisted(today)])
            current_stocks = set(self.portfolio.stocks())
            missing_stocks = desired_stocks.difference(current_stocks)
            extra_stocks = current_stocks.difference(desired_stocks)
            for stock in extra_stocks:
                self.broker.sell(stock, self.account, self.portfolio)
            budget = self.split_money(self.account.balance, len(missing_stocks)) - (self.broker.fees * 2)
            for stock in missing_stocks:
                self.broker.buy(self.strategy, budget, stock, self.account, self.portfolio, self.loss, self.blacklist_duration)

    def sort_by_performance(self, start_date):
        for stock in self.market.stocks.values():
            stock.set_start(start_date)
        top_stocks = sorted(list(self.market.stocks.values()), key=lambda i: i.performance_key(), reverse=True)
        top_stocks = [s for s in top_stocks if s.performance_key() > 0]
        return top_stocks