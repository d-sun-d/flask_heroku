class ActionResponse(object):
    def __init__(self):
        self.count = 0
        self.messages = []
        self.forced = None
        self.keyboard = None
        self.entities = None

    def to_dict(self):
        res = {}
        res['Count'] = self.count
        res['Messages'] = self.messages
        res['ForcedState'] = self.forced
        res['ForcedKeyboard'] = self.keyboard
        res['Entities'] = self.entities
        return res