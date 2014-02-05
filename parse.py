from helper import parse
import cPickle as pickle

f = open('data.csv','r').read()
f = f.split('FILE')

stocks = []
for stock in f:
    stocks.append(parse(stock))

pickle.dump(stocks,open("pickles/stocks.p","wb"))
