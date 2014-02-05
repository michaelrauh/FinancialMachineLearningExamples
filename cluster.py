"""Take coordinates from stats and cluster them to determine biy/sell split.
This iteration will use an average location for good/bad as its algorithm.

"""
from helper import avg, extrapolate
import cPickle as pickle
years = pickle.load(open("pickles/years.p","rb"))

# For each year, find average location of good points, average location of
# bad points. Look into "zip" to optimize.
avg_good = {}
avg_bad = {}

# Train on all but last valid year
for year in years:
        if year < years.keys()[-1]:
                for stock in years[year][True]:
                        flipped = zip(*years[year][True])
                for n in range(0, len(flipped)):
                        if not year in avg_good:
                                avg_good[year] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                        avg_good[year][n] = avg(flipped[n])

# Code repeated for bad. Refactor this
for year in years:
        if year < years.keys()[-1]:
                for stock in years[year][False]:
                        flipped = zip(*years[year][False])
                for n in range(0, len(flipped)):
                        if not year in avg_bad:
                                avg_bad[year] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                        avg_bad[year][n] = avg(flipped[n])

# Find centroid trend and predict next year's centroids
next_good = [0, 0, 0, 0, 0, 0, 0, 0, 0]
next_bad = [0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(0, len(flipped)):
        next_good[i] = extrapolate(avg_good, i)
        next_bad[i] = extrapolate(avg_bad, i)

pickle.dump(next_good,open("pickles/next_good.p","wb"))
pickle.dump(next_bad,open("pickles/next_bad.p","wb"))
