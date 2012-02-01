import re
import threading
import logging

from siriObjects.baseObjects import ClientBoundCommand, RequestCompleted
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
__criteria_key__ = "criterias"

__error_responses__ = {"de-DE": "Es ist ein Fehler in der Verarbeitung ihrer Anfrage aufgetreten!", "en-US": "There was an error during the processing of your request!", "en-GB": "There was an error during the processing of your request!", "en-AU": "There was an error during the processing of your request!", "fr-FR": "Il y avait une erreur lors du traitement de votre demande!"}

def register(lang, regex):
    def addInfosTo(func):
        if not __criteria_key__ in func.__dict__:
            func.__dict__[__criteria_key__] = dict()
        crits = func.__dict__[__criteria_key__]
        crits[lang] = re.compile(regex, re.IGNORECASE)
        return func
    return addInfosTo

class Plugin(threading.Thread):
    def __init__(self, method, speech, language):
        super(Plugin, self).__init__()
        self.__method = method
        self.__lang = language
        self.__speech = speech
        self.waitForResponse = None
        self.response = None
        self.refId = None
        self.connection = None
        self.logger = logging.getLogger("logger")
    
    def run(self):
        try:
            try:
                self.__method(self, self.__speech, self.__lang)
            except:
                self.logger.exception("Unexpected during plugin processing")
                self.say(__error_responses__[self.__lang])
                self.complete_request()
        except:
            pass
        self.connection.current_running_plugin = None

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

    def say(self, text, speakableText=""):
        view = AddViews(self.refId)
        if speakableText == "":
            speakabletext = text
        view.views += [AssistantUtteranceView(text, speakableText)]
        self.connection.send_object(view)