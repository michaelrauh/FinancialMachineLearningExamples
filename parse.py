from helper import parse
import cPickle as pickle

f = open('data.csv','r').read()
f = f.split('FILE')
f = f[0:50]
stocks = []
for stock in f:
    stocks.append(parse(stock))

pickle.dump(stocks,open("pickles/stocks.p","wb"))
