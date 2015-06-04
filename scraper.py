import urllib2


def get_todays_symbols():
        f = urllib2.urlopen("http://www.barchart.com/stocks/high.php?_dtp1=0").read()
        symbols = f[f.find("symbols") + len("symbols\" value=\""):f.find("/>", f.find("symbols"))-2].split(',')
        return symbols


def get_data(symbol, ipo):
        """Get Data from Google Finance"""
        if ipo == 'n/a':
            ipo = '1972'

        try:
            PRESENT = '2015'
            url = 'http://www.google.com/finance/historical?q=' + symbol + \
                  '&histperiod=daily&startdate=Jan+1%2C+' + ipo + \
                  '&enddate=Dec+31%2C+' + PRESENT + '&output=csv'
            f = urllib2.urlopen(url).read()
            points = f.replace('\n', ',').split(',')
        # TODO: catch specific error
        except:
            points = []
        return points