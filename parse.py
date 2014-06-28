from helper import Parse
import cPickle as pickle
import urllib2

f = urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?d=6&e=1&f=2010&g=d&a=7&b=19&c=2000&ignore=.csv&s=bbby').read()
#f = open('table.csv','r').read()
#f = f.split('FILE')
#stocks = []
#for stock in f:
#    stocks.append(Parse(stock))

stocks = Parse(f)
pickle.dump(stocks,open("pickles/stocks.p","wb"))
