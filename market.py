import stock
import data_service as d
from parser import DataOrder
import datetime
from event import Event


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
        print("Done initializing")

    def load_all_stocks(self):
        for symbol in self.symbols:
            self.stocks[symbol] = stock.Stock(symbol, self.start)

    def tick(self):
        for symbol in self.price_map.keys():
            current_price = self.price_map[symbol][self.date][self.time.value]
            self.stocks[symbol].push_price(self.date, self.time.value, current_price)
            if self.date.weekday() == 0 and self.time == DataOrder.open:
                sunday = self.date - datetime.timedelta(1)
                saturday = self.date - datetime.timedelta(2)
                sunday_price = self.price_map[symbol][sunday]
                saturday_price = self.price_map[symbol][saturday]
                self.stocks[symbol].push_day(sunday, sunday_price)
                self.stocks[symbol].push_day(saturday, saturday_price)
        Event.trigger_all()
        if self.time == DataOrder.close:
            self.time = DataOrder.open
            self.date = self.data_service.next_valid_date(self.date)
        else:
            self.time = DataOrder(int(self.time.value) + 1)
        print("current time is", str(self.date), str(self.time.name))