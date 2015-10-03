import cPickle as pickle
portfolio_size = 1
FTW = 253

def sort_symbols(day):
    differences = day.keys()
    differences = sorted(differences)
    symbols = []
    for difference in differences:
        symbols.append(day[difference])
    return symbols # make sure not backward

class User(portfolio_size):
    user.portfolio = []
    user.cash = 10000

stocks = pickle.load('all_stocks.p')

#organize by date. Before this is done, get the percent increase over the year instead of the high:

days = {}

for stock in stocks:
    for day in stock.dates:
        high = stock[day].high
        if day not in days:
            days[day] = dict()
        days[day].append({high: stock.symbol})

user = User(portfolio_size)

for i in range(FTW, len(days)):
    todays_symbols = sort_symbols(days[i])
    todays_portfolio = todays_symbols[:portfolio_size]
    for item in user.portfolio:
        if item not in todays_portfolio:
            user.sell(item)
    for item in todays_portfolio:
        if item not in user.portfolio:
            user.add_to_cart(item)
    user.complete_purchase()

for item in user.portfolio:
    user.sell(item)
print user.cash