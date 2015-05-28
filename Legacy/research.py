#import helper
import urllib.request
import pylab as plt
import datetime
import subprocess
import pickle
import os

#Only pull stock data if it is not pickled away in buckets
#Factor functions out to helpers
# Make the main function runnable on any day in the past

subprocess.Popen(["caffeinate", "-t", "300"])
f = urllib.request.urlopen("http://www.barchart.com/stocks/high.php?_dtp1=0").read().decode("utf-8")
symbols = f[f.find("symbols") + len("symbols\" value=\""):f.find("/>", f.find("symbols"))-2].split(',') 

#symbols = symbols[:5]

def scrape(symbol):
        try:
                """Get Data from Google Finance"""
                PRESENT = '2015'
                url = 'http://www.google.com/finance/historical?q=' + symbol + \
                      '&histperiod=daily&startdate=Jan+1%2C+'+ '2014' + \
                      '&enddate=Dec+31%2C+' + PRESENT + '&output=csv'
                f = urllib.request.urlopen(url).read().decode("utf-8")
                points = f.replace('\n',',').split(',')
        except:
                points = []
        return points

stocks = []
for symbol in symbols:
    print (symbol, symbols.index(symbol), len(symbols))
    stocks.append(scrape(symbol))
max_len = 0
for stock in stocks:
        if len(stock) > max_len:
                max_len = len(stock)
                all_dates = list(reversed(stock[0:-1:6]))

def find_highs(stock):
    """find all 52 week highs for a stock if there is enough data"""
    high_dates = []
    try:
        FTW = 253 # fifty two weeks, with holidays
        dates = list(reversed(stock[0:-1:6]))
        dates.pop()
        highs = list(reversed(stock[2:-1:6]))
        highs.pop()
        for i in range(FTW,len(highs)):
            if max(highs[i-FTW:i-1]) < highs[i]:
                high_dates.append(dates[i])
    except:
        pass

    return high_dates

def elapsed_time(beginning, end, dates=all_dates): #apparently this doesn't necessarily contain all dates. It may fail.
    return dates.index(end) - dates.index(beginning)

def get_high_number(highs, threshold, dates = all_dates):
        """gets current high number. -1 shows error"""
        count = 0

        if len(highs) == 0:
                return -1
        elif len(highs) == 1:
                return 0
        current_high = highs.pop()
        last_high = highs.pop()

        while (elapsed_time(last_high, current_high) <= threshold) and len(highs) > 0:
                current_high = last_high
                last_high = highs.pop()
                count += 1
        return count

def get_all_high_numbers(threshold): 
    numbers = []
    for stock in stocks:
        highs = find_highs(stock)
        numbers.append(get_high_number(highs, threshold))
    return sum(numbers)/len(numbers)

def find_counts(threshold):
        x = {}
        for stock in stocks:
                highs = find_highs(stock)
                symbol = symbols[stocks.index(stock)]
                high_number = get_high_number(highs, threshold)
                try:
                        x[high_number].append(symbol)
                except:
                        x[high_number] = [symbol]
        return x

#################MAKE GRAPHS###############

date = str(datetime.date.today())

try:
        os.mkdir(date)
except:
        pass

plt.figure(1)
buckets = find_counts (15)
try:
        del(buckets[-1])
except:
        pass
y = [len(buckets[high_number]) for high_number in buckets]
x = range(len(y))

deltas = []
for i in range(len(y) -1):
        deltas.append((y[i + 1] - y[i])/y[i])
        
plt.subplot(221)
plt.title("number for t = 15")
plt.bar(x, y)
plt.subplot(222)
plt.title("% change in number for t = 15")
plt.bar(range(len(deltas)), deltas)

buckets_one = find_counts (1)
try:
        del(buckets_one[-1])
except:
        pass
y = [len(buckets_one[high_number]) for high_number in buckets_one]
x = range(len(y))

deltas = []
for i in range(len(y) -1):
        deltas.append((y[i + 1] - y[i])/y[i])

plt.subplot(223)
plt.title("number for t = 1")
plt.bar(x, y)
plt.subplot(224)
plt.title("% change in number for t = 1")
plt.bar(range(len(deltas)), deltas)

f = open(date + '/counts.txt', 'w')
f.write("15:\n")
f.write(str(buckets))
f.write("1:\n")
f.write(str(buckets_one))
plt.savefig(date + '/figures.pdf', bbox_inches='tight')
#plt.show()
f.close()

#plt.figure(2)
#plt.subplot(221)

#Separate by cap, sector
