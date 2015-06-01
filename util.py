import urllib2


def scrape(symbol, ipo):
        """Get Data from Google Finance"""
        if ipo == 'n/a':
            ipo = '1972'

        try:
            PRESENT = '2014'
            url = 'http://www.google.com/finance/historical?q=' + symbol + \
                  '&histperiod=daily&startdate=Jan+1%2C+'+ ipo + \
                  '&enddate=Dec+31%2C+' + PRESENT + '&output=csv'
            f = urllib2.urlopen(url).read()
            points = f.replace('\n', ',').split(',')
        except:
            points = []
        return points