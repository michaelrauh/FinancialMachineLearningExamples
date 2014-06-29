"""Calculate average return by number of previous lows"""
import cPickle as pickle
import urllib2

opn = 0
high = 1
low = 2
close = 3
volume = 4

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

def num_fifty_two(date,yearLows,dates):
    """Find number of 52 week lows in 10 day period before date"""
    count = 0
    last_ten = dates[dates.index(date)-10:dates.index(date)]
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
    
    #create map from date to point data.
    point_map = {}
    for i in range(len(dates)):
        #print opens[i],highs[i],lows[i],closes[i],volumes[i]
        try:
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

def find_coordinates(stock):
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
    print len(yearLows), 'lows found: '
    for date in yearLows:
        print date
        maximum = find_max(date,dates,point_map)
        minimum = find_min(maximum,dates,point_map)
        coordinates[date] = []
        # Number of 52 week lows in 10 day period #
        coordinates[date].append(num_fifty_two(date, yearLows, dates))

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

def future_value(date, stock):
    """Return true if the stock is a good buy"""
    month = 20
    opn = 0
    interest = 1.08
    dates = stock[0]
    stock = stock[1]
    try:
            later = dates [dates.index(date) + month]
    except IndexError:
            later = dates[-1]
    value = ((stock[later][opn]) - stock[date][opn])/stock[later][opn]
    return value

symbol = raw_input('enter symbol: ')
start = str(int(raw_input('enter training start year: ')) - 1) # go back one extra year for low detection. This extra year isn't in results.
end = raw_input('enter training end year: ')

url = 'http://www.google.com/finance/historical?q=' + symbol + '&histperiod=daily&startdate=Jan+1%2C+'+ start + '&enddate=Dec+31%2C+' + end + '&output=csv'

f = urllib2.urlopen(url).read()
stock = Parse(f)

all_points = find_coordinates(stock)
low_count = [[] for i in range(20)]
interest = .08

for date in all_points:
    low_count[all_points[date][0]].append(future_value(date,stock))

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
        
