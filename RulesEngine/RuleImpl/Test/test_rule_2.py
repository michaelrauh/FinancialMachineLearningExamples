__author__ = 'Ahmad Farag'
__doc__ = 'Test Rule that Takes Input ModelObjects and Prints Out Each Object with the Date'

from RulesEngine.RuleBase.rule import Rule

class TestRuleTwo(Rule):

    def __init__(self):
        self.rule_name = 'Test Rule 2'
        self.action_type = 'Test'
        self.action_sequence = '2'
        self.rule_id = 'R002'
        self.path = "RulesStorage/" + self.action_type + "/"
        try:
            os.makedirs(self.path)
        except:
            raise IOError("Cant Seem to Build " + self.action_type + " directory")
        storagelocation = open(self.path + self.action_sequence + " " + self.rule_id + ".p", 'wb')
        RuleSave.dump([self.rule_name,self.rule_id,self.action_sequence,self.rule_id,self.path], storagelocation)

    def execute(self,model_objects):
        print "Testing:\n"
        for index, object in enumerate(model_objects):
            print index, object
