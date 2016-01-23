import datetime
import time

import trader
import grapher
from market import Market
from parser import DataOrder
import strategy_thief
import shift_trader

START_TIME = time.time()
START_ERA = datetime.date(2005, 1, 1)
END_ERA = datetime.date(2015, 10, 30)
START_SIM = datetime.date(2005, 1, 1)
END_SIM = datetime.date(2015, 10, 30)

Market.initialize(START_ERA, END_ERA)

for tolerance in [.95]:
    for window in [2]:
        for horizon in [2]:
            Market.traders.append(shift_trader.ShiftTrader(10000, "vanilla", 5, horizon, tolerance, window))

while Market.date < END_SIM - datetime.timedelta(30):
    if Market.time in [DataOrder.close]:
        for trader in Market.traders:
            trader.trade()
    Market.tick()

for trader in Market.traders:
    grapher.graph(trader.all_net_worths, trader.portfolio.value() + trader.account.balance, trader.horizon, trader.portfolio_size, START_SIM, END_SIM, trader.price_change, trader.blacklist_duration, trader.strategy)

END_TIME = time.time()
minutes, seconds = divmod(END_TIME-START_TIME, 60)
print("total time elapsed: ", minutes, "m", seconds, "s")