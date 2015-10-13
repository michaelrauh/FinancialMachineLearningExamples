import stock
import static_data as data
import datetime


class Market:
    def __init__(self):
        self.symbols = data.symbols()
        self.stocks = {}

    def create_stock(self, symbol, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        cap = data.cap(symbol)
        ipo = data.ipo(symbol)
        sector = data.sector(symbol)
        industry = data.industry(symbol)
        return stock.Stock(symbol, cap, ipo, sector, industry, start_date, end_date)

    def load_all(self, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        for symbol in self.symbols:
            new_stock = self.create_stock(symbol, start_date, end_date)
            if new_stock.data is not None:
                self.stocks[(symbol, start_date, end_date)] = new_stock

    def get_top_x(self, x, start_date, end_date, era_start=datetime.date(1950, 1, 1), era_end=datetime.date.today()):
        assert(self.stocks != {})
        assert(era_start <= start_date <= end_date <= era_end)
        for stock in self.stocks.values():
            stock.start_date = start_date
            stock.end_date = end_date
        top_stocks = sorted(list(self.stocks.values()), key=lambda stock : stock.performance_key(), reverse=True)
        return top_stocks[:x]

market = Market()
market.load_all()
tops = market.get_top_x(3, datetime.date(2015, 10, 8), datetime.date.today())
for top in tops:
    print(top.symbol)