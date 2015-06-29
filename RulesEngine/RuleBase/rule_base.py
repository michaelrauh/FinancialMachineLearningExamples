__author__ = 'Ahmad Farag'
import rule
from os import listdir
from os.path import isfile, isdir, join
import cPickle as local_rule_base

class RuleBase:

    def __init__(self):
        self.name = "Rule Base"
        self.rules = []
        print "Loading Rules"
        # rules = local_rule_base.load(open("data/pickles/" + symbol + "/" + date + ".p", "rb"))
        impl_path = '../RuleImpl'
        actiontype_directories = [ f for f in listdir(impl_path) if isdir(join(impl_path,f))]
        print "Action Types Found: " + actiontype_directories.__str__() + "\n"
        for actiontype in actiontype_directories:
            action_path = impl_path+"/"+actiontype
            actiontype_rules = [ f for f in listdir(action_path ) if isfile(join(action_path ,f))]
            print "Rules of ActionType " + actiontype + "\n\t" + actiontype_rules.__str__() + "\n"

    def load_from_name(name):

        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod


# x = RuleBase()