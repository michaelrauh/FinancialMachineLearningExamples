import math


def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)


def pearson(x, y):
    assert len(x) == len(y)
    n = len(x)
    if n < 30: #make > 30 to avoid undertrain
        return 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)


def shift(prices, shift): # TODO make sure dates are earlier to later
    return prices[shift:]


def normalize(x, y):
    # make same length
    if len(x) > len(y):
        x = x[:len(y)]
    else:
        y = y[:len(x)]

    # make less than a year to avoid overtrain
    if len(x) > 253:
        extra = len(x) - 253
        x = x[extra:]
        y = y[extra:]

    return x, y

all_stocks = get_all_stocks_closes() #returns map sym -> list of closes for last two years (max)

all_corr = dict()

for sym_a in all_stocks:
    for x in (0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 80, 126, 253):
        shifted_stock = shift(all_stocks[sym_a], x)
        for sym_b in all_stocks:
            norm_a, norm_b = normalize(shifted_stock, all_stocks[sym_b])
            corr = pearson(norm_a, norm_b)
            if corr not in all_corr:
                all_corr[corr] = list()
            all_corr[corr].append(sym_a, sym_b, x)