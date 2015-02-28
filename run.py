import pickle
import sys

preferences = []

class Preference:
    def get(self):
            self.start = input("enter a start date: ")
            self.end = input("enter an end date: ")
            self.min_cap = input("enter a min company size in dollars: ")
            self.max_cap = input("enter a max company size in dollars: ")
            self.sectors = input("enter a space separated list of sectors: ").split(' ')
            self.industries = input("enter a space separated list of industries: ").split(' ')

while (input("press q to stop putting in more preferences: ") != 'q'):
    x = Preference()
    x.get()
    preferences.append(x)
