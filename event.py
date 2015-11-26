class Event:
    def __init__(self, trigger, action):
        self.trigger = trigger
        self.action = action

    def fire_if_applicable(self, date):
        if self.trigger(date):
            self.action(date)