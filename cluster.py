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
deg_good = [1 for i in range(len(flipped))]
deg_bad = [1 for i in range(len(flipped))]
back_good = [0 for i in range(len(flipped))] #max 47 for this data set. 47 looks at only 1 year
back_bad = [0 for i in range(len(flipped))]

total = 0
for thing in [deg_bad,deg_good]:
        for a in range(1,6):
                for b in range(9):
                        thing[b] = a
                        for guy in [back_good,back_bad]:
                                for c in [0,10,20,30,40,47]:
                                        for d in range(9):
                                                print total
                                                total += 1
                                                """guy[d] = c
                                                next_good = [0 for i in range(len(flipped))]
                                                next_bad = [0 for i in range(len(flipped))]
                                                print 'back_good:', back_good
                                                print 'back_bad:', back_bad
                                                print 'deg_good:',deg_good
                                                print 'deg_bad:', deg_bad
                                                for i in range(0, len(flipped)):
                                                        next_good[i] = extrapolate(avgs[True], i, deg_good[i], back_good[i])
                                                        next_bad[i] = extrapolate(avgs[False], i, deg_bad[i], back_bad[i])
                                                pickle.dump(next_good,open("pickles/next_good.p","wb"))
                                                pickle.dump(next_bad,open("pickles/next_bad.p","wb"))
                                                execfile('run.py')"""
