from siriObjects.baseObjects import ClientBoundCommand, AceObject

class AlarmSearch(ClientBoundCommand):
    def __init__(self, minute=0, hour=0):
        super(AlarmSearch, self).__init__("Search", "com.apple.ace.alarm")
        self.minute = minute
        self.hour = hour
    def to_plist(self):
        self.add_property('minute')
        self.add_property('hour')
        return super(AlarmSearch, self).to_plist()
class AlarmSnippet(AceObject):                
    def __init__(self, temporary=False, dialogPhase="Completion", alarms=None):
        super(AlarmSnippet, self).__init__("Snippet", "com.apple.ace.alarm")
        self.temporary = temporary
        self.dialogPhase = dialogPhase
        self.alarms = alarms if alarms != None else []
    def to_plist(self):
        self.add_property('temporary')
        self.add_property('dialogPhase')
        self.add_property('alarms')
        return super(AlarmSnippet, self).to_plist()
class AlarmObject(AceObject):
    def __init__(self, identifier=""):
        super(AlarmObject, self).__init__("Object", "com.apple.ace.alarm")
        self.identifier = identifier
    def to_plist(self):
        self.add_property('identifier')
        return super(AlarmObject, self).to_plist()