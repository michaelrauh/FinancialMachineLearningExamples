from stock import *
import util
import urllib2


def get_todays_symbols():
    f = urllib2.urlopen("http://www.barchart.com/stocks/high.php?_dtp1=0").read()
    symbols = f[f.find("symbols") + len("symbols\" value=\""):f.find("/>", f.find("symbols"))-2].split(',')
    return symbols

x = get_todays_symbols()

print (x)

def get_symbol_map():
    stocks = []
    for filename in ('data/nyse.csv', 'data/nasdaq.csv'):
        f = open(filename).read()
        f = f.split('\n')
        f.pop(0)
        for row in f:
            x = row.split('"')
            stock = Stock()
            stock.symbol = x[1].replace('^', '-')
            ipo = x[9]
            stock.sector = x[11]
            print(len(stocks), stock.symbol, len(stock.data))
    return stocks


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