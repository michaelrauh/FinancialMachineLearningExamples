import trader as t
import datetime as d
import matplotlib.pyplot as plt
import os

START = d.date(2005, 1, 1)
END = d.date(2015, 10, 30)
HORIZON = 365

trader = t.Trader(1000000, START, END)
balances = []

x = 1
trader.reset()
trader.top_x(x, START, END, HORIZON, balances)
plt.plot(balances)
os.makedirs('output', exist_ok=True)
plt.savefig('output/' + str(START) + str(END) + str(HORIZON) + str(x) + 'output.png', bbox_inches='tight')
plt.show()
print("Multiplier when x =", x, "is", (trader.balance() - 1000000)/1000000)