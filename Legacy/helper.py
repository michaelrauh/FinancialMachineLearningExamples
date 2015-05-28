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
