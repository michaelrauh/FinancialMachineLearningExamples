import datetime
import time

from market import Market

START_TIME = time.time()
START_ERA = datetime.date(2005, 1, 1)
END_ERA = datetime.date(2015, 10, 30)
START_SIM = datetime.date(2005, 1, 1)
END_SIM = datetime.date(2015, 10, 30)

Market.initialize(START_ERA, END_ERA)

while Market.date < END_SIM - datetime.timedelta(30):
    Market.tick()

END_TIME = time.time()
minutes, seconds = divmod(END_TIME-START_TIME, 60)
print("total time elapsed: ", minutes, "m", seconds, "s")