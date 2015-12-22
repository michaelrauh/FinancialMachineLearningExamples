from copy import deepcopy


class Event:

    events = dict()

    @classmethod
    def register_event(cls, event, trader_name, symbol):
        if trader_name not in cls.events:
            cls.events[trader_name] = {}
        if symbol not in cls.events[trader_name]:
            cls.events[trader_name][symbol] = list()
        cls.events[trader_name][symbol].append(event)

    @classmethod
    def trigger_all(cls):
        iter_events = deepcopy(cls.events)
        for trader_name in iter_events:
            for symbol in iter_events[trader_name]:
                for event in iter_events[trader_name][symbol]:
                    if event.trigger():
                        event.action()
                        cls.delete_trigger(trader_name, symbol)
            
    @classmethod
    def delete_trigger(cls, trader_name, symbol):
        try:
            del(cls.events[trader_name][symbol])
        except KeyError:
            pass

    def __init__(self, trigger, action, trader_name, symbol):
        self.trigger = trigger
        self.action = action
        Event.register_event(self, trader_name, symbol)

    def fire_if_applicable(self):
        if self.trigger():
            self.action()