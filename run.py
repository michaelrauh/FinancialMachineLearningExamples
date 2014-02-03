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
print(percent_correct)
# good = distance(next_good,question) < distance (next_bad,question)
