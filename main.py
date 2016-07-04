import datetime
import time

from market import Market
from parser import DataOrder

START_TIME = time.time()
START_ERA = datetime.date(2005, 1, 1)
END_ERA = datetime.date(2015, 10, 30)
START_SIM = datetime.date(2005, 1, 1)
END_SIM = datetime.date(2015, 10, 30)

all_highs = []

Market.initialize(START_ERA, END_ERA)

while Market.date < END_SIM - datetime.timedelta(30):
    if Market.time in [DataOrder.close]:
        all_highs.append(Market.find_todays_profile())
    Market.tick()

final_highs = {}
for high_profile in all_highs:
    for high_number in high_profile.keys():
        if high_number not in final_highs:
            final_highs[high_number] = 0
        final_highs[high_number] += high_profile[high_number]

END_TIME = time.time()
minutes, seconds = divmod(END_TIME-START_TIME, 60)
print("total time elapsed: ", minutes, "m", seconds, "s")
print(all_highs)
print(final_highs)