import datetime

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
    date = None
    time = None

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