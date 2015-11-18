import stock
import static_data as data
import blacklist as bl


class Market:

    @staticmethod
    def create_stock(symbol, start_date, end_date, validate):
        cap = data.cap(symbol)
        ipo = data.ipo(symbol)
        sector = data.sector(symbol)
        industry = data.industry(symbol)
        return stock.Stock(symbol, cap, ipo, sector, industry, start_date, end_date, validate)

    def __init__(self, start_date, end_date):
        self.symbols = data.symbols()
        self.stocks = {}
        self.load_all(start_date, end_date)
        self.all_dates = self.get_all_dates()

    def load_all(self, start_date, end_date):
        print("loading...")
        path = bl.path(start_date, end_date)
        if not bl.blacklist_exists(path):
            print("no blacklist. Loading will be slow")
            blacklist = []
            for symbol in self.symbols:
                self.stocks[symbol] = self.create_stock(symbol, start_date, end_date, True)
                if self.stocks[symbol].data is None:
                    blacklist.append(symbol)
            bl.write_to_blacklist(path, blacklist)
        else:
            for symbol in self.symbols:
                if not bl.blacklisted(path, symbol):
                    self.stocks[symbol] = self.create_stock(symbol, start_date, end_date, False)

    def get_top_x(self, x, start_date, end_date):
        for stock_data in self.stocks.values():
            stock_data.start_date = start_date
            stock_data.end_date = end_date
        top_stocks = sorted(list(self.stocks.values()), key=lambda i: i.performance_key(), reverse=True)
        top_stocks = [s for s in top_stocks if s.performance_key() > 0]
        return top_stocks[:x]

    def open_on(self, date):
        return date in self.all_dates

    def get_all_dates(self):
        all_dates = set()
        for s in self.stocks.values():
            if s.data is not None:
                all_dates = all_dates.union(s.all_dates())
        return all_dates

    def get_price(self, symbol, date):
        return self.stocks[symbol].get_price(date)