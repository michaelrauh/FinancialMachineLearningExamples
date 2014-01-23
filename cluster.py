"""Take coordinates from stats and cluster them to determine biy/sell split. This iteration will use an average location for good/bad as its algorithm"""

import cPickle as pickle
years = pickle.load(open("pickles/years.p","rb"))
def avg(points):
        if sum(points) != 0:
                return sum(points)/len(points)
        else:
                return 0

def extrapolate(avg,i): # Obviously not a very good function yet
        years = list(avg.keys())
        years.sort()
        diff = avg[years[-1]][i] - avg[years[-2]][i]
        return avg[years[-1]][i] + diff

# For each year, find average location of good points, average location of bad points.
avg_good = {}
avg_bad = {}
flipped = [[],[],[],[],[],[],[],[],[]]
for year in years:
        for stock in years[year][True]:
                for i in range(0,len(flipped)):
                        flipped[i].append(stock[i])
        for n in range (0,len(flipped)):
                if not year in avg_good:
                        avg_good[year] = [0,0,0,0,0,0,0,0,0]
                avg_good[year][n] = avg(flipped[n])

# Code repeated for bad. Refactor this
for year in years:
        for stock in years[year][False]:
                for i in range(0,len(flipped)):
                        flipped[i].append(stock[i])
        for n in range (0,len(flipped)):
                if not year in avg_bad:
                        avg_bad[year] = [0,0,0,0,0,0,0,0,0]
                avg_bad[year][n] = avg(flipped[n])
                        
# Find centroid trend and predict next year's centroids
next_good = [0,0,0,0,0,0,0,0,0]
next_bad = [0,0,0,0,0,0,0,0,0]

for i in range (0,len(flipped)):
        next_good[i] = extrapolate(avg_good,i)
        next_bad[i] = extrapolate(avg_bad,i)

pickle.dump(next_good,open("pickles/next_good.p","wb"))
pickle.dump(next_bad,open("pickles/next_bad.p","wb"))
