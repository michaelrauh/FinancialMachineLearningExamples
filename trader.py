import datetime
import market as m
import portfolio as p
import broker as b
import account as a
from parser import DataOrder
import math


class Trader:

    @staticmethod
    def split_money(money, ways):
        return math.floor(money/ways)

    def __init__(self, starting_money, start_date, end_date):
        self.starting_money = starting_money
        self.market = m.Market(start_date, end_date)
        self.account = a.Account(starting_money)
        self.portfolio = p.Portfolio()
        self.broker = b.Broker(self.market)

    def top_x(self, x, horizon, loss, blacklist_duration):
        today = self.market.date
        if self.market.time == DataOrder.close:
            time_ago = today - datetime.timedelta(horizon)
            desired_stocks = set(self.sort_by_performance(time_ago)[0:x])
            current_stocks = set(self.portfolio.stocks())
            missing_stocks = desired_stocks.difference(current_stocks)
            extra_stocks = current_stocks.difference(desired_stocks)
            for stock in extra_stocks:
                self.broker.sell(stock, self.account, self.portfolio, today)
            budget = self.split_money(self.account.balance, len(missing_stocks)) - (self.broker.fees * 2)
            for stock in missing_stocks:
                self.broker.buy_stop_loss(budget, self.portfolio, self.account, stock, loss, blacklist_duration)

    def sort_by_performance(self, start_date):
        for stock in self.market.stocks.values():
            stock.set_start(start_date)
        top_stocks = sorted(list(self.market.stocks.values()), key=lambda i: i.performance_key(), reverse=True)
        top_stocks = [s for s in top_stocks if s.performance_key() > 0]
        return top_stocks