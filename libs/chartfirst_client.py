import json
import requests

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



def send_push(botname = "StaffAccorDemoBot", messages=[], recever_id=1298445):
    data = {}
    headers = {}
    headers['Authorization'] = "Basic MzM4RkM1MzFGMzk4N0E1MTA4RkM0RTUzNzg2QUUwQjQwRUM0NjNCODo="
    headers["Content-Type"] = "application/json"
    data['Count'] = 1
    data['Messages'] = messages
    data['ForcedState'] = None
    data['ForcedKeyboard'] = None
    params = {}
    params["id"] = int(recever_id)
    params["channel"] = "telegram"

    res = requests.post("https://ch-message-processor-test.azurewebsites.net/v1/push/"+botname,headers=headers, data=json.dumps(data), params=params)
    print res.url
    print res.status_code