import datetime as d
import time

import trader as t
import grapher as g
from market import Market
from parser import DataOrder
import matplotlib.pyplot as plt


start_time = time.time()

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

Market.initialize(START_ERA, END_ERA)
traders = []
portfolio_size = 8
traders.append(t.Trader(10000, "vanilla", portfolio_size, 365))

apple = Market.price_map["aapl"]

def perf(start, end):
    return (end-start)/start

questions = []
answers = []

while Market.date < END_SIM - d.timedelta(30):
    if Market.time == DataOrder.open:
        open_price = apple[Market.date][0]
        close_price = apple[Market.date][3]
        next_open = apple[Market.date + d.timedelta(days=1)][0]
        question = perf(open_price, close_price)
        answer = perf(close_price, next_open)
        questions.append(question)
        answers.append(answer)
    Market.tick()

plt.scatter(questions, answers)
plt.show()
end_time = time.time()

print("total time elapsed:", (end_time - start_time)/60, "minutes")