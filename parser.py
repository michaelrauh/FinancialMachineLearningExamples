def parse_static_info():
    stock_map = dict()
    for filename in ('data/nyse.csv', 'data/nasdaq.csv'):
            f = open(filename).read()
            f = f.split('\n')
            f.pop(0)
            for row in f:
                x = row.split('"')
                symbol = x[1].replace('^', '-') # TODO: make sure yahoo works like this
                ipo = x[9]
                sector = x[11]
                stock_map[symbol] = ipo, sector

    return stock_map

# TODO: Make sure there are no junk values. Smooth these out by averaging adjacent entries

def get_maximums(data):
    return list(reversed(data[2::7]))


def get_dates(data):
    return list(reversed(data[0::7]))


def get_closes(data):
    return list(reversed(data[4::7]))