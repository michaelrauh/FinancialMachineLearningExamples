def parse_static_info():
    stock_map = dict()
    for filename in ('data/nyse.csv', 'data/nasdaq.csv'):
            f = open(filename).read()
            f = f.split('\n')
            f.pop(0)
            for row in f:
                x = row.split('"')
                symbol = x[1].replace('^', '-')
                ipo = x[9]
                sector = x[11]
                stock_map[symbol] = ipo, sector

    return stock_map


def get_maximums(data):
    return list(reversed(data[2:-1:6]))


def get_dates(data):
    return list(reversed(data[0:-1:6]))