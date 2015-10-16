import stock
import static_data as data
import datetime


class Market:
    def __init__(self):
        self.symbols = data.symbols()
        self.stocks = {}

    @staticmethod
    def create_stock(symbol, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        cap = data.cap(symbol)
        ipo = data.ipo(symbol)
        sector = data.sector(symbol)
        industry = data.industry(symbol)
        return stock.Stock(symbol, cap, ipo, sector, industry, start_date, end_date)

    def load_all(self, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        start_dates = [start_date for i in range(len(self.symbols))]
        end_dates = [end_date for i in range(len(self.symbols))]
        desired_keys = set(zip(self.symbols, start_dates, end_dates))
        current_keys = set(self.stocks.keys())
        missing_keys = desired_keys.difference(current_keys)
        for key in missing_keys:
            self.stocks[key] = self.create_stock(*key)

    def get_top_x(self, x, start_date, end_date, era_start=datetime.date(1950, 1, 1), era_end=datetime.date.today()):
        self.load_all(start_date=era_start, end_date=era_end)
        for stock in self.stocks.values():
            stock.start_date = start_date
            stock.end_date = end_date
        top_stocks = sorted(list(self.stocks.values()), key=lambda stock : stock.performance_key(), reverse=True)
        return top_stocks[:x]