"""Take coordinates from stats and cluster them to determine buy/sell split.
This iteration will use an average location for good/bad as its algorithm.

"""
import numpy as np
from helper import avg, extrapolate
import cPickle as pickle
import warnings
warnings.simplefilter('ignore', np.RankWarning)

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
#one at a time -> much worse than spline
#deg_good = [9,9,9,5,1,1,1,5,3] 
#deg_bad = [8,2,2,9,0,0,0,2,2]

#two at a time -> slightly worse than spline                                
#deg_good = [2,0,5,5,1,1,1,4,0]
#deg_bad = [9,9,9,2,0,0,0,9,9]

#info from varying timescales trying each good/bad covarying combo
#multivalue back seems to be giving odd division by zero
#back = [38,47,47,47,38,47,47,47,47] # 48 means ignore all years. 47 all but last
#deg_good = [0,0,0,0,0,0,1,0,0]
#deg_bad = [7,8,7,5,9,7,7,5,6]

#single best score
#back = 37
#deg_good = [0,0,0,0,0,0,1,0,0]
#deg_bad = [0,0,0,0,0,0,7,0,0]

#back one year amalgamation
back = 37
deg_good = [3,0,0,0,7,0,1,0,0]
deg_bad = [9,8,7,5,5,7,7,5,6]

next_good = [0 for i in range(len(flipped))]
next_bad = [0 for i in range(len(flipped))]
for i in range(0, len(flipped)):
        next_good[i] = extrapolate(avgs[True], i, deg_good[i], 37)
        next_bad[i] = extrapolate(avgs[False], i, deg_bad[i], 37)
pickle.dump(next_good,open("pickles/next_good.p","wb"))
pickle.dump(next_bad,open("pickles/next_bad.p","wb"))
print deg_good, deg_bad
execfile('run.py')
