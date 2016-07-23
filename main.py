import datetime
import time

from market import Market
from parser import DataOrder
import matplotlib.pyplot as plt
import statistics
import math

START_TIME = time.time()
START_ERA = datetime.date(2005, 1, 1)
END_ERA = datetime.date(2015, 10, 30)
START_SIM = datetime.date(2005, 1, 1)
END_SIM = datetime.date(2015, 10, 30)

Market.initialize(START_ERA, END_ERA)

while Market.date < END_SIM - datetime.timedelta(30):
    if Market.time in [DataOrder.close] and Market.date > START_ERA + datetime.timedelta(days=365):
        Market.find_todays_profile()
    Market.tick()
    print(Market.date)

final_highs = {i: [] for i in range(100)}
for high_number in range(100):
    if high_number in Market.interesting_stocks:
        all_on_high = Market.interesting_stocks[high_number]
        highest_date = None
        highest_count = 0
        for date in all_on_high:
            if len(all_on_high[date]) > highest_count:
                highest_count = len(all_on_high[date])
                highest_date = date
        del(all_on_high[highest_date])
        for date in all_on_high:
            for thing in all_on_high[date]:
                final_highs[high_number].append(thing)

means = []
intervals = []

for key in final_highs:
    final_highs[key] = [x for x in final_highs[key] if x != 0]

for i in range(100):
    if i in final_highs.keys():
        l = final_highs[i]
        try:
            mean = float(sum(l))/len(l)
            dev = statistics.stdev(l)
            n = len(l)
            std_error = dev/math.sqrt(n)
            interval = 1.96 * std_error
        except:
            mean = 0
            interval = 0
        means.append(mean)
        intervals.append(interval)

plt.errorbar(range(len(means)), means, yerr=intervals)
plt.savefig("output/" + "means" + ".png")
plt.gcf().clear()

END_TIME = time.time()
minutes, seconds = divmod(END_TIME-START_TIME, 60)
print("total time elapsed: ", minutes, "m", seconds, "s")