print "Parse"
execfile('Parse.py')
del(stocks)
print "stats"
execfile('stats.py')
del(years)
del(all_points)
print "cluster"
execfile('cluster.py')
del(next_good)
del(next_bad)
print "run"
execfile('run.py')
