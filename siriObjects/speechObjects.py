from baseObjects import ServerBoundCommand, ClientBoundCommand


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