import pickle
import os


def get_blacklist(path):
    return pickle.load(open(path, 'rb'))


def write_to_blacklist(path, blacklist):
    pickle.dump(blacklist, open(path, 'wb'))


def blacklisted(path, symbol):
    blacklist = pickle.load(open(path, 'rb'))
    return symbol in blacklist


def blacklist_exists(path):
    return os.path.exists(path)


def path(start_date, end_date):
    return "data/blacklist" + str(start_date) + str(end_date) + ".p"