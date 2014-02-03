"""Calculate f-score by querying results for last valid year"""
from __future__ import division
from helper import distance, good_buy
import cPickle as pickle

next_good = pickle.load(open("pickles/next_good.p","rb"))
next_bad = pickle.load(open("pickles/next_bad.p","rb"))
stocks = pickle.load(open("pickles/all_points.p","rb"))
years = pickle.load(open("pickles/years.p","rb"))

prediction = False
true_positive = 0
true_negative = 0
false_positive = 0
false_negative = 0

for stock in stocks:
    for date in stock:
        year = int(date[0:4])
        if year == years.keys()[-2]:
            point = stock[date]
            actual = good_buy(date,point)
            prediction = distance(next_good,point) < distance (next_bad,point)
            if prediction:
                if prediction == actual:
                    true_positive += 1
                else:
                    false_positive += 1
            else:
                if prediction == actual:
                    true_negative += 1
                else:
                    false_negative += 1
                    
percent_correct = (true_positive + true_negative)/(false_positive + false_negative + true_positive + true_negative)
f = (2 * true_positive) / ((2 * true_positive) + false_positive + false_negative)

if (false_positive + true_positive == 0):
    print "Always chooses False"
elif (false_negative + true_negative == 0):
    print "Always chooses True"
else:
    print "Chooses mixed values!\n"
    print"Percent correct:", percent_correct
    print "F1 Score:", f
    print "\nTrue_positive:", true_positive
    print "True_negative:", true_negative
    print "False_positive:", false_positive
    print "False_negative:", false_negative
