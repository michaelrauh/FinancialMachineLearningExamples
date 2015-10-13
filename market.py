import stock
import static_data as data
import datetime


class Market:
    def __init__(self):
        self.symbols = data.symbols()
        self.stocks = {}

    def load(self, symbol, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        cap = data.cap(symbol)
        ipo = data.ipo(symbol)
        sector = data.sector(symbol)
        industry = data.industry(symbol)
        self.stocks[(symbol, start_date, end_date)] = stock.Stock(symbol, cap, ipo, sector, industry, start_date, end_date)

    def load_all(self, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        for symbol in self.symbols:
            self.fetch(symbol, start_date, end_date)

    def fetch(self, symbol, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        try:
            return self.stocks[(symbol, start_date, end_date)]
        except KeyError:
            self.load(symbol, start_date, end_date)
            return self.stocks[(symbol, start_date, end_date)]

    def get_top_x(self, x, start_date, end_date, era_start=datetime.date(1950, 1, 1), era_end=datetime.date.today()):
        self.load_all(start_date=era_start, end_date=era_end)
        for stock in self.stocks.values():
            stock.start_date = start_date
            stock.end_date = end_date
        top_stocks = sorted(list(self.stocks.values()), key=lambda stock : stock.performance_key(), reverse=True)
        return top_stocks[:x]

market = Market()
market.get_top_x(3, datetime.date(2015, 10, 8), datetime.date.today())