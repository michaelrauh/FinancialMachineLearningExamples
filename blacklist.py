import pickle
import os


def get_blacklist(filename):
    return pickle.load(open(filename, 'rb'))


def write_to_blacklist(filename, blacklist):
    pickle.dump(blacklist, open(filename, 'wb'))


def blacklisted(filename, symbol):
    blacklist = pickle.load(open(filename, 'rb'))
    return symbol in blacklist


def blacklist_exists(filename):
    return os.path.exists(filename)


def path(start_date, end_date):
    return "data/blacklist" + str(start_date) + str(end_date) + ".p"