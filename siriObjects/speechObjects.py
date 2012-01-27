from siriObjects.baseObjects import ServerBoundCommand, ClientBoundCommand, AceObject

import uuid
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

class SpeechFailure(ClientBoundCommand):
    def __init__(self, refId, reasonDescription, reason=0):
        super(SpeechFailure, self).__init__("SpeechFailure", "com.apple.ace.speech", None, refId)
        self.reasonDescription = reasonDescription
        self.reason = reason
    
    def to_plist(self):
        self.add_property('reasonDescription')
        self.add_property('reason')
        return super(SpeechFailure, self).to_plist()


class SpeechRecognized(ClientBoundCommand):
    def __init__(self, refId, recognition, sessionId=str.upper(str(uuid.uuid4()))):
        super(SpeechRecognized, self).__init__("SpeechRecognized", "com.apple.ace.speech", None, refId)
        self.sessionId = sessionId
        self.recognition = recognition
        
    def to_plist(self):
        self.add_property('sessionId')
        self.add_property('recognition')
        return super(SpeechRecognized, self).to_plist()


class Recognition(AceObject):
    def __init__(self, phrases=None):
        super(Recognition, self).__init__("Recognition", "com.apple.ace.speech")
        self.phrases = phrases if phrases != None else []
    
    def to_plist(self):
        self.add_property('phrases')
        return super(Recognition, self).to_plist()

class Phrase(AceObject):
    def __init__(self, lowConfidence=False, interpretations=None):
        super(Phrase, self).__init__("Phrase", "com.apple.ace.speech")
        self.lowConfidence = lowConfidence
        self.interpretations = interpretations if interpretations != None else []
    
    def to_plist(self):
        self.add_property('lowConfidence')
        self.add_property('interpretations')
        return super(Phrase, self).to_plist()

class Interpretation(AceObject):
    def __init__(self, tokens=None):
        super(Interpretation, self).__init__("Interpretation", "com.apple.ace.speech")
        self.tokens = tokens if tokens != None else []
    
    def to_plist(self):
        self.add_property('tokens')
        return super(Interpretation, self).to_plist()

class Token(AceObject):    
    def __init__(self, text, startTime, endTime, confidenceScore, removeSpaceBefore, removeSpaceAfter):
        super(Token, self).__init__("Token", "com.apple.ace.speech")
        self.text = text
        self.startTime = startTime
        self.endTime = endTime
        self.confidenceScore = confidenceScore
        self.removeSpaceBefore = removeSpaceBefore
        self.removeSpaceAfter = removeSpaceAfter

    def to_plist(self):
        self.add_property('text')
        self.add_property('startTime')
        self.add_property('endTime')
        self.add_property('confidenceScore')
        self.add_property('removeSpaceBefore')
        self.add_property('removeSpaceAfter')
        return super(Token, self).to_plist()
