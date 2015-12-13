import stock
import data_service as d
from parser import DataOrder


class Market:
    def __init__(self, start_date, end_date):
        self.data_service = d.DataService(start_date, end_date)
        self.data_service.load()
        self.price_map = self.data_service.data_map
        self.symbols = self.data_service.symbols()
        self.stocks = {}
        self.load_all_stocks()
        self.date = self.data_service.round_from_weekend(start_date)
        self.time = DataOrder.open
        self.events = {}

    def load_all_stocks(self):
        for symbol in self.symbols:
            self.stocks[symbol] = stock.Stock(symbol)

    def tick(self):
        for stock in self.price_map.values():
            current_price = stock[self.date][self.time.value]
            stock.push_price(self.date, self.time, current_price)
        self.try_all_events()
        if self.time == DataOrder.close:
            self.time = DataOrder.open
            self.date = self.data_service.next_valid_date(self.date)
        else:
            self.time += 1

    def register_event(self, stock, trigger):
        self.events[stock] = trigger

    def delete_event(self, stock):
        del (self.events[stock])

    def try_all_events(self):
        iter_events = dict(self.events)
        for event in iter_events.values():
            event.fire_if_applicable()