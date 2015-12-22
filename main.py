import trader as t
import datetime as d
import grapher as g
import market as m
import time

start_time = time.time()

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

market = m.Market(START_ERA, END_ERA)
current_date = START_SIM
traders = []


def hash(port, loss, black, strategy):
    return str(port) + str(loss) + str(black) + strategy

for portfolio_size in [2, 3, 5, 8]:
    for loss in [-.1, -.05]:
        for blacklist_duration in [30]:
            for strategy in ["vanilla", "stop_loss"]:
                name = hash(portfolio_size, loss, blacklist_duration, strategy)
                traders.append(t.Trader(name, 10000, market, strategy, portfolio_size, 365, loss, blacklist_duration))

for trader in traders:
    print(trader.portfolio_size, trader.loss, trader.blacklist_duration, trader.strategy)

balances = [[] for i in range(len(traders))]

while current_date < END_SIM - d.timedelta(30):
    for trader, i in zip(traders, range(len(traders))):
        trader.trade()
        balances[i].append(trader.portfolio.value() + trader.account.balance)
    market.tick()
    current_date = market.date

for trader, i in zip(traders, range(len(traders))):
    g.graph(balances[i], trader.portfolio.value() + trader.account.balance, trader.horizon, trader.portfolio_size,
            START_SIM, END_SIM, trader.loss, trader.blacklist_duration, i, trader.strategy)

end_time = time.time()

print("total time elapsed:", (end_time - start_time)/60, "minutes")