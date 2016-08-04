import datetime as d
import time

import trader as t
import grapher as g
from market import Market
from parser import DataOrder


start_time = time.time()

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

Market.initialize(START_ERA, END_ERA)
traders = []
portfolio_size = 8
traders.append(t.Trader(10000, "vanilla", portfolio_size, 365))

while Market.date < END_SIM - d.timedelta(30):
    if Market.time in [DataOrder.open, DataOrder.close]:
        for trader, i in zip(traders, range(len(traders))):
            trader.trade()
    Market.tick()

balances = [trader.all_net_worths for trader in traders]
for trader, i in zip(traders, range(len(traders))):
    g.graph(balances[i], trader.portfolio.value() + trader.account.balance, trader.horizon, trader.portfolio_size,
            START_SIM, END_SIM, trader.price_change, trader.blacklist_duration, i, trader.strategy)

end_time = time.time()

print("total time elapsed:", (end_time - start_time)/60, "minutes")