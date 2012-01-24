from baseObjects import ServerBoundCommand, ClientBoundCommand, AceObject


class StartSpeechRequest(ServerBoundCommand):
    def getCodec(self):
        try:
            return self.getProperties()['codec']
        except:
            return ""

    def getHandsFree(self):
        try:
            return self.getProperties()['handsFree']
        except:
            return False
    
    def getAudioSource(self):
        try:
            return self.getProperties()['audioSource']
        except:
            return ""

class SpeechSpacket(ServerBoundCommand):
    def getSpeechPackets(self):
        try:
            return self.getProperties()['packets']
        except:
            return []
    
    def getPacketNumber(self):
        try:
            return self.getProperties()['packetNumber']
        except:
            return -1

class FinishSpeech(ServerBoundCommand):
    def getPacketCount(self):
        try:
            return self.getProperties()['packetCount']
        except:
            return -1


class SpeechRecognized(ClientBoundCommand):
    def __init__(self, refId):
        super(SpeechRecognized, self).__init__("SpeechRecognized", "com.apple.ace.speech", None, refId)

    def getSessionId(self):
        try:
            return self.getProperties()['sessionId']
        except:
            return ""

    def setSessionId(self, sessionId):
        self.getProperties()['sessionId'] = sessionId
    
    def getRecognition(self):
        try:
            return self.getProperties()['recognition']
        except:
            return None

    def setRecognition(self, recognition):
        if isinstance(recognition, Recognition):
            self.getProperties()['recognition'] = recognition
        else:
            raise Exception('Wrong Class', 'You must supply this setter with a Recognition class')


class Recognition(AceObject):
    def __init__(self):
        super(Recognition, self).__init__("Recognition", "com.apple.ace.speech")

    def getPhrases(self):
        try:
            self.getProperties()['phrases']
        except:
            return []

    def setPhrases(self, phrases):
        if isinstance(phrases, list)
            if len(phrases) == len(filter(lambda x: isinstance(x, Phrases), phrases)):
                self.getProperties()['phrases'] = phrases
            else:
                raise Exception('Wrong Class', 'All elements of phrases must be of type Phrases')
        else:
            raise Exception('Wrong Class', 'phrases must be a list of Phrases')
