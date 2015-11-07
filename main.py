import trader as t
import datetime as d

START = d.date(2005, 1, 1)
END = d.date(2015, 10, 30)

trader = t.Trader(1000000, START, END)

for x in range(1, 500):
    trader.reset()
    trader.top_x(500, START, END)
    print("final balance when x = ", x, "is", trader.balance())