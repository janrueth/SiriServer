from siriObjects.baseObjects import ClientBoundCommand, AceObject

class EventSearch(ClientBoundCommand):
    def __init__(self, timeZoneId="America/Chicago", startDate=None, endDate=None, limit=10):
        super(EventSearch, self).__init__("EventSearch", "com.apple.ace.calendar")
        self.timeZoneId = timeZoneId
        self.startDate = startDate
        self.endDate = endDate
        self.limit = limit
    def to_plist(self):
        self.add_property('timeZoneId')
        self.add_property('startDate')
        self.add_property('endDate')
        self.add_property('limit')
        return super(EventSearch, self).to_plist()
class EventObject(AceObject):
    def __init__(self, timeZoneId="America/Chicago", title="", startDate=None, endDate=None):
        super(EventObject, self).__init__("Event", "com.apple.ace.calendar")
        self.timeZoneId = timeZoneId
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
    def to_plist(self):
        self.add_property('timeZoneId')
        self.add_property('title')
        self.add_property('startDate')
        self.add_property('endDate')
        return super(EventObject, self).to_plist()
class EventSnippet(AceObject):
    def __init__(self, temporary=False, dialogPhase="Confirmation", events=None, confirmationOptions=None):
        super(EventSnippet, self).__init__("EventSnippet", "com.apple.ace.calendar")
        self.temporary = temporary
        self.dialogPhase = dialogPhase
        self.events = events if events != None else []
        self.confirmationOptions = confirmationOptions
    def to_plist(self):
        self.add_property('temporary')
        self.add_property('dialogPhase')
        self.add_property('events')
        self.add_property('confirmationOptions')
        return super(EventSnippet, self).to_plist()
class ExistingEventObject(AceObject):
    def __init__(self, identifier=""):
        super(ExistingEventObject, self).__init__("Event", "com.apple.ace.calendar")
        self.identifier = identifier
    def to_plist(self):
        self.add_property('identifier')
        return super(ExistingEventObject, self).to_plist()