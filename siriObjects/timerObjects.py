from siriObjects.baseObjects import ClientBoundCommand, AceObject


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


class TimerSnippet(AceObject):                
    def __init__(self, timers = None):
        super(TimerSnippet, self).__init__("Snippet", "com.apple.ace.timer")
        self.timers = timers if timers != None else []
    
    def to_plist(self):
        self.add_property('timers')
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