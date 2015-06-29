__author__ = 'Ahmad'

import cPickle as RuleSave
import os

class Rule:

    def __init__(self):
        self.rule_name = 'Abstract Rule'
        self.action_type = 'Abstraction'
        self.action_sequence = '1'
        self.rule_id = 'R000'
        self.path = "RulesStorage/" + self.action_type + "/"
        try:
            os.makedirs(self.path)
        except:
            raise IOError("Cant Seem to Build " + self.action_type + " directory")
        storagelocation = open(self.path + self.action_sequence + " " + self.rule_id + ".p", 'wb')
        RuleSave.dump([self.rule_name,self.rule_id,self.action_sequence,self.rule_id], storagelocation)

    def execute(self,model_objects):
        # do logic for rule here
        raise NotImplementedError('Logic for Rule Must be Implemented in SubClass')

