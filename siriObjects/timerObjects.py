from siriObjects.baseObjects import ClientBoundCommand, AceObject
from siriObjects.systemObjects import SendCommands, StartRequest
from siriObjects.uiObjects import ConfirmationOptions

class TimerGet(ClientBoundCommand):
    def __init__(self, refId):
        super(TimerGet, self).__init__("Get", "com.apple.ace.timer", None, refId)
    
    def to_plist(self):
        return super(TimerGet, self).to_plist()

class TimerSet(ClientBoundCommand):
    def __init__(self, refId, timer = None):
        super(TimerSet, self).__init__("Set", "com.apple.ace.timer", None, refId)
        self.timer = timer
    
    def to_plist(self):
        self.add_property("timer")
        return super(TimerSet, self).to_plist()

class TimerCancel(ClientBoundCommand):
    def __init__(self, refId):
        super(TimerCancel, self).__init__("Cancel", "com.apple.ace.timer", None, refId)
           
    def to_plist(self):
        return super(TimerCancel, self).to_plist()


class TimerPause(ClientBoundCommand):
    def __init__(self, refId):
        super(TimerPause, self).__init__("Pause", "com.apple.ace.timer", None, refId)
           
    def to_plist(self):
        return super(TimerPause, self).to_plist()

class TimerResume(ClientBoundCommand):
    def __init__(self, refId):
        super(TimerResume, self).__init__("Resume", "com.apple.ace.timer", None, refId)
           
    def to_plist(self):
        return super(TimerResume, self).to_plist()

class TimerSnippet(AceObject):                
    def __init__(self, timers = None, confirm = False):
        super(TimerSnippet, self).__init__("Snippet", "com.apple.ace.timer")
        self.timers = timers if timers != None else []
        if confirm:
            self.confirmationOptions = ConfirmationOptions(
                    submitCommands = SendCommands(StartRequest(utterance="^timerConfirmation^=^yes^ ^timerVerb^=^set^ ^timerNoun^=^timer^")),
                    cancelCommands = SendCommands(StartRequest(utterance="^timerConfirmation^=^no^ ^timerVerb^=^set^ ^timerNoun^=^timer^")),
                    denyCommands = SendCommands(StartRequest(utterance="^timerConfirmation^=^no^ ^timerVerb^=^set^ ^timerNoun^=^timer^")),
                    confirmCommands = SendCommands(StartRequest(utterance="^timerConfirmation^=^yes^ ^timerVerb^=^set^ ^timerNoun^=^timer^")),
                    denyText = "Keep it",
                    cancelLabel = "Keep it",
                    submitLabel = "Change it",
                    confirmText = "Change it",
                    cancelTrigger = "Confirm")
        else:
            self.confirmationOptions = None
    
    def to_plist(self):
        self.add_property('timers')
        if self.confirmationOptions:
            self.add_property('confirmationOptions')
        return super(TimerSnippet, self).to_plist()

class TimerObject(AceObject):
    def __init__(self, timerValue = None, state = None):
        super(TimerObject, self).__init__("Object", "com.apple.ace.timer")
        self.timerValue = timerValue
        self.state = state
    
    def to_plist(self):
        self.add_property('timerValue')
        self.add_property('state')
        return super(TimerObject, self).to_plist()
