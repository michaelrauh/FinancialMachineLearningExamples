_symbol_map_ = {}

for filename in ('static_data/nyse.csv', 'static_data/nasdaq.csv'):
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


def cap(symbol):
    cap = _symbol_map_[symbol][0]
    if cap == 'n/a':
        return None
    if cap[-1] == 'B':
        mult = 1000000000
    else:
        mult = 1000000
    return int((float(cap[1:-1]) * mult))


def ipo(symbol):
    ans = _symbol_map_[symbol][1]
    if ans == 'n/a':
        return None
    else:
        return int(ans)


def sector(symbol):
    ans = _symbol_map_[symbol][2]
    if ans == 'n/a':
        return None
    else:
        return ans


def industry(symbol):
    ans = _symbol_map_[symbol][3]
    if ans == 'n/a':
        return None
    else:
        return ans