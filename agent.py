""" This module will run run.py, simulating users at different risk levels. The goal is to find a risk
level that is not 100% (this is a naive buy all strategy) which gives greater returns than the market average.
This module may also specify preference for hashing method used, submarkets to examine, and rulesets to base
risk levels on. Therefore, it will essentially run run.py with the parameters:

submarkets
risk
hasher
ruleset

It will run an optimization strategy on each vector. If vectors counterindicate (overtrain), it will
run pairwise. If overtraining always occurs before acceptance criteria is met, the project will fail.
"""
