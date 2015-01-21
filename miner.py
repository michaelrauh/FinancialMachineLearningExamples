import urllib.request
from random import choice

START_TRAIN = "00"
STOP_TRAIN = "11"
START_RUN = "11"
STOP_RUN = "15"
MONTH = 20
FIFTY_TWO_WEEKS = 52 * 5


def parse(symbol):
        """Create record of dates and stock data from google api given symbol"""
        url = 'http://www.google.com/finance/historical?q=' + symbol + \
              '&histperiod=daily&startdate=Jan+1%2C+20'+ START_TRAIN + \
              '&enddate=Dec+31%2C+20' + STOP_RUN + '&output=csv'
        f = urllib.request.urlopen(url).read().decode("utf-8")
        points = f.replace('\n',',').split(',')
        
        # create map from date to point data.
        point_map = {}
        dates = []
        for i in range(6, len(points)-6, 6):
            try:
                point_map[points[i]] = (float(points[i+1]),float(points[i+2]),\
                                        float(points[i+3]),float(points[i+4]),float(points[i+5]))
                dates.append(points[i])
            except:
                pass
        dates.reverse()
        stock = (dates,point_map)
        return stock


def get_all_stocks():
        """Load stock list from barchart, then parse each stock"""
        f = urllib.request.urlopen("http://www.barchart.com/stocks/high.php?_dtp1=0").read().decode("utf-8")
        symbols = f[f.find("symbols") + len("symbols\" value=\""):f.find("/>", f.find("symbols"))-2].split(',')
        current_date = f[f.find("dtaDate") + len("dtaDate\">"):f.find("</", f.find("dtaDate"))]
        stocks = []
        loaded_symbols = []

        print(len(symbols))
        i = 0
        for symbol in symbols:
            i += 1
            print(i)
            try:
                stock = parse (symbol)
                stocks.append(stock)
                loaded_symbols.append(symbol)
            except:
                pass              
        return stocks, loaded_symbols


def load_stocks():
        stocks, symbols = get_all_stocks()
        train_stocks = []
        run_stocks = []

        for stock in stocks:
                (train_dates, run_dates) = ([], [])
                (train_stock, run_stock) = ({}, {})
                dates = stock[0]
                stock = stock[1]

                run_times = range(int(START_RUN),int(STOP_RUN))
                train_times = range(int(START_TRAIN),int(STOP_TRAIN))
                
                for date in dates:
                        year = int(date[-2:])
                        if year in run_times:
                                run_stock [date] = stock[date]
                                run_dates.append(date)
                        elif year in train_times:
                                train_stock[date] = stock[date]
                                train_dates.append(date)
                train_stocks.append((train_dates,train_stock))
                run_stocks.append((run_dates,run_stock))
        return train_stocks,run_stocks, symbols


def find_highs(dates, stock):
        """find fifty two week highs for a stock. There may be none in training set"""
        high_dates = []
        HIGH = 1
        highs = [stock[date][HIGH] for date in dates]
        for i in range(FIFTY_TWO_WEEKS, len(dates)):
                if max(highs[i - FIFTY_TWO_WEEKS:i-1]) < highs[i]:
                        high_dates.append(dates[i])
        return high_dates


def get_high_number(dates,highs,high):
        """given a high, gives how many come before it in a month"""
        return len(set.intersection(set(dates[dates.index(high) - MONTH:dates.index(high) + 1]), set(highs))) -1


def get_current_highs(run_stocks):
        """ returns the high number for each stock. If the stock is new, it returns None"""
        current_highs = []
        for i in range(len(run_stocks)):
                try:
                        dates = run_stocks[i][0]
                        highs = run_highs[i]
                        high = run_highs[i][-1]
                        current_highs.append(get_high_number(dates,highs,high))
                except:
                        current_highs.append(None)
        return current_highs

# Load lists of date, date->stock tuples
train_stocks, run_stocks, symbols = load_stocks()

# Get dates for 52 week highs for train and run
train_highs = [find_highs(stock[0],stock[1]) for stock in train_stocks]
run_highs = [find_highs(stock[0],stock[1]) for stock in run_stocks]

