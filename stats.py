import pickle
pointMap = pickle.load(open("points.p","rb"))

#Here looking just at daily lows
low = 100000000

#So far, a global low. 52 week low is a little tougher
for point in pointMap:
	if (pointMap[point][3] < low):
		low = pointMap[point][3]
