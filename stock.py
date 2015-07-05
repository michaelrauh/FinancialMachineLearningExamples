import scraper
import parser


def populate_stocks(symbols):
    stocks = list()
    stock_data = parser.parse_static_info()
    for symbol in symbols:
        print len(symbols), symbols.index(symbol), symbol
        try:
            ipo, sector = stock_data[symbol]
            stock = Stock(symbol, ipo, sector)
            stocks.append(stock)
        except:
            print "skipped ", symbol
    return stocks


def get_todays_stocks():
    symbols = scraper.get_todays_symbols()
    stocks = populate_stocks(symbols)
    return stocks


def get_all_stocks():
    stock_data = parser.parse_static_info()
    symbols = stock_data.keys()
    stocks = populate_stocks(symbols)
    return stocks


def elapsed_time(beginning, end, dates):
    return dates.index(end) - dates.index(beginning)


class Stock:
    def __init__(self, symbol, ipo, sector):
        self.ipo = ipo
        self.sector = sector
        self.symbol = symbol
        self.data = scraper.get_data(symbol, ipo)
        self.all_dates = parser.get_dates(self.data)
        self.day_maximums = parser.get_maximums(self.data)
        self.highs = self.find_highs()
        self.high_number = self.current_high_number()
        self.all_high_numbers = self.get_all_high_numbers()
        self.all_closes = parser.get_closes(self.data)
        self.today = self.all_dates[-1]

    def __str__(self):
        return str((self.symbol, self.ipo, self.sector))

    def find_highs(self):
        high_dates = list()
        try:
            FTW = 253 # fifty two weeks, with holidays
            dates = self.all_dates
            dates.pop()
            highs = self.day_maximums
            highs.pop()
            for i in range(FTW, len(highs)):
                if max(highs[i-FTW:i-1]) < highs[i]:
                    high_dates.append(dates[i])
        except:
            pass

        return high_dates

    def current_high_number(self):
        count = 0
        threshold = 15
        highs = list(self.highs)
        all_dates = list(self.all_dates)

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

# TODO: Test this method to be sure the list isn't coming out backward and that it isn't being consumed backward

    def get_all_high_numbers(self):
        all_highs = list()
        while len(self.highs) > 0:
            all_highs.append(self.current_high_number())
            self.highs.pop()
        return all_highs