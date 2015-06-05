import scraper
import parser


def get_todays_stocks():
    stocks = list()
    stock_data = parser.parse_static_info()
    symbols = scraper.get_todays_symbols()[:5] # TODO: Remove this cap of five symbols

    for symbol in symbols:
        print len(symbols), symbols.index(symbol)
        try:
            ipo, sector = stock_data[symbol]
            stock = Stock(symbol, ipo, sector)
            data = scraper.get_data(symbol, ipo)
            stock.find_highs(data)
            stocks.append(stock)
        except:
            print "skipped ", symbol

    return stocks


class Stock:
    def __init__(self, symbol, ipo, sector):
        self.ipo = ipo
        self.sector = sector
        self.symbol = symbol

    def __str__(self):
        return str((self.symbol, self.ipo, self.sector))

    def find_highs(self, data):
        pass