import scraper
import parser


def get_todays_stocks(symbols):
    stocks = list()
    stock_data = parser.parse_static_info()
    symbols = scraper.get_todays_symbols()

    for symbol in symbols:
        ipo, sector = stock_data[symbol]
        stock = Stock(ipo, sector)
        data = scraper.get_data(symbol, ipo)
        stock.find_highs(data)
        stocks.append(stock)

    return stocks


class Stock:
    def __init__(self, ipo, sector):
        self.ipo = ipo
        self.sector = sector
        pass

    def find_highs(self, data):
        pass