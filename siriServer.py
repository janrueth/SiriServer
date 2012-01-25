import socket, ssl, sys, zlib, binascii, time, select, struct, biplist
from email.utils import formatdate
import uuid
import speex
import flac
import json
import asyncore
from M2Crypto import BIO, RSA, X509

from siriObjects import speechObjects, baseObjects, uiObjects

caCertFile = open('OrigAppleSubCACert.der')
caCert = X509.load_cert_bio(BIO.MemoryBuffer(caCertFile.read()), format=0)
caCertFile.close()
certFile = open('OrigAppleServerCert.der')
serverCert = X509.load_cert_bio(BIO.MemoryBuffer(certFile.read()), format=0)
certFile.close()



class HandleConnection(asyncore.dispatcher_with_send):
    def __init__(self, conn):
        asyncore.dispatcher_with_send.__init__(self, conn)
        self.socket = ssl.wrap_socket(conn,
                                      server_side=True,
                                      certfile="server.passless.crt",
                                      keyfile="server.passless.key",
                                      ssl_version=ssl.PROTOCOL_TLSv1,
                                      do_handshake_on_connect=False,
                                      cert_reqs=ssl.CERT_NONE)
        while True:
            try:
                self.socket.do_handshake()
                break
            except ssl.SSLError, err:
                if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                    select.select([self.socket], [], [])
                elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                    select.select([], [self.socket], [])
                else:
                    raise        
        self.consumed_ace = False
        self.data = ""
        self.binary_mode = False
        self.decompressor = zlib.decompressobj()
        self.compressor = zlib.compressobj()
        self.unzipped_input = ""
        self.unzipped_output_buffer = ""
        self.output_buffer = ""
        self.speech = dict()
        self.pong = 1
        self.ping = 0
            
    def readable(self):
        if isinstance(self.socket, ssl.SSLSocket):
            while self.socket.pending() > 0:
                self.handle_read_event()
            return True

    def handle_read(self):
        self.data += self.recv(8192)
        if not self.binary_mode:
            if "\r\n\r\n" in self.data:
                endOfHeader = self.data.find("\r\n\r\n")+4
                self.header = self.data[:endOfHeader]
                self.data = self.data[endOfHeader:]
                print "Received new header from iDevice"
                print self.header
                print "Header end"
                self.binary_mode = True
                self.header_complete = True
        else:
            if not self.consumed_ace:
                print "Received removing ace instruction: ", repr(self.data[:4])
                self.data = self.data[4:]
                self.consumed_ace = True
                self.output_buffer = "HTTP/1.1 200 OK\r\nServer: Apache-Coyote/1.1\r\nDate: " +  formatdate(timeval=None, localtime=False, usegmt=True) + "\r\nConnection: close\r\n\r\n\xaa\xcc\xee\x02"
                #self.flush_output_buffer()
            
            self.process_compressed_data()

    def send_object(self, obj):
        self.send_plist(obj.to_plist())

    def send_plist(self, plist):
        print "Sending: ", plist
        bplist = biplist.writePlistToString(plist);
        #
        self.unzipped_output_buffer = struct.pack('>BI', 2,len(bplist)) + bplist
        self.flush_unzipped_output() 
    
    def send_pong(self, id):
        self.unzipped_output_buffer = struct.pack('>BI', 4, id)
        self.flush_unzipped_output() 

    def parseGoogleResponse(self, response):
        header_end = response.find('\r\n\r\n')
        if header_end < 0:
            return None
        header_end += 4
        #        print "Google header: ", response[:header_end]
        json_string = response[header_end:len(response)-1];
        return json.loads(json_string)

    def process_compressed_data(self):
        self.unzipped_input += self.decompressor.decompress(self.data)
        self.data = ""
        while self.hasNextObj():
            object = self.read_next_object_from_unzipped()
            if object != None:
                print "Packet with class: ", object['class']
                print "packet with content: ", object
                
                
                if object['class'] == 'GetSessionCertificate':
                    caDer = caCert.as_der()
                    serverDer = serverCert.as_der()
                    self.send_plist({"class": "GetSessionCertificateResponse", "group": "com.apple.ace.system", "aceId": str(uuid.uuid4()), "refId": object['aceId'], "properties":{"certificate": biplist.Data("\x01\x02"+struct.pack(">I", len(caDer))+caDer + struct.pack(">I", len(serverDer))+serverDer)}})

                    #self.send_plist({"class":"CommandFailed", "properties": {"reason":"Not authenticated", "errorCode":0, "callbacks":[]}, "aceId": str(uuid.uuid4()), "refId": object['aceId'], "group":"com.apple.ace.system"})
                if object['class'] == 'CreateSessionInfoRequest':
		    # how does a positive answer look like?
                    print "returning response"
                    self.send_plist({"class":"CommandFailed", "properties": {"reason":"Not authenticated", "errorCode":0, "callbacks":[]}, "aceId": str(uuid.uuid4()), "refId": object['aceId'], "group":"com.apple.ace.system"})
                    #self.send_plist({"class":"SessionValidationFailed", "properties":{"errorCode":"UnsupportedHardwareVersion"}, "aceId": str(uuid.uuid4()), "refId":object['aceId'], "group":"com.apple.ace.system"})
                    
                if object['class'] == 'CreateAssistant':
                    self.send_plist({"class": "AssistantCreated", "properties": {"speechId": str(uuid.uuid4()), "assistantId": str(uuid.uuid4())}, "group":"com.apple.ace.system", "callbacks":[], "aceId": str(uuid.uuid4()), "refId": object['aceId']})
            
                if object['class'] == 'SetAssistantData':
                    # grab assistant data, how is a device identified?
                    pass
                
		#probably Create Set and Load assistant work together, first we create one response with success, fill it with set..data and later can load it again using load... however.. what are valid responses to all three requests?
                if object['class'] == 'LoadAssistant':
                # reply with a AssistentLoaded
                #  self.send_plist({"class": "AssistantNotFound", "aceId":str(uuid.uuid4()), "refId":object['aceId'], "group":"com.apple.ace.system"})
                    self.send_plist({"class": "AssistantLoaded", "properties": {"version": "20111216-32234-branches/telluride?cnxn=293552c2-8e11-4920-9131-5f5651ce244e", "requestSync":False, "dataAnchor":"removed"}, "aceId":str(uuid.uuid4()), "refId":object['aceId'], "group":"com.apple.ace.system"})
                    pass
                if object['class'] == 'DestroyAssistant':
                    self.send_plist({"class": "AssistantDestroyed", "properties": {"assistantId": object['properties']['assistantId']}, "aceId":str(uuid.uuid4()), "refId":object['aceId'], "group":"com.apple.ace.system"})

                if object['class'] == 'StartSpeechRequest' or object['class'] == 'StartSpeechDictation':
                    decoder = speex.Decoder()
                    decoder.initialize(mode=speex.SPEEX_MODEID_WB)
                    encoder = flac.Encoder()
                    encoder.initialize(16000, 1, 16) #16kHz sample rate, 1 channel, 16 bits per sample
                    self.speech[object['aceId']] = (decoder, encoder)
                    
                if object['class'] == 'SpeechPacket':
                    (decoder, encoder) = self.speech[object['refId']]
                    pcm = decoder.decode(object['properties']['packets'])
                    encoder.encode(pcm)
                
                if object['class'] == 'CancelRequest':
                    # we should test if this stil exists..
                    del self.speech[object['refId']]
                
                if object['class'] == 'FinishSpeech':
                    (decoder, encoder) = self.speech[object['refId']]
                    decoder.destroy()
                    encoder.finish()
                    flacBin = encoder.getBinary()
                    encoder.destroy()
                    del self.speech[object['refId']]
                    #this should be done async
                    
                    http_request = "POST /speech-api/v1/recognize?xjerr=1&client=chromium&pfilter=2&lang=de-DE&maxresults=6 HTTP/1.0\r\nHost: www.google.com\r\nContent-Type: audio/x-flac; rate=16000\r\nContent-Length: %d\r\n\r\n" % len(flacBin)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(("www.google.com", 80))
                    s.send(http_request)
                    s.send(flacBin)
                    response = s.recv(1024)
                    s.close()
                    answer = self.parseGoogleResponse(response)
                    if answer != None:
                        possible_matches = answer['hypotheses']
                        if len(possible_matches) > 0:
                            best_match = possible_matches[0]['utterance']
                            best_match_confidence = possible_matches[0]['confidence']
                            print u"Best matching result: \"{0}\" with a confidence of {1}%".format(best_match, round(float(best_match_confidence)*100,2))
                            
                            # construct a SpeechRecognized
                            token = speechObjects.Token(best_match, 0, 0, 1000.0, True, True)
                            interpretation = speechObjects.Interpretation([token])
                            phrase = speechObjects.Phrase(lowConfidence=False, interpretations=[interpretation])
                            recognition = speechObjects.Recognition([phrase])
                            recognized = speechObjects.SpeechRecognized(object['refId'], recognition)
                            
                            # Send speechRecognized to iDevice
                            self.send_object(recognized)
                            
                            # Just for now echo the detected text
                            view = uiObjects.AddViews(object['refId'])
                            view.views += [uiObjects.AssistantUtteranceView(text=best_match, speakableText=best_match)]
                            self.send_object(view)
                            
                            # at the end we need to finish the request
                            self.send_object(baseObjects.RequestCompleted(object['refId']))
                    
    def hasNextObj(self):
        if len(self.unzipped_input) == 0:
            return False
        cmd, inter1, inter2, data = struct.unpack('>BBBH', self.unzipped_input[:5])
        if cmd in (3,4): #ping pong
            return True
        if cmd == 2:
            #print "expect: ", data+5,  " received: ", len(self.unzipped_input)
            return ((data + 5) < len(self.unzipped_input))
    
    def read_next_object_from_unzipped(self):
        cmd, inter1, inter2, data = struct.unpack('>BBBH', self.unzipped_input[:5])
        print cmd, inter1, inter2, data
        
        if cmd == 3: #ping
            self.ping = data
            self.send_pong(self.pong)
            self.pong += 1
            print "Returning a Pong"
            self.unzipped_input = self.unzipped_input[5:]
            return None

        object_size = data
        prefix = self.unzipped_input[:5]
        object_data = self.unzipped_input[5:object_size+5]
        self.unzipped_input = self.unzipped_input[object_size+5:]
        return self.parse_object(object_data)
    
    def parse_object(self, object_data):
        #this is a binary plist file
        plist = biplist.readPlistFromString(object_data)
        return plist

    def flush_unzipped_output(self):
            
        self.output_buffer += self.compressor.compress(self.unzipped_output_buffer)
        #make sure everything is compressed
        self.output_buffer += self.compressor.flush(zlib.Z_SYNC_FLUSH)
        self.unzipped_output_buffer = ""

        self.flush_output_buffer()

    def flush_output_buffer(self):
        if len(self.output_buffer) > 0:
            self.send(self.output_buffer)
            self.output_buffer = ""

class SiriServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = HandleConnection(sock)

	
print "Opening Server on port 443"
server = SiriServer('', 443)
asyncore.loop()
