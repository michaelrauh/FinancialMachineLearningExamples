from parser import DataOrder
import datetime


class Stock:

    def __init__(self, symbol):
        self.symbol = symbol
        self.start_date = None
        self.blacklist_date = datetime.date(1900, 1, 1)
        self.price_history = dict()
        self.current_price = None

    def push_price(self, date, time, price):
        self.price_history[date] = {time: price}
        self.current_price = price

    def fetch_price(self, date, time):
        try:
            return self.price_history[date][time]
        except KeyError:
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

    def blacklist(self, date, duration):
        self.blacklist_date = date + datetime.timedelta(duration)

    def blacklisted(self, date):
        return date < self.blacklist_date