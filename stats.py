import pickle
pointMap = pickle.load(open("points.p","rb"))

#Here looking just at daily lows
low = 100000000
i=0
yearLows = []

#So far, a global low. 52 week low is a little tougher.
for point in pointMap:
	if (pointMap[point][3] < low):
		low = pointMap[point][3]

#For each 52 week low, we want to know:
#1: number of 52 week lows in last 10 days
#2: slope from local min
#3: slope from local max

#These will be mapped to the date and pickled out
