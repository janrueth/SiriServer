
import re
import threading

from siriObjects.baseObjects import ClientBoundCommand, RequestCompleted
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
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
        self.connection.current_running_plugin = None
        self.connection.send_object(RequestCompleted(self.refId))

    def ask(self, text):
        self.waitForResponse = threading.Event()
        view = AddViews(self.refId)
        view.views += [AssistantUtteranceView(text, text, listenAfterSpeaking=True)]
        self.connection.send_object(view)
        self.waitForResponse.wait()
        self.waitForResponse = None
        return self.response

    def getResponseForRequest(self, clientBoundCommand):
        self.waitForResponse = threading.Event()
        if isinstance(clientBoundCommand, ClientBoundCommand):
            self.connection.send_object(clientBoundCommand)
        else:
            self.connection.send_plist(clientBoundCommand)
        self.waitForResponse.wait()
        self.waitForResponse = None
        return self.response
    
    def sendRequestWithoutAnswer(self, clientBoundCommand):
        if isinstance(clientBoundCommand, ClientBoundCommand):
            self.connection.send_object(clientBoundCommand)
        else:
            self.connection.send_plist(clientBoundCommand)

    def say(self, text):
        view = AddViews(self.refId)
        view.views += [AssistantUtteranceView(text, text)]
        self.connection.send_object(view)