import trader as t
import datetime as d

START = d.date(2005, 1, 1)
END = d.date(2015, 10, 30)

trader = t.Trader(10000, START, END)
trader.top_x(10, START, END)
print(trader.balance())