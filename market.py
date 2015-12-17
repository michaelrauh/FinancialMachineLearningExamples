import stock
import data_service as d
from parser import DataOrder
import datetime


class Market:
    def __init__(self, start_date, end_date):
        self.data_service = d.DataService(start_date, end_date)
        self.data_service.load()
        self.date = self.data_service.round_from_weekend(start_date)
        self.start = self.date
        self.price_map = self.data_service.data_map
        self.symbols = self.data_service.symbols()
        self.stocks = {}
        self.load_all_stocks()
        self.time = DataOrder.open
        self.events = {}

    def load_all_stocks(self):
        for symbol in self.symbols:
            self.stocks[symbol] = stock.Stock(symbol, self.start)

    def tick(self):
        for symbol in self.price_map.keys():
            current_price = self.price_map[symbol][self.date][self.time.value]
            self.stocks[symbol].push_price(self.date, self.time.value, current_price)
            if self.date.weekday() == 0 and self.time == DataOrder.open:
                # On Monday Morning, push the weekend. In data_service, the weekend is filled with the monday open price
                # This makes it so that in retrospect it is known that orders put in over the weekend will fill at
                # market open. Pushing on monday prevents knowledge of the future. If we ever iterate through the
                # weekend it will be necessary to stop interpolating forward for weekends.
                sunday = self.date - datetime.timedelta(1)
                saturday = self.date - datetime.timedelta(2)
                sunday_price = self.price_map[symbol][sunday]
                saturday_price = self.price_map[symbol][saturday]
                self.stocks[symbol].push_day(sunday, sunday_price)
                self.stocks[symbol].push_day(saturday, saturday_price)
        self.try_all_events()
        if self.time == DataOrder.close:
            self.time = DataOrder.open
            self.date = self.data_service.next_valid_date(self.date)
        else:
            self.time = DataOrder(int(self.time.value) + 1)

    def register_event(self, stock, trigger):
        self.events[stock] = trigger

    def delete_event(self, stock):
        del (self.events[stock])

    def try_all_events(self):
        iter_events = dict(self.events)
        for event in iter_events.values():
            event.fire_if_applicable()