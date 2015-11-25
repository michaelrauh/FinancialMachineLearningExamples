import trader as t
import datetime as d
import grapher as g

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

trader = t.Trader(1000000, START_ERA, END_ERA)

for x in [1]:
    for horizon in [55]:
        balances = []
        trader.reset()
        trader.top_x(x, START_SIM, END_SIM, horizon, balances)
        g.graph(balances, trader.balance(), horizon, x, START_SIM, END_SIM)
        print("x=", x, "horizon=", horizon, "balance=", (trader.balance()))