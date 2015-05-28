from stock import *
import util


def get_stocks():
    stocks = []
    for filename in ('data/nyse.csv', 'data/nasdaq.csv'):
        f = open(filename).read()
        f = f.split('\n')
        f.pop(0)
        for row in f:
            x = row.split('"')
            stock = Stock()
            stock.symbol = x[1].replace('^', '-')
            cap = x[7]
            ipo = x[9]
            stock.sector = x[11]
            industry = x[13]
            stock.data = util.scrape(stock.symbol, ipo)
            if len(stock.data) > 0:
                stocks.append(stock)
            print(len(stocks), stock.symbol, len(stock.data))
    return stocks


def get_date():
    return 'mmddyyyy'