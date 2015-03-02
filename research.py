import urllib.request

f = urllib.request.urlopen("http://www.barchart.com/stocks/high.php?_dtp1=0").read().decode("utf-8")
symbols = f[f.find("symbols") + len("symbols\" value=\""):f.find("/>", f.find("symbols"))-2].split(',')

def scrape(symbol):
        """Get Data from Google Finance"""
        try:
            PRESENT = '2014'
            url = 'http://www.google.com/finance/historical?q=' + symbol + \
                  '&histperiod=daily&startdate=Jan+1%2C+'+ '2013' + \
                  '&enddate=Dec+31%2C+' + PRESENT + '&output=csv'
            f = urllib.request.urlopen(url).read().decode("utf-8")
            points = f.replace('\n',',').split(',')
        except:
            points = []
        return points

def get_all_dates(stocks):
    max_len = 0
    for stock in stocks:
        if len(stock) > max_len:
            max_len = len(stock)
            all_dates = list(reversed(stock[0:-1:6]))
    return all_dates

stocks = []
for symbol in symbols:
    print (symbol, symbols.index(symbol), len(symbols))
    stocks.append(scrape(symbol))
all_dates = get_all_dates(stocks)

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

def elapsed_time(beginning, end, dates=all_dates):
    return dates.index(end) - dates.index(beginning)

def get_high_number(highs, threshold, dates = all_dates):
    #get rid of the try catch
    count = 0
    try:
        current_high = highs.pop()
        last_high = highs.pop()

        while (elapsed_time(last_high, current_high) <= threshold) and len(highs) > 0:
            current_high = last_high
            last_high = highs.pop()
            count += 1
    except:
        pass
    return count

def get_all_high_numbers(threshold):
    numbers = []
    for stock in stocks:
        highs = find_highs(stock)
        numbers.append(get_high_number(highs, threshold))
    return sum(numbers)/len(numbers)
