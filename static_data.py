_symbol_map_ = {}

for filename in ('static_data_files/nyse.csv', 'static_data_files/nasdaq.csv'):
    f = open(filename).read()
    f = f.split('\n')
    f.pop(0)
    for row in f:
        x = row.split('"')
        symbol = x[1].replace('/', '').replace('^', '').lower()
        cap = x[7]
        ipo = x[9]
        sector = x[11]
        industry = x[13]
        _symbol_map_[symbol] = [cap, ipo, sector, industry]


def symbols():
    return list(_symbol_map_.keys())


def cap(stock_symbol):
    size = _symbol_map_[stock_symbol][0]
    if size == 'n/a':
        return None
    if size[-1] == 'B':
        multiplier = 1000000000
    else:
        multiplier = 1000000
    return int((float(size[1:-1]) * multiplier))


def ipo(stock_symbol):
    ans = _symbol_map_[stock_symbol][1]
    if ans == 'n/a':
        return None
    else:
        return int(ans)


def sector(stock_symbol):
    ans = _symbol_map_[stock_symbol][2]
    if ans == 'n/a':
        return None
    else:
        return ans


def industry(stock_symbol):
    ans = _symbol_map_[stock_symbol][3]
    if ans == 'n/a':
        return None
    else:
        return ans