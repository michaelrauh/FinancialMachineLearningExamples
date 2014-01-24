"""Query trained data on new stock"""

from helper import *
import cPickle as pickle

next_good = pickle.load(open("pickles/next_good.p","rb"))
next_bad = pickle.load(open("pickles/next_bad.p","rb"))

# Parse
file = open("input.csv",'r')
data = file.read()
test = parse(data)

# Stats
test_coordinates = find_coordinates(test)
normalize(test_coordinates)

print ("echo chosen date")
for value in list(test_coordinates.keys()):
    print value
#choice = raw_input()
choice = list(test_coordinates.keys())[0]
question = test_coordinates[choice]

# Predict
print (distance(next_good,question) < distance (next_bad,question))
