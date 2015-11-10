import trader as t
import datetime as d

START = d.date(2005, 1, 1)
END = d.date(2015, 10, 30)

trader = t.Trader(1000000, START, END)

for x in range(1, 300):
    trader.reset()
    trader.top_x(x, START, END)
    print("Multiplier when x =", x, "is", (trader.balance() - 1000000)/1000000)