current_highs = get_current_highs(run_stocks)

# Get quartile returns for the current high for each stock
def get_same_highs(current):
        """takes the stock pos and returns all dates that high number occurred on for the stock in that pos"""
        try:
                current_dates = []
                dates = train_stocks[current][0]
                highs = train_highs[current]
                for high in highs:
                        if current_highs[current] == get_high_number(dates,highs,high):
                                current_dates.append(high)
                return current_dates
        except:
                return None

def get_same_run_highs(current):
        """takes the stock pos and returns all dates that high number occurred on for the stock in that pos"""
        try:
                current_dates = []
                dates = run_stocks[current][0]
                highs = run_highs[current]
                for high in highs:
                        if current_highs[current] == get_high_number(dates,highs,high):
                                current_dates.append(high)
                return current_dates
        except:
                return None
        
all_same_highs = [get_same_highs(i) for i in range(len(train_stocks))]

def get_returns(stock, same_highs, look_forward):
        CLOSE = 3
        dates, stock = stock
        returns = []
        for i in range(len(same_highs)):
                current_value = stock[same_highs[i]][CLOSE]
                try:
                        later_date = dates[dates.index(same_highs[i]) + look_forward]
                except:
                        later_date = dates[-1]
                later_value = stock[later_date][CLOSE]
                returns.append(((later_value - current_value)/current_value) * 100)
        return returns
        
all_returns = [get_returns(train_stocks[i], all_same_highs[i], 20) for i in range(len(symbols))]

all_same_run_highs = [get_same_run_highs(i) for i in range(len(run_stocks))]

all_run_returns = [get_returns(run_stocks[i],all_same_run_highs[i],20) for i in range(len(symbols))]

occurrences = [len(returns) for returns in all_returns]

for returns in all_returns:
        if len(returns) == 0:
                returns.append(float("-inf"))

leasts = [min(returns) for returns in all_returns]

def twenty_five(l):
        l.sort()
        return l[int(len(l)/4)]

q1s = [twenty_five(returns) for returns in all_returns]


def median(l):
        l.sort()
        return l[int(len(l)/2)]

medians = [median(returns) for returns in all_returns]

def seventy_five(l):
        l.sort()
        return l[int(len(l) * 3/4)]

q3s = [seventy_five(returns) for returns in all_returns]

mosts = [max(returns) for returns in all_returns]

q1map = {}
for q1 in q1s:
        pos = q1s.index(q1)
        q1map[q1] = symbols[pos], current_highs[pos], leasts[pos],q1s[pos], medians[pos],q3s[pos],mosts[pos], occurrences[pos]

keys = list(q1map.keys())
keys.sort()
keys.reverse()
for key in keys:
        if q1map[key][-1] > 9:
                #print (q1map[key])
                pass


too_low, q0_to_q1, q1_to_q2, q2_to_q3, q3_to_q4, too_high = 0,0,0,0,0,0
for n in range(len(symbols)):
        try:
                 i = choice(range(len(symbols)))
                 for num in all_run_returns[n]:
                        if num < leasts[i]:
                                too_low +=1
                        elif num < q1s[i]:
                                q0_to_q1 += 1
                        elif num < medians[i]:
                                q1_to_q2 += 1
                        elif num < q3s[i]:
                                q2_to_q3 += 1
                        elif num < mosts[i]:
                                q3_to_q4 += 1
                        elif num > mosts[i]:
                                if mosts[i] != float("-inf"):
                                        too_high += 1
        except:
                pass
total = sum([too_low, q0_to_q1, q1_to_q2, q2_to_q3, q3_to_q4, too_high])
print(too_low/total + q0_to_q1/total, q1_to_q2/total, q2_to_q3/total, q3_to_q4/total + too_high/total)


for z in range(len(current_highs)):
	if current_highs[z] == None:
		current_highs[z] = -1

#for each current high number
for high_number in range(max(current_highs)):
	count = 0
	total = 0
	for item in range(len(all_run_returns)):
		if current_highs[item] == high_number:
			count += len(all_run_returns[item])
			total += sum(all_run_returns[item])
	print(high_number, count, count/total)
