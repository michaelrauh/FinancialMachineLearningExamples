import datetime
import math

import stock
import data_service as d
from parser import DataOrder
from event import Event


class Market:

    stocks = dict()
    symbols = []
    start = None
    price_map = dict()
    events = {}
    data_service = None
    sorted_stocks = dict()
    date = datetime.date.today()
    time = None
    traders = list()
    highest_performing_traders = dict()

    @classmethod
    def initialize(cls, start_date, end_date):
        cls.data_service = d.DataService(start_date, end_date)
        cls.data_service.load()
        cls.date = cls.data_service.round_from_weekend(start_date)
        cls.start = cls.date
        cls.price_map = cls.data_service.data_map
        cls.symbols = cls.data_service.symbols()
        cls.load_all_stocks()
        cls.time = DataOrder.open
        print("Done initializing")

    @classmethod
    def load_all_stocks(cls):
        for symbol in cls.symbols:
            cls.stocks[symbol] = stock.Stock(symbol, cls.start)

    @classmethod
    def tick(cls):
        cls.sorted_stocks = dict()
        cls.highest_performing_traders = dict()
        for symbol in cls.price_map.keys():
            current_price = cls.price_map[symbol][cls.date][cls.time.value]
            cls.stocks[symbol].push_price(cls.date, cls.time.value, current_price)
            if cls.date.weekday() == 0 and cls.time == DataOrder.open:
                sunday = cls.date - datetime.timedelta(1)
                saturday = cls.date - datetime.timedelta(2)
                sunday_price = cls.price_map[symbol][sunday]
                saturday_price = cls.price_map[symbol][saturday]
                cls.stocks[symbol].push_day(sunday, sunday_price)
                cls.stocks[symbol].push_day(saturday, saturday_price)
        Event.trigger_all()
        if cls.time == DataOrder.close:
            cls.time = DataOrder.open
            cls.date = cls.data_service.next_valid_date(cls.date)
        else:
            cls.time = DataOrder(int(cls.time.value) + 1)

    @classmethod
    def sort_by_performance(cls, start_date):
        if start_date not in cls.sorted_stocks:
            for stock in cls.stocks.values():
                stock.set_start(start_date)
            top_stocks = sorted(list(cls.stocks.values()), key=lambda i: i.performance_key(), reverse=True)
            top_stocks = [s for s in top_stocks if s.performance_key() > 0]
            cls.sorted_stocks[start_date] = top_stocks
        return cls.sorted_stocks[start_date]

    @classmethod
    def shift_regress(cls, horizon):
        best_correlation = -1
        best_stock = None
        yesterday = cls.date - datetime.timedelta(1)
        horizon_ago = yesterday - datetime.timedelta(horizon)
        top_stocks = cls.sort_by_performance(horizon_ago)
        for stock in top_stocks:
            month_before_horizon = horizon_ago - datetime.timedelta(30)
            slice_a = stock.get_history_slice(month_before_horizon, horizon_ago)
            for other_stock in list(cls.stocks.values()):
                month_ago = yesterday - datetime.timedelta(30)
                slice_b = other_stock.get_history_slice(month_ago, yesterday)
                if slice_a is not None and slice_b is not None:
                    correlation = cls.pearson(slice_a, slice_b)
                    if correlation > best_correlation:
                        best_correlation = correlation
                        best_stock = other_stock
        return best_correlation, best_stock

    @staticmethod
    def average(x):
        assert len(x) > 0
        return float(sum(x)) / len(x)

    @staticmethod
    def pearson(x, y):
        assert len(x) == len(y)
        n = len(x)
        assert n > 0
        avg_x = Market.average(x)
        avg_y = Market.average(y)
        diffprod = 0
        xdiff2 = 0
        ydiff2 = 0
        for idx in range(n):
            xdiff = x[idx] - avg_x
            ydiff = y[idx] - avg_y
            diffprod += xdiff * ydiff
            xdiff2 += xdiff * xdiff
            ydiff2 += ydiff * ydiff

        return diffprod / math.sqrt(xdiff2 * ydiff2)

    @classmethod
    def sort_traders_by_performance(cls, horizon):
        if horizon not in cls.highest_performing_traders:
            for trader in cls.traders:
                trader.set_performance_horizon(horizon)
            valid_traders = [trader for trader in cls.traders if trader.performance() is not None]
            top_traders = sorted(list(valid_traders), key=lambda i: i.performance(), reverse=True)
            top_traders = [t for t in top_traders if t.performance() >= 0]
            cls.highest_performing_traders[horizon] = top_traders
        return cls.highest_performing_traders[horizon]