
import re
import threading


__criteria_key__ = "criterias"

def register(lang, regex):
    def addInfosTo(func):
        if not __criteria_key__ in func.__dict__:
            func.__dict__[__criteria_key__] = dict()
        crits = func.__dict__[__criteria_key__]
        crits[lang] = re.compile(regex, re.IGNORECASE)
        return func
    return addInfosTo

class Plugin(object):
    def __init__(self):
        self.waitForResponse = None
        self.response = None
        self.refId = None
        self.connection = None

    def complete_request(self):
        pass

    def ask(self, text):
        self.waitForResponse = threading.Event()
        self.connection.send_object() #<- this needs to be thread safe
        self.waitForResponse.wait()
        return self.response
    
    def say(self, text):
        self.connection.send_object()