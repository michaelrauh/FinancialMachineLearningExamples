import urllib.request
import pickle
import subprocess

subprocess.Popen(["caffeinate", "-t", "21600"]) #Prevent sleep for 6 hours

class Stock:
    pass

def scrape(symbol, ipo):
        """Get Data from Google Finance"""
        if ipo == 'n/a':
            ipo = '1972' #oldest stock in the table
        
        try:
            PRESENT = '2014'
            url = 'http://www.google.com/finance/historical?q=' + symbol + \
                  '&histperiod=daily&startdate=Jan+1%2C+'+ ipo + \
                  '&enddate=Dec+31%2C+' + PRESENT + '&output=csv'
            f = urllib.request.urlopen(url).read().decode("utf-8")
            points = f.replace('\n',',').split(',')
        except:
            points = []
        return points

stocks = []
for filename in ('nyse.csv','nasdaq.csv'):
    f = open(filename).read()
    f = f.split('\n')
    f.pop(0)
    for row in f:
        x = row.split('"')
        stock = Stock()
        stock.symbol = x[1].replace('^','-') 
        stock.cap = x[7]
        stock.ipo = x[9]
        stock.sector = x[11]
        stock.industry = x[13]
        stock.data = scrape(stock.symbol,stock.ipo)
        if len(stock.data) > 0:
            stocks.append(stock)
            print(len(stocks), stock.symbol, len(stock.data))
out = open('raw_stocks.txt','wb')
pickle.dump(stocks,out)
out.close()
print("done")
