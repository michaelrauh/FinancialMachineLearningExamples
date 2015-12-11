class Event:
    def __init__(self, trigger, action):
        self.trigger = trigger
        self.action = action

    def fire_if_applicable(self):
        if self.trigger():
            self.action()