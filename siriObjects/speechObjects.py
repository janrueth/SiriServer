from siriObjects.baseObjects import ServerBoundCommand, ClientBoundCommand, AceObject


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
            self.getProperties()['recognition'] = recognition.getPList()
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
        if type(phrases) == list:
            if len(phrases) == len(filter(lambda x: isinstance(x, Phrases), phrases)):
                self.getProperties()['phrases'] = map(lambda x: x.getPList(), phrases)
            else:
                raise Exception('Wrong Class', 'All elements of phrases must be of type Phrases')
        else:
            raise Exception('Wrong Class', 'phrases must be a list of Phrases')

class Phrases(AceObject):
    def __init__(self):
        super(Phrases, self).__init__("Phrases", "com.apple.ace.speech")
    
    def getLowConfidence(self):
        try:
            return self.getProperties()['lowConfidence']
        except:
            return False

    def setLowConfidence(self, lowConfidence):
        if type(lowConfidence) == bool:
            self.getProperties()['lowConfidence'] = lowConfidence
        else:
            raise Exception('Wrong Type', 'lowConfidence must be of type bool')

    def getInterpretations(self):
        try:
            return self.getProperties()['interpretations']
        except:
            return []

    def setInterpretations(self, interpretations):
        if type(interpretations) == list:
            if len(interpretations) == len(filter(lambda x: isinstance(x, Interpretation), interpretations)):
                self.getProperties()['interpretations'] = map(lambda x: x.getPList(), interpretations)
            else:
                raise Exception('Wrong Class', 'All elements of interpretations must be of type Interpretation')
        else:
            raise Exception('Wrong Class', 'interpretations must be a list of Interpretations')

class Interpretation(AceObject):
    def __init__(self):
        super(Interpretation, self).__init__("Interpretation", "com.apple.ace.speech")

    def getTokens(self):
        try:
            return self.getProperties()['tokens']
        except:
            return []

    def setTokens(self, tokens):
        if type(tokens) == list:
            if len(tokens) == len(filter(lambda x: isinstance(x, Token), tokens)):
                self.getProperties()['tokens'] = map(lambda x: x.getPList(), tokens)
            else:
                raise Exception('Wrong Class', 'All elements of tokens must be of type Token')
        else:
            raise Exception('Wrong Class', 'tokens must be a list of Tokens')

class Token(AceObject):
    def __init__(self, text, startTime, endTime, confidenceScore, removeSpaceBefore, removeSpaceAfter):
        super(Token, self).__init__("Token", "com.apple.ace.speech")
        self.setText(text)
        self.setStartTime(startTime)
        self.setEndTime(endTime)
        self.setConfidenceScore(confidenceScore)
        self.setRemoveSpaceBefore(removeSpaceBefore)
        self.setRemoveSpaceAfter(removeSpaceAfter)

    def setText(self, text):
        self.getProperties()['text'] = text

    def setStartTime(self, startTime):
        self.getProperties()['startTime'] = startTime
    
    def setEndTime(self, endTime):
        self.getProperties()['endTime'] = endTime
    
    def setConfidenceScore(self, confidenceScore):
        self.getProperties()['confidenceScore'] = confidenceScore

    def setRemoveSpaceBefore(self, removeSpaceBefore):
        self.getProperties()['removeSpaceBefore'] = removeSpaceBefore

    def setRemoveSpaceAfter(self, removeSpaceAfter):
        self.getProperties()['removeSpaceAfter'] = removeSpaceAfter
