from parser import DataOrder
import datetime
import market

class Stock:

    def __init__(self, symbol, begin_sim):
        self.symbol = symbol
        self.start_date = None
        self.price_history = dict()
        self.current_price = None
        self.beginning_of_time = begin_sim
        self.performance_history = []
        self.most_recent_high = begin_sim
        self.most_recent_high_number = 0

    def push_price(self, date, time, price):
        if date not in self.price_history:
            self.price_history[date] = dict()
        self.price_history[date][time] = price
        self.current_price = price

    def push_day(self, date, data):
        self.price_history[date] = data

    def fetch_price(self, date, time):
        if date > self.beginning_of_time:
            return self.price_history[date][time.value]
        else:
            return None

    def current_performance(self, start_date):
        start = self.fetch_price(start_date, DataOrder.low)
        end = self.current_price
        if start is None or end is None:
            return 0
        return (end-start)/start

    def custom_performance(self, price):
        start = self.current_price
        end = price
        if start is None or end is None:
            return 0
        return (end-start)/start

    def set_start(self, start_date):
        self.start_date = start_date

    def performance_key(self):
        return self.current_performance(self.start_date)

    def get_history_slice(self, start_date, end_date):
        if self.fetch_price(start_date, DataOrder.open) is None:
            return None
        slice = list()
        current_date = start_date
        while current_date < end_date - datetime.timedelta(1):
            for time in [DataOrder.open, DataOrder.low, DataOrder.high, DataOrder.close]:
                current_price = self.fetch_price(current_date, time)
                slice.append(current_price)
            current_date = current_date + datetime.timedelta(1)
        return slice

    def moving_average(self, start_date, end_date):
        slice = self.get_history_slice(start_date, end_date)
        if slice is not None:
            return sum(slice)/len(slice)
        else:
            return None

    def get_high_number(self, start_date, end_date):
        performance = self.current_performance(start_date)
        self.performance_history.append(performance)
        if performance >= max(self.performance_history[-15:]):
            future_price = market.Market.get_price(self.symbol, market.Market.date + datetime.timedelta(days=21))
            perf = self.custom_performance(future_price)
            if end_date <= (self.most_recent_high + datetime.timedelta(days=21)):
                self.most_recent_high_number += 1
            else:
                self.most_recent_high_number = 0
            self.most_recent_high = end_date
            if self.most_recent_high_number not in market.Market.interesting_stocks:
                market.Market.interesting_stocks[self.most_recent_high_number] = {}
            if market.Market.date not in market.Market.interesting_stocks[self.most_recent_high_number]:
                market.Market.interesting_stocks[self.most_recent_high_number][market.Market.date] = []
            market.Market.interesting_stocks[self.most_recent_high_number][market.Market.date].append(perf)

    def __repr__(self):
        return self.symbol