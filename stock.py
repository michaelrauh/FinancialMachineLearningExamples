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
            stocks.append(stock)
        except:
            print "skipped ", symbol

    return stocks


def find_highs(data):
    high_dates = []
    try:
        FTW = 253 # fifty two weeks, with holidays
        dates = list(reversed(data[0:-1:6]))
        dates.pop()
        highs = list(reversed(data[2:-1:6]))
        highs.pop()
        for i in range(FTW, len(highs)):
            if max(highs[i-FTW:i-1]) < highs[i]:
                high_dates.append(dates[i])
    except:
        pass

    return high_dates


class Stock:
    def __init__(self, symbol, ipo, sector):
        self.ipo = ipo
        self.sector = sector
        self.symbol = symbol
        self.data = scraper.get_data(symbol, ipo)
        self.highs = find_highs(self.data)

    def __str__(self):
        return str((self.symbol, self.ipo, self.sector))