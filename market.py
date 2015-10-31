import stock
import static_data as data


class Market:
    def __init__(self, start_date, end_date):
        self.symbols = data.symbols()
        self.stocks = {}
        self.load_all(start_date, end_date)
        self.all_dates = self.get_all_dates()

    @staticmethod
    def create_stock(symbol, start_date, end_date):
        cap = data.cap(symbol)
        ipo = data.ipo(symbol)
        sector = data.sector(symbol)
        industry = data.industry(symbol)
        return stock.Stock(symbol, cap, ipo, sector, industry, start_date, end_date)

    def load_all(self, start_date, end_date):
        for symbol in self.symbols:
            self.stocks[symbol] = self.create_stock(symbol, start_date, end_date)

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
        for stock in self.stocks.values():
            if stock.data is not None:
                all_dates = all_dates.union(stock.all_dates())
        return all_dates

    def get_price(self, symbol, date):
        return self.stocks[symbol].get_open_price(date)