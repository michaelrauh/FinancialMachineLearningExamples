import urllib2
import os
import datetime
import cPickle as pickle


def get_todays_symbols():
        f = urllib2.urlopen("http://www.barchart.com/stocks/high.php?_dtp1=0").read()
        symbols = f[f.find("symbols") + len("symbols\" value=\""):f.find("/>", f.find("symbols"))-2].split(',')
        return symbols


def get_data(symbol, ipo):
    date = str(datetime.date.today())

    try:
        points = pickle.load(open("data/pickles/" + symbol + "/" + date + ".p", "rb"))
    except:
        """Get Data from Google Finance"""
        if ipo == 'n/a':
            ipo = '1972'

        try:
            present = str(datetime.date.today().year)
            url = 'http://www.google.com/finance/historical?q=' + symbol + \
                  '&histperiod=daily&startdate=Jan+1%2C+' + ipo + \
                  '&enddate=Dec+31%2C+' + present + '&output=csv'
            f = urllib2.urlopen(url).read()
            points = f.replace('\n', ',').split(',')
        except:
            points = []
        try:
            os.makedirs("data/pickles/" + symbol + "/")
        except:
            pass
        f = open("data/pickles/" + symbol + "/" + date + ".p", 'wb')
        pickle.dump(points, f)
    return points