from stats import *
points = coordinates
#Get centroids for each year
yearPoints={}
years = []

#First we have to separate points by year. This maps years to lists of tuples containing dates and data.
for point in points:
	if not point[0:4] in list(yearPoints):
		yearPoints[point[0:4]] = []
		years.append(point[0:4])
	yearPoints[point[0:4]].append((point,points[point]))
#find centroid trend and predict next year's centroids
