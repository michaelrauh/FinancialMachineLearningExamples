"""Take coordinates from stats and cluster them to determine biy/sell split.
This iteration will use an average location for good/bad as its algorithm.

"""
from helper import avg, extrapolate
import cPickle as pickle
years = pickle.load(open("pickles/years.p","rb"))

# For each year, find average location of good points, average location of
# bad points.
avgs = {}
avgs[True] = {}
avgs[False] = {}
flipped = [0 for i in range(10)]

# Train on all but last valid year
for year in years:
        if year < years.keys()[-3]:
                for good in [True,False]:
                        all_flipped = [[] for i in range (len(flipped))]
                        for stock in years[year][good]:
                                flipped = zip(*years[year][good])
                                for z in range (0,len(flipped)):
                                        all_flipped[z] += flipped[z]
                        if not year in avgs[good]:
                                avgs[good][year] = [0 for i in range(len(flipped))]
                        for z in range (0,len(flipped)):
                                avgs[good][year][z] = avg(all_flipped[z])

# Find centroid trend and predict next year's centroids
next_good = [0 for i in range(len(flipped))]
next_bad = [0 for i in range(len(flipped))]

for i in range(0, len(flipped)):
        next_good[i] = extrapolate(avgs[True], i)
        next_bad[i] = extrapolate(avgs[False], i)

pickle.dump(next_good,open("pickles/next_good.p","wb"))
pickle.dump(next_bad,open("pickles/next_bad.p","wb"))
