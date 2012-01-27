from siriObjects.baseObjects import ClientBoundCommand, AceObject

class GetRequestOrigin(ClientBoundCommand):
    def __init__(self, refId, desiredAccuracy="ThreeKilometers", searchTimeout=8.0):
        super(GetRequestOrigin, self).__init__("GetRequestOrigin", "com.apple.ace.system", None, refId)
        self.desiredAccuracy = desiredAccuracy
        self.searchTimeout = searchTimeout
    
    def to_plist(self):
        self.add_property('desiredAccuracy')
        self.add_property('searchTimeout')
        return super(GetRequestOrigin, self).to_plist()


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


class SendCommands(ClientBoundCommand):
    def __init__(self, refId, commands=None):
        super(SendCommands, self).__init__("SendCommands", "com.apple.ace.system", None, refId)
        self.commands = commands if commands != None else []
    
    def to_plist(self):
        self.add_property('commands')
        return super(SendCommands, self).to_plist()

