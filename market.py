import stock
import static_data as data
import datetime


class Market:
    def __init__(self):
        self.symbols = data.symbols()
        self.stocks = {}
        self.load_all(start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today())
        self.all_dates = self.get_all_dates()

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

    def get_top_x(self, x, start_date, end_date):
        for stock in self.stocks.values():
            stock.start_date = start_date
            stock.end_date = end_date
        top_stocks = sorted(list(self.stocks.values()), key=lambda stock : stock.performance_key(), reverse=True)
        return top_stocks[:x]

    def open_on(self, date):
        return date in self.all_dates

    def get_all_dates(self):
        all_dates = set()
        for stock in self.stocks:
            all_dates = all_dates.union(stock.all_dates())
        return all_dates