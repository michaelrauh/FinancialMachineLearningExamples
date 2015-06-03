from stock import *
import util
import urllib2


def get_todays_symbols():
    f = urllib2.urlopen("http://www.barchart.com/stocks/high.php?_dtp1=0").read()
    symbols = f[f.find("symbols") + len("symbols\" value=\""):f.find("/>", f.find("symbols"))-2].split(',')
    return symbols


def get_todays_stocks(symbols):
    stocks = []
    for filename in ('data/nyse.csv', 'data/nasdaq.csv'):
        f = open(filename).read()
        f = f.split('\n')
        f.pop(0)
        for row in f:
            x = row.split('"')
            symbol = x[1].replace('^', '-')
            if symbol in symbols:
                stock = Stock()
                stock.symbol = symbol
                ipo = x[9]
                stock.sector = x[11]
                stock.data = util.scrape(stock.symbol, ipo)
                stock.highs = util.find_highs(stock.data)
                if len(stock.data) > 0:
                    stocks.append(stock)
    return stocks