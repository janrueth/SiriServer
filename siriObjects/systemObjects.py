from siriObjects.baseObjects import ClientBoundCommand, AceObject, ServerBoundCommand

class GetRequestOrigin(ClientBoundCommand):
    desiredAccuracyThreeKilometers = "ThreeKilometers"
    desiredAccuracyKilometer = "Kilometer"
    desiredAccuracyHundredMeters = "HundredMeters"
    desiredAccuracyNearestTenMeters = "NearestTenMeters"
    desiredAccuracyBest = "Best"
    
    def __init__(self, refId, desiredAccuracy=desiredAccuracyHundredMeters, maxAge=None, searchTimeout=8.0):
        super(GetRequestOrigin, self).__init__("GetRequestOrigin", "com.apple.ace.system", None, refId)
        self.desiredAccuracy = desiredAccuracy
        self.searchTimeout = searchTimeout
        self.maxAge = maxAge
    
    def to_plist(self):
        self.add_property('desiredAccuracy')
        self.add_property('searchTimeout')
        self.add_property('maxAge')
        return super(GetRequestOrigin, self).to_plist()

class SetRequestOrigin(ServerBoundCommand):
    statusValid = "Valid"
    statusTimeout = "Timeout"
    statusUnknown = "Unknown"
    statusDenied = "Denied"
    statusDisabled = "Disabled"
    def __init__(self, plist):
        self.aceId = None
        self.refId = None
        self.timestamp = None
        self.status = None
        self.speed = None
        self.direction = None
        self.desiredAccuracy = None
        self.altitude = None
        self.age = None
        self.horizontalAccuracy = None
        self.verticalAccuracy = None
        self.longitude = None
        self.latitude = None
        super(SetRequestOrigin, self).__init__(plist)


class DomainObject(AceObject):
    def __init__(self, group, identifier=None):
        super(DomainObject, self).__init__("Object", group)
        self.identifier = identifier
    
    def to_plist(self):
        self.add_property('identifier')
        return super(DomainObject, self).to_plist()

class DomainObjectCreate(ClientBoundCommand):
    def __init__(self, refId, object=None):
        super(DomainObjectCreate, self).__init__("DomainObjectCreate", "com.apple.ace.system", None, refId)
        self.object = object
    
    def to_plist(self):
        self.add_property('object')
        return super(DomainObjectCreate, self).to_plist()



class DomainObjectRetrieve(ClientBoundCommand):
    def __init__(self, refId, identifiers=None):
        super(DomainObjectRetrieve, self).__init__("DomainObjectRetrieve", "com.apple.ace.system", None, refId)
        self.identifiers = identifiers if identifiers != None else []
    
    def to_plist(self):
        self.add_property('identifiers')
        return super(DomainObjectRetrieve, self).to_plist()



class DomainObjectCommit(ClientBoundCommand):
    def __init__(self, refId, identifier=None):
        super(DomainObjectCommit, self).__init__("DomainObjectCommit", "com.apple.ace.system", None, refId)
        self.identifier = identifier
    
    def to_plist(self):
        self.add_property('identifier')
        return super(DomainObjectCommit, self).to_plist()

class StartRequest(AceObject):
    def __init__(self, handsFree=False, utterance=""):
        super(StartRequest, self).__init__("StartRequest", "com.apple.ace.system")
        self.handsFree = handsFree
        self.utterance = utterance

    def to_plist(self):
        self.add_property('handsFree')
        self.add_property('utterance')
        return super(StartRequest, self).to_plist()

class ResultCallback(AceObject):
    def __init__(self, commands=None, code=0):
        super(ResultCallback, self).__init__("ResultCallback", "com.apple.ace.system")
        self.commands = commands if commands != None else []
        self.code = code

    def to_plist(self):
        self.add_property('commands')
        self.add_property('code')
        return super(ResultCallback, self).to_plist()


class SendCommands(AceObject):
    def __init__(self, commands=None):
        super(SendCommands, self).__init__("SendCommands", "com.apple.ace.system")
        self.commands = commands if commands != None else []
    
    def to_plist(self):
        self.add_property('commands')
        return super(SendCommands, self).to_plist()


