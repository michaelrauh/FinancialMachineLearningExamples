import math
import stock


def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)


def pearson(x, y):
    assert len(x) == len(y)
    n = len(x)
    if n < 20: # avoid undertrain
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

all_stocks = stock.get_all_stocks()
#dump stocks

train = dict()
run = dict()
for current_stock in all_stocks:
    for date, close in zip(list(reversed(current_stock.all_dates)), list(reversed(current_stock.all_closes))):
        if run_criteria(date):
            if current_stock.symbol not in run:
                run[current_stock.symbol] = list()
            run[current_stock.symbol].append(close)
        elif train_criteria(date):
            if current_stock.symbol not in train:
                train[current_stock.symbol] = list()
            train[current_stock.symbol].append(close)

#dump dicts

def find_corrs(stock_set):
    all_corr = dict()
    for sym_a in stock_set:
        for x in (0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 80, 126, 253):
            shifted_stock = shift(stock_set[sym_a], x)
            for sym_b in all_stocks:
                norm_a, norm_b = normalize(shifted_stock, stock_set[sym_b])
                corr = pearson(norm_a, norm_b)
                all_corr[corr] = (sym_a, sym_b, x)
    return all_corr

train_corr = find_corrs(train)
run_corr = find_corrs(run)

#dump pickles

special_sort(train_corr) #abs, sort and throw out 1s
special_sort(run_corr)


def test(x, train_corr, run_corr):
    top_train = train_corr[:x]
    top_run = run_corr[:x]
    ans = len(set(top_run).intersection(set(top_train)))
    print x * 1.0/ans


def get_results(train_corr, run_corr):
    ans = set()
    i = 100
    while len(ans) < 10:
        top_train = train_corr[:i]
        top_run = run_corr[:i]
        ans = set(top_run).intersection(set(top_train))
        i += 100

    reverse_lookup = {v: k for k, v in top_run.items()}
    x = []
    for thing in ans:
        x.append(thing, reverse_lookup[thing])

    #dump thing
    print thing

for i in range(0,1000,100):
    print i
    test(i, train_corr, run_corr)