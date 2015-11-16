import trader as t
import datetime as d
import matplotlib.pyplot as plt
import os

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

trader = t.Trader(1000000, START_ERA, END_ERA)

for x in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]:
    for horizon in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]:
        balances = []
        trader.reset()
        trader.top_x(x, START_SIM, END_SIM, horizon, balances)
        plt.plot(balances)
        plt.title("x=" + str(x) + ", horizon=" + str(horizon) + ", balance=" + str(round(trader.balance(), 2)))
        plt.xlabel("number of days after Jan. 1, 2005")
        plt.ylabel("Portfolio value (USD)")
        os.makedirs('output', exist_ok=True)
        plt.savefig('output/' + str(START_SIM) + "_" + str(END_SIM) + "_" + str(x) + "_" + str(horizon) + '.png', bbox_inches='tight')
        plt.gcf().clear()
        print("x=", x, "horizon=", horizon, "balance=", (trader.balance()))