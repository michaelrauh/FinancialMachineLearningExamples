import stock
import static_data as data
import datetime


class Market:
    def __init__(self):
        self.symbols = data.symbols
        self.stocks = {}

    def load(self, symbol, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        cap = data.cap(symbol)
        ipo = data.ipo(symbol)
        sector = data.sector(symbol)
        industry = data.industry(symbol)
        self.stocks[symbol] = stock.Stock(symbol, cap, ipo, sector, industry, start_date, end_date)

    def load_all(self, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        for symbol in self.symbols:
            self.load(symbol, start_date, end_date)

    def fetch(self, symbol, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        try:
            return self.stocks[symbol]
        except KeyError:
            self.load(symbol, start_date, end_date)
            return self.stocks[symbol]