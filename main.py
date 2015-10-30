import trader as t
import datetime as d

START = d.date(2005, 0, 0)
END = d.date(2015, 10, 30)

trader = t.Trader(10000)
trader.top_x(1, START, END)
print(trader.balance())