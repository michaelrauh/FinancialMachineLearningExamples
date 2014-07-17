"""Calculate average return by number of previous lows"""
import cPickle as pickle
import urllib2
import sys

opn = 0
high = 1
low = 2
close = 3
volume = 4
continues = True

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
    #create map from date to point data.
    point_map = {}
    dates = []
    for i in range (6,len(points)-6,6):
        try:
            point_map[points[i]] = (float(points[i+1]),float(points[i+2]),float(points[i+3]),float(points[i+4]),float(points[i+5]))
            dates.append(points[i])
        except:
            print points[i],'ignored' #This may result in out of bounds as there'll be fewer dates to look back to when finding lows. It may also be a low in terms of slightly more than 52 weeks. May miss lows. Very unlikely.
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

def future_value(date, stock,time,very_simple):
    """Return true if the stock is a good buy"""
    dates = stock[0]
    stock = stock[1]
    try:
            later = dates [dates.index(date) + time]
    except IndexError:
        if not very_simple:
            print 'Warning: Looking past end of data. Using last date.'
        later = dates[-1]
    value = ((stock[later][close]) - stock[date][close])/stock[later][close]
    return value

mistake = True
while mistake:
    try:
        start = str(int(raw_input('enter training start year: ')) - 1) # go back one extra year for low detection. This extra year isn't in results.
        end = raw_input('enter training end year: ')
        interest = float(raw_input('enter expected return(ex. .08): '))
        period = int(raw_input('Enter how far back to look for lows in days: '))
        time = int(raw_input('Enter time to hold stock in days: '))
        simple = bool(raw_input('Enter nonempty string for simple mode: '))
        very_simple = bool(raw_input('Enter nonempty string for screener mode: '))
        mistake = False
    except:
        print 'try again.\n'
    

symbol = 'dummy'
while symbol != '':
    symbol = raw_input('enter symbol: ')

    try:
        url = 'http://www.google.com/finance/historical?q=' + symbol + '&histperiod=daily&startdate=Jan+1%2C+'+ start + '&enddate=Dec+31%2C+' + end + '&output=csv'
        print symbol, str(int(start) + 1), end
        f = urllib2.urlopen(url).read()
    except:
        print "input a valid symbol"
        continues = False
    if continues:
        stock = Parse(f)

        all_points = find_coordinates(stock,period,not simple and not very_simple)
        low_count = [[] for i in range(period)]

        for date in all_points:
            low_count[all_points[date][0]].append(future_value(date,stock,time,very_simple))

        total = 0
        for count in low_count:
            total += len(count)

        low_count = [count for count in low_count if len(count) != 0]
        lenses = [len(count) for count in low_count]
        def sum_prior(l,index):
            return sum(l[0:index+1])
        lenses2 = []

        for i in range(len(lenses)):
            lenses2.append(sum(lenses))
            lenses.pop(0)

        if not very_simple:
            print '|count|','instances |','occurrence|','%bottom |','mean |','   0%   |','    25%   |','   50%   |','   75%   |','   100%   |','percent safe |', 'percent good|'
        i =0
        for count in low_count:
            likelihood = lenses2[i]#float(len(count))/total
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
            one = str(round(i, 3)).rjust(0)
            two = str(round(len(count),3)).rjust(10)
            three = str(round(likelihood,3)).rjust(10)
            four = str(round((len(count)/float(likelihood)),3)).rjust(10)
            five = str(round(average, 3)).rjust(10)
            six = str(round(q0, 3)).rjust(10)
            seven = str(round(q1, 3)).rjust(10)
            eight = str(round(q2, 3)).rjust(10)
            nine = str(round(q3,3)).rjust(10)
            ten = str(round(q4,3)).rjust(10)
            eleven = str(round(make,3)).rjust(10)
            twelve = str(round(good,3)).rjust(10)
            if not very_simple:
                print one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve
            i+=1

        start2 = '2013'
        end2 = '2014'
        url = 'http://www.google.com/finance/historical?q=' + symbol + '&histperiod=daily&startdate=Jan+1%2C+'+ start2 + '&enddate=Dec+31%2C+' + end2 + '&output=csv'
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
            if not very_simple:
                print '# lows, slope from local max, slope from local min, volatility, volume, bull power, bear power, volatility at max, volatility at min'
            if not very_simple:
                print tech[recent]
        except IndexError:
            print 'No recent lows found. Should have bought it a long time ago.'
            continues = False

        if simple:
            continues = False

    if continues:   
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
        runs = min([min(lengths),5])
        if not very_simple:
            print 'indicator','date','recent','closest','% difference','projected value'
        for j in range(runs):
            if not very_simple:
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
                try:
                    if i in [4,5,6]:
                        x /=100000
                        closest /= 100000
                except:
                    pass
                if not very_simple:
                    print i,date , round(x,3), str(round(closest,3)).rjust(15),error , str(round(future_value(date,stock,time,very_simple),3)).rjust(20)

        """ Now we want to look at the dates with the same number of past lows and do a similar analysis on them.
        Why did the good ones do well while the bad ones did badly? Does the new one look more like the good or the bad?"""
        same_num_lows = []
        for date in dates:
            if date != recent:
                if stocks[date][0] == query[0]:
                    same_num_lows.append((date,stocks[date]))
        if not very_simple:
            print '\nDays with the same number of lows as the current lows:'

        for day in same_num_lows:
            if not very_simple:
                print '\n'
            for i in range (1,9):
                x =query[i]
                closest = day[1][i]
                date = day[0]
                try:
                    error = str(round((abs(closest - x)/float(x)),3) * 100).rjust(15)
                except:
                    error = float("inf")
                try:
                    if i in [4,5,6]:
                        x /=100000
                        closest /= 100000
                except:
                    pass
                if not very_simple:
                    print i,date , round(x,3), str(round(closest,3)).rjust(15),error , str(round(future_value(date,stock,time,very_simple),3)).rjust(20)
    continues = True

                

                

