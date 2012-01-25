from uuid import uuid4

import siriObjects.speechObjects

class AceObject(object):
    def __init__(self, encodedClassName, groupIdentifier):
        self.className = encodedClassName
        self.groupId = groupIdentifier
        self.plist = dict()
        self.properties = dict()
    
    def add_item(self, name):
        self.plist[name] = getattr(self, name)

    def add_property(self, name):
        self.properties[name] = getattr(self, name)

    @staticmethod
    def list_to_plist(newList):
        def parseList(x):
            if type(x) == list:
                new = AceObject.list_to_plist(x)
            elif type(x) == dict:
                new = AceObject.dict_to_plist(x)
            else:
                try:
                    new = x.to_plist()
                except:
                    new = x
            return new

        return map(parseList, newList)

    @staticmethod
    def dict_to_plist(newDict):
        def parseDict((k,v)):
            if type(v) == list:
                new = AceObject.list_to_plist(v)
            elif type(v) == dict:
                new = AceObject.dict_to_plist(v)
            else:
                try:
                    new = v.to_plist()
                except:
                    new = v
            return (k,new)
                
        return dict(map(parseDict, newDict.items()))

    def to_plist(self):
        self.plist['group'] = self.groupId
        self.plist['class'] = self.className
        self.plist['properties'] = self.properties

        for key in self.plist.keys():
            if type(self.plist[key]) == list:
                self.plist[key] = AceObject.list_to_plist(self.plist[key])
            elif type(self.plist[key]) == dict:
                self.plist[key] = AceObject.dict_to_plist(self.plist[key])
            else:
                try:
                    self.plist[key] = self.plist[key].to_plist() 
                except:
                    pass
        return self.plist

class ServerBoundCommand(AceObject):
    def __init__(self, plist):
        super(ServerBoundCommand, self).__init__(None, None)
        self.plist = plist
        
    def getAceId(self):
        return self.plist['aceId']


class ClientBoundCommand(AceObject):
    def __init__(self, encodedClassName, groupIdentifier, aceId, refId):
        super(ClientBoundCommand, self).__init__(encodedClassName, groupIdentifier)
        self.aceId= aceId if aceId != None else str.upper(str(uuid4()))
        self.refId = refId if refId != None else str.upper(str(uuid4()))

    def to_plist(self):
        self.add_item('aceId')
        self.add_item('refId')
        return super(ClientBoundCommand, self).to_plist()


class RequestCompleted(ClientBoundCommand):
    def __init__(self, refId, callbacks = []):
        super(RequestCompleted, self).__init__("RequestCompleted", "com.apple.ace.system", None, refId)
        self.callbacks = callbacks
    
    def to_plist(self):
        self.add_property('callbacks')
        return super(RequestCompleted, self).to_plist()

#classToPyClassMapping = {'StartSpeechRequest': speechObjects.StartSpeechRequest,
#    'SpeechSpacket': speechObjects.SpeechSpacket,
#    'FinishSpeech': speechObjects.FinishSpeech
#}


#def ServerBoundPlistToObject(plist):
#    clazz = plist['class']
#    try:
#        obj = classToPyClassMapping[clazz]
#        return obj(plist)
#    except:
#        raise Exception('ClassNotFound', 'The class you were looking for is not implemented')
    