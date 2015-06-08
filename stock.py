import scraper
import parser


def get_todays_stocks():
    stocks = list()
    stock_data = parser.parse_static_info()
    symbols = scraper.get_todays_symbols() # TODO: Remove this cap of five symbols

    for symbol in symbols:
        print len(symbols), symbols.index(symbol), symbol
        try:
            ipo, sector = stock_data[symbol]
            stock = Stock(symbol, ipo, sector)
            stocks.append(stock)
        except:
            print "skipped ", symbol

    return stocks


def find_highs(data):
    high_dates = list()
    try:
        FTW = 253 # fifty two weeks, with holidays
        dates = list(reversed(data[0:-1:6])) # TODO: Move to parser
        dates.pop()
        highs = list(reversed(data[2:-1:6]))
        highs.pop()
        for i in range(FTW, len(highs)):
            if max(highs[i-FTW:i-1]) < highs[i]:
                high_dates.append(dates[i])
    except:
        pass

    return high_dates


def elapsed_time(beginning, end, dates):
    return dates.index(end) - dates.index(beginning)


class Stock:
    def __init__(self, symbol, ipo, sector):
        self.ipo = ipo
        self.sector = sector
        self.symbol = symbol
        self.data = scraper.get_data(symbol, ipo)
        self.highs = find_highs(self.data)
        self.all_dates = list(reversed(self.data[0:-1:6]))
        self.high_number = self.current_high_number()

    def __str__(self):
        return str((self.symbol, self.ipo, self.sector))

    def current_high_number(self):
        count = 0
        threshold = 15
        highs = self.highs
        all_dates = self.all_dates

        if len(highs) == 0:
                return -1
        elif len(highs) == 1:
                return 0
        current_high = highs.pop()
        last_high = highs.pop()

        while (elapsed_time(last_high, current_high, all_dates) <= threshold) and len(highs) > 0:
                current_high = last_high
                last_high = highs.pop()
                count += 1
        return count