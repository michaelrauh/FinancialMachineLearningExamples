import trader as t
import datetime as d

START = d.date(2005, 1, 1)
END = d.date(2015, 10, 30)
HORIZON = 365

trader = t.Trader(1000000, START, END)

x = 5
trader.reset()
trader.top_x(x, START, END, HORIZON)
print("Multiplier when x =", x, "is", (trader.balance() - 1000000)/1000000)