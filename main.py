import trader as t
import datetime as d
import matplotlib.pyplot as plt
import os

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)
HORIZON = 365

trader = t.Trader(1000000, START_ERA, END_ERA)
balances = []

x = 1
trader.reset()
trader.top_x(x, START_SIM, END_SIM, HORIZON, balances)
plt.plot(balances)
os.makedirs('output', exist_ok=True)
plt.savefig('output/' + str(START_SIM) + str(END_SIM) + str(HORIZON) + str(x) + 'output.png', bbox_inches='tight')
plt.show()
print("Multiplier when x =", x, "is", (trader.balance() - 1000000)/1000000)