import stock
import static_data as data
import data_service as d
from parser import DataOrder
import tick as t
import datetime


class Market:
    @staticmethod
    def create_stock(symbol, start_date, end_date):
        cap = data.cap(symbol)
        ipo = data.ipo(symbol)
        sector = data.sector(symbol)
        industry = data.industry(symbol)
        return stock.Stock(symbol, cap, ipo, sector, industry, start_date, end_date)

    def __init__(self, start_date, end_date):
        data_service = d.DataService(start_date, end_date)
        self.price_map = data_service.data_map
        self.symbols = data_service.symbols()
        self.stocks = {}
        self.load_all(start_date, end_date)
        self.date = start_date
        self.time = DataOrder.open
        self.events = {}

    def try_all_events(self):
        iter_events = dict(self.events)
        for event in iter_events.values():
            event.fire_if_applicable()

    def tick(self):
        for stock in self.price_map.values():
            current_price = stock[self.date][self.time]
            tick = t.Tick(self.date, self.time, current_price)
            stock.push_price(tick)
        self.try_all_events()
        if self.time == DataOrder.close:
            self.time = DataOrder.open
            self.date = self.date + datetime.timedelta(1)
        else:
            self.time += 1

    def load_all(self, start_date, end_date):
        for symbol in self.symbols:
            self.stocks[symbol] = self.create_stock(symbol, start_date, end_date)