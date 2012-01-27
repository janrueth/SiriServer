from siriObjects.baseObjects import ClientBoundCommand, AceObject

class GetRequestOrigin(ClientBoundCommand):
    def __init__(self, desiredAccuracy="ThreeKilometers", searchTimeout=8.0):
        super(GetRequestOrigin, self).__init__("GetRequestOrigin", "com.apple.ace.system")
        self.desiredAccuracy = desiredAccuracy
        self.searchTimeout = searchTimeout
    def to_plist(self):
        self.add_property('desiredAccuracy')
        self.add_property('searchTimeout')
        return super(GetRequestOrigin, self).to_plist()
class DomainObjectCreate(ClientBoundCommand):
    def __init__(self, object=None):
        super(DomainObjectCreate, self).__init__("DomainObjectCreate", "com.apple.ace.system")
        self.object = object
    def to_plist(self):
        self.add_property('object')
        return super(DomainObjectCreate, self).to_plist()
class DomainObjectRetrieve(ClientBoundCOmmand):
    def __init__(self, identifiers=None):
        super(DomainObjectRetrieve, self).__init__("DomainObjectRetrieve", "com.apple.ace.system")
        self.identifiers = identifiers if identifiers != None else []
    def to_plist(self):
        self.add_property('identifiers')
        return super(DomainObjectRetrieve, self).to_plist()
class DomainObjectCommit(ClientBoundCOmmand):
    def __init__(self, identifier=None):
        super(DomainObjectCommit, self).__init__("DomainObjectCommit", "com.apple.ace.system")
        self.identifier = identifier
    def to_plist(self):
        self.add_property('identifier')
        return super(DomainObjectCommit, self).to_plist()
    
# Calendar Event-related objects
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
    
# Contacts-related objects
class PersonSearch(ClientBoundCommand):
    def __init__(self, name="", scope="Local"):
        super(PersonSearch, self).__init__("PersonSearch", "com.apple.ace.contact")
        self.name = name
        self.scope = scope
    def to_plist(self):
        self.add_property('name')
        self.add_property('scope')
        return super(PersonSearch, self).to_plist()
    
# Alarm-related objects
class AlarmSearch(ClientBoundCommand):
    def __init__(self, minute=0, hour=0):
        super(AlarmSearch, self).__init__("Search", "com.apple.ace.alarm")
        self.minute = minute
        self.hour = hour
    def to_plist(self):
        self.add_property('minute')
        self.add_property('hour')
        return super(AlarmSearch, self).to_plist()