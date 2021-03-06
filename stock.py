from parser import DataOrder


class Stock:

    def __init__(self, symbol, begin_sim):
        self.symbol = symbol
        self.start_date = None
        self.price_history = dict()
        self.current_price = None
        self.beginning_of_time = begin_sim

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

    def set_start(self, start_date):
        self.start_date = start_date

    def performance_key(self):
        return self.current_performance(self.start_date)

    def __repr__(self):
        return self.symbol