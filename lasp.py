"""Calculate average return by number of previous lows"""
import cPickle as pickle
import urllib2
import sys

opn = 0
high = 1
low = 2
close = 3
volume = 4

def find_closest(l,x):
    diffs = []
    for item in l:
        diffs.append(abs(item-x))
    return l[diffs.index(min(diffs))]

def slope_max(dates,date, maximum,point_map):
    """Find slope from maximum to date"""
    rise = point_map[maximum][high] - point_map[date][high]
    run = dates.index(date) - dates.index(maximum)
    try:
            return rise/run
    except ZeroDivisionError:
            return 0

def slope_min(dates,date, minimum,point_map):
    """Find slope from minimum to date"""
    rise = point_map[minimum][low] - point_map[date][low]
    run = dates.index(date) - dates.index(minimum)
    try:
            return rise/run
    except ZeroDivisionError:
            return 0

def num_fifty_two(date,yearLows,dates,period):
    """Find number of 52 week lows in a period before date"""
    count = 0
    last_ten = dates[dates.index(date)-period:dates.index(date)]
    for day in last_ten:
        count += yearLows.count(day)
    return count

def find_max(date,dates,point_map):
    """Find local max"""
    date_index = dates.index(date)
    while(point_map[dates[date_index]][high] < point_map[dates[date_index-1]][high]):
        date_index -= 1
    return dates[date_index]

def find_min(maximum,dates,point_map):
    """find local min"""
    date_index = dates.index(maximum)
    while(point_map[dates[date_index]][low] > point_map[dates[date_index-1]][low]):
        date_index -= 1
    return dates[date_index]


def Parse (data):
    """Create map from CSV"""
    points = data.replace('\n',',').split(',') # split csv
    points.pop()
    points = points[6:]
    dates = points[::6]
    opens = points[1::6]
    highs=points[2::6]
    lows=points[3::6]
    closes=points[4::6]
    volumes=points[5::6]
    banned = []
    
    for thing in [dates,opens,highs,lows,closes,volumes]:
        for i in range(len(thing)):
            if thing[i] == '-':
                if dates[i] not in banned:
                    banned.append(dates[i])
    for bad in banned:
        dates.remove(bad)
    #create map from date to point data.
    point_map = {}
    for i in range(len(dates)):
        try:
            if dates[i] not in banned:
                point_map[dates[i]] = (float(opens[i]),float(highs[i]),float(lows[i]),float(closes[i]),float(volumes[i])) 
        except:
            point_map[dates[i]] = (float(opens[i-1]),float(highs[i-1]),float(lows[i-1]),float(closes[i-1]),float(volumes[i-1]))
    dates.reverse() #Dates earliest to latest
    stock = (dates,point_map)
    return stock


def avg(points):
        """Find average of a list of points"""
        try:
                return sum(points)/len(points)
        except ZeroDivisionError:
                return 0
        except TypeError:
                return points

def find_coordinates(stock,period,verbose = True):
    """Run technical analysis on a given stock"""
    # Make list of lows
    lows = []
    dates = stock[0]
    point_map = stock[1]
    for date in dates:
        lows.append(point_map[date][low])
    yearLows = []
    fiftytwoweeks= 5 * 52

    # Find each 52 week low and add to yearLows. Map is not in order so
    # iterate over dates
    for i in range(fiftytwoweeks, len(dates)):
        # For dates after first buffer year
        if min(lows[i - fiftytwoweeks:i - 1]) > lows[i]:
            # If lowest in last 52 weeks is greater than current
            yearLows.append(dates[i])
            # Then this is a 52 week low (save the date)
            

    coordinates = {}
    if verbose:
        print len(yearLows), 'lows found: '
    for date in yearLows:
        if verbose:
            print date
        maximum = find_max(date,dates,point_map)
        minimum = find_min(maximum,dates,point_map)
        coordinates[date] = []
        # Number of 52 week lows in last month period #
        coordinates[date].append(num_fifty_two(date, yearLows, dates,period))

        # Slope from local max #
        coordinates[date].append(slope_max(dates, date, maximum, point_map))

        # Slope from local min #
        coordinates[date].append(slope_min(dates, date, minimum, point_map))

        # Volatility #
        coordinates[date].append(point_map[date][high] - point_map[date][low])

        # Volume #
        coordinates[date].append(point_map[date][volume])

        # Bull power #
        coordinates[date].append(point_map[maximum][volume])

        # Bear power #
        coordinates[date].append(point_map[minimum][volume])

        # Volatility at maximum #
        coordinates[date].append(point_map[maximum][high] - point_map[maximum][low])

        # Volatility at minimum #
        coordinates[date].append(point_map[minimum][high] - point_map[minimum][low])
    return coordinates

