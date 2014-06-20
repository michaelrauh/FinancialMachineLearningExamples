"""Take coordinates from stats and cluster them to determine buy/sell split.
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
extend = list.extend
append = list.append

def flatten(l):
        try:
                return [item for sublist in l for item in sublist]
        except:
                return l

# Train on all but last valid year
for year in years:
        if year < years.keys()[-3]:
                for good in [True,False]:
                        all_flipped = [[] for i in range (len(flipped))]
                        for stock in years[year][good]:
                                flipped = zip(*years[year][good])
                                for z in range (0,len(flipped)):
                                        append(all_flipped[z],flipped[z])
                        for x in range(0,len(flipped)):
                                all_flipped[x] = flatten(flipped[x])
                        if not year in avgs[good]:
                                avgs[good][year] = [0 for i in range(len(flipped))]
                        for z in range (0,len(flipped)):
                                avgs[good][year][z] = avg(all_flipped[z])



#this stuff drives the rest and must be brute forced
deg_good = [0 for i in range(9)]
deg_bad = [0 for i in range(9)]
back_good = [0 for i in range(len(flipped))] #max 47 for this data set. 47 looks at only 1 year
back_bad = [0 for i in range(len(flipped))]

for place in range(9):
        deg_good = [0 for i in range(9)]
        deg_bad = [0 for i in range(9)]
        for deg1 in range(10):
                deg_good[place] = deg1
                for deg2 in range(10):
                        deg_bad[place] = deg2
                        next_good = [0 for i in range(len(flipped))]
                        next_bad = [0 for i in range(len(flipped))]
                        for i in range(0, len(flipped)):
                                next_good[i] = extrapolate(avgs[True], i, deg_good[i], 0)
                                next_bad[i] = extrapolate(avgs[False], i, deg_bad[i], 0)
                        pickle.dump(next_good,open("pickles/next_good.p","wb"))
                        pickle.dump(next_bad,open("pickles/next_bad.p","wb"))
                        print deg_good, deg_bad
                        execfile('run.py')
