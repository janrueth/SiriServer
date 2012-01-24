from uuid import uuid4

import speechObjects

class AceObject:
    def __init__(self, encodedClassName, groupIdentifier):
        self.plist = dict()
        self.plist['class'] = encodedClassName
        self.plist['group'] = groupIdentifier
    
    def getPList(self):
        return self.plist

    def getClass(self):
        return self.plist['class']
    
    def getGroup(self):
        return self.plist['group']

class ServerBoundCommand(AceObject):
    def __init__(self, plist):
        super(ServerBoundCommand, self).__init__(None, None)
        self.plist = plist
        
    def getAceId(self):
        return self.plist['aceId']
    
    def getProperties(self):
        try:
            return self.plist['properties']
        except:
            return dict()

class ClientBoundCommand(AceObject):
    def __init__(self, encodedClassName, groupIdentifier, aceId, refId)
        super(ServerBoundCommand, self).__init__(encodedClassName, groupIdentifier)
        self.plist['aceId'] = aceId if aceId != None else str(uuid4())
        self.plist['refId'] = refId if refId != None else str(uuid4())

    def getAceId(self):
        return self.plist['aceId']
    
    def getRefId(self):
        return self.plist['refId']



classToPyClassMapping = {
    'StartSpeechRequest' = speechObjects.StartSpeechRequest
    'SpeechSpacket' = speechObjects.SpeechSpacket
    'FinishSpeech' = speechObjects.FinishSpeech
}


def ServerBoundPlistToObject(plist):
    clazz = plist['class']
    try:
        obj = classToPyClassMapping[clazz]
        return obj(plist)
    except:
        raise Exception('ClassNotFound', 'The class you were looking for is not implemented')
    