def future_value(date, stock,time):
    """Return true if the stock is a good buy"""
    dates = stock[0]
    stock = stock[1]
    try:
            later = dates [dates.index(date) + time]
    except IndexError:
            print 'Warning: Looking past end of data. Using last date.'
            later = dates[-1]
    value = ((stock[later][close]) - stock[date][close])/stock[later][close]
    return value


symbol = raw_input('enter symbol: ')
start = str(int(raw_input('enter training start year: ')) - 1) # go back one extra year for low detection. This extra year isn't in results.
end = raw_input('enter training end year: ')
interest = float(raw_input('enter expected return(ex. .08): '))
period = int(raw_input('Enter how far back to look for lows in days: '))
time = int(raw_input('Enter time to hold stock in days: '))
simple = bool(raw_input('Enter nonempty string for simple mode'))

try:
    url = 'http://www.google.com/finance/historical?q=' + symbol + '&histperiod=daily&startdate=Jan+1%2C+'+ start + '&enddate=Dec+31%2C+' + end + '&output=csv'
    print symbol, str(int(start) + 1), end
    f = urllib2.urlopen(url).read()
except:
    print "input a valid symbol"
    sys.exit()
stock = Parse(f)

all_points = find_coordinates(stock,period,not simple)
low_count = [[] for i in range(period)]

for date in all_points:
    low_count[all_points[date][0]].append(future_value(date,stock,time))

total = 0
for count in low_count:
    total += len(count)

print '|count|','instances |','occurrence|','mean |','   0%   |','    25%   |','   50%   |','   75%   |','   100%   |','percent safe |', 'percent good|'
i =0
for count in low_count:
    try:
        likelihood = float(len(count))/total
        goods = 0
        makes = 0
        count.sort()
        average = avg(count)
        q0 = count[0]
        q1 = count[len(count)/4]
        q2 = count[len(count)/2]
        q3 = count [len(count)/4 * 3]
        q4 = count[-1]
        for item in count:
            if item > 0:
                makes += 1
        make = float(makes)/len(count)
        for item in count:
            if item > interest:
                goods += 1
        good = float(goods)/len(count)
        print str(round(i, 3)).rjust(0),str(round(len(count),3)).rjust(10),str(round(likelihood,3)).rjust(10),str(round(average, 3)).rjust(10),str(round(q0, 3)).rjust(10),str(round(q1, 3)).rjust(10),str(round(q2, 3)).rjust(10),str(round(q3,3)).rjust(10),str(round(q4,3)).rjust(10),str(round(make,3)).rjust(10),str(round(good,3)).rjust(10)
        i+=1
    except:
        pass

start = '2013'
end = '2014'
url = 'http://www.google.com/finance/historical?q=' + symbol + '&histperiod=daily&startdate=Jan+1%2C+'+ start + '&enddate=Dec+31%2C+' + end + '&output=csv'
f = urllib2.urlopen(url).read()
focus = Parse(f)
tech = find_coordinates(focus,period,False)
try:
    temp = tech.keys()
    for i in range(len(temp)):
        temp[i] = temp[i].split('-')
    months_numbers = ['00','01','02','03','04','05','06','07','08','09','10','11']
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    x = []
    for date in temp:
        if len(date[0]) == 1:
            date[0] = '0' + date[0]
        x.append(date[2] + months_numbers[months.index(date[1])] + date[0])
    x.sort()
    top = x[-1]
    yr = top[:2]
    mn = top[2:4]
    day = top[4:]
    if day[0] == '0':
        day = day[1]
    recent = day + '-' + months[int(mn)] + '-' + yr
    print 'Most recent low:',recent
    print '# lows, slope from local max, slope from local min, volatility, volume, bull power, bear power, volatility at max, volatility at min'
    print tech[recent]
except IndexError:
    print 'No recent lows found. Should have bought it a long time ago.'
    sys.exit()

if simple:
    sys.exit()
    
#set up data for finding closest
dates = all_points.keys()
stocks = all_points
query = tech[recent]
indicators = [{} for i in range(9)]
for date in dates:
    if date != recent:
        for i in range(9):
            indicators[i][stocks[date][i]] = date
    
l = [[] for i in range(9)]
for i in range(1,9):
    l[i] = indicators[i].keys()

lengths = []
for i in range(len(l)):
    lengths.append(len(l[i]))
lengths.pop(0)
print 'indicator','date','recent','closest','% difference','projected value'
for j in range(min(lengths)):
    print '\n', j
    for i in range(1,9):
        x = query[i]
        closest = find_closest(l[i],x)
        l[i].remove(closest)
        date = indicators[i][closest]
        try:
            error = str(round((abs(closest - x)/float(x)),3) * 100).rjust(15)
        except:
            error = float("inf")
        print i,date , round(x,3), str(round(closest,3)).rjust(15),error , str(round(future_value(date,stock,time),3)).rjust(20)




        