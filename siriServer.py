import socket, ssl, sys, zlib, binascii, time, select, struct, biplist
from email.utils import formatdate
import uuid
import reencode
import flac
import json
import asyncore

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

    def send_plist(self, plist):
        bplist = biplist.writePlistToString(plist);
        #
        self.unzipped_output_buffer = struct.pack('!BBBH', 2,0,0,len(bplist)) + bplist
        self.flush_unzipped_output() 
    
    def send_pong(self, id):
        self.unzipped_output_buffer = struct.pack('!BBBH', 4,0,0, id)
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
                    print "Got asked for certificate, should return GetSessionCertificateResponse, but how?"
                    #"APPEL SENDS 2 CERTS HERE, starting with a six byte header (first byte = 1, second byte = number of certificated following, network ordered int32 with length of first certificate DER formatted, then after this certificate again int32 in networkorder length of next certificate"
                    {"group":"com.apple.ace.system", "aceId": str(uuid.uuid4()), "refId": object['aceId'], "class": "GetSessionCertificateResponse", "properties":{"certificate": "\x01\x00\x00\x00\x00\x00"}}
                    pass
                
                if object['class'] == 'CreateSessionInfoRequest':
		    # how does a positive answer look like?
                    print "returning response"
                    #self.send_plist({"class":"CommandFailed",
                    #                "properties":
                    #            {"reason":"Not authenticated", "errorCode":0, "callbacks":[]},
                    #            "aceId": str(uuid.uuid4()),
                    #            "refId": object['refId'],
                    #            "group":"com.apple.ace.system"})
                    self.send_plist({"class": "CreateSessionInfoResponse", "properties": {"sessionInfo": "THIS IS YOUR TOKEN FUCKHEAD", "validityDuration": 90000}, "aceId":str(uuid.uuid4()), "refId":object['aceId'], "group":"com.apple.ace.system"})
                    
                if object['class'] == 'CreateAssistant':
                    self.send_plist({"class": "AssistantCreated", "properties": {"speechId": str(uuid.uuid4()), "assistantId": str(uuid.uuid4())}, "group":"com.apple.ace.system", "callbacks":[], "aceId": str(uuid.uuid4()), "refId": object['aceId']})
                    #self.send_plist({"class": "GetSessionCertificateResponse", "properties": {"sessionInfo": "\x02\xDA=\x99\xC2\x0E\xE2\x10__\x038\xE8>C\xA5\xD5\x00\x00\x00@\xA6\xC4\x879\x84s\e\xCC\b\xEB\xC7\a>\xA6\x8AxZ\xF6\x1ELr\x1F3\x81\x8E$;9\xF6+`A<\akW\x86\xD9\x1Es\x16%\xD3aK_\xC1\xCElrM\xAA\x80\xD6\xA3V)\xF1\x80\xAF\xFF\xAA\x86\xD2\x01\xC1\xDA\xD9F~9I\x82[\xD2\xA4\xF2\xE9o'\x91\x05\xE0|\b\x00\x00\x006\x01\x02\fnb\xA2\x966\x94*@\xE8\x86\x98vu\xD4mO", "validityDuration": 90000}, "group": "com.apple.ace.system", "refId": object['aceId'], "ace_id": str(uuid.uuid4())})
                
                if object['class'] == 'SetAssistantData':
                    # grab assistant data, how is a device identified?
                    pass
                
		#probably Create Set and Load assistant work together, first we create one response with success, fill it with set..data and later can load it again using load... however.. what are valid responses to all three requests?
                if object['class'] == 'LoadAssistant':
                # reply with a AssistentLoaded
                   self.send_plist({"class": "AssistantLoaded", "properties": {"version": "20111216-32234-branches/telluride?cnxn=293552c2-8e11-4920-9131-5f5651ce244e", "requestSync":False, "dataAnchor":"removed"}, "aceId":str(uuid.uuid4()), "refId":object['aceId'], "group":"com.apple.ace.system"})
            
                if object['class'] == 'StartSpeechRequest':
                    self.speech[object['aceId']] = []
                        
                if object['class'] == 'StartSpeechDictation':
                    self.speech[object['aceId']] = []
                    
                if object['class'] == 'SpeechPacket':
                    self.speech[object['refId']] += object['properties']['packets']
                
                if object['class'] == 'CancelRequest':
                    del self.speech[object['refId']]
                
                if object['class'] == 'FinishSpeech':
		    #this should be done async
                    pcm = reencode.decodeToPCM(self.speech[object['refId']], 16000, 8)
                    del self.speech[object['refId']]
                    enc = flac.Encoder()
                    numSamples = int(len(pcm)/2)
                    enc.initialize(16000, 1, 16, numSamples)
                    enc.encode(pcm)
                    enc.finish()
                    flacBin = enc.getBinary()
                    enc.destroy()
                    
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
                                #self.send_plist({"class": "SpeechRecognized", "properties": {"recognition": {"properties": {"phrases": }}}})
                    
                #                if object['class'] == 'ClearContext':
                    #   getSessionCertificateResponse = dict([("group", "com.apple.ace.system"), ("ref_id", str(uuid.uuid4())), ("ace_id", str(uuid.uuid4())), ("class", "GetSessionCertificateResponse"), ("properties", dict([("certificate", "\x01\x02\x00\x00\x04\x160\x82\x04\x120\x82\x02\xFA\xA0\x03\x02\x01\x02\x02\x01\x1C0\r\x06\t*\x86H\x86\xF7\r\x01\x01\x05\x05\x000b1\v0\t\x06\x03U\x04\x06\x13\x02US1\x130\x11\x06\x03U\x04\n\x13\nApple Inc.1&0$\x06\x03U\x04\v\x13\x1DApple Certification Authority1\x160\x14\x06\x03U\x04\x03\x13\rApple Root CA0\x1E\x17\r110126190134Z\x17\r190126190134Z0\x81\x851\v0\t\x06\x03U\x04\x06\x13\x02US1\x130\x11\x06\x03U\x04\n\f\nApple Inc.1&0$\x06\x03U\x04\v\f\x1DApple Certification Authority1907\x06\x03U\x04\x03\f0Apple System Integration Certification Authority0\x82\x01\"0\r\x06\t*\x86H\x86\xF7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0F\x000\x82\x01\n\x02\x82\x01\x01\x00\xDA\xE0\x0F\x98\x97\xCBX)\x86*\v\xB8\x9E\x19Z1\xC3-\x0Ej,R\x01\xEE\x1D\x03\xFB\x82Ai\xCDP&6z\xB7\fo\x0E9\x03\xB8\xD4\x18V\xA3\b\xB2<\xC3\xFB6A\xE4\xD7\xC8g`2\vN2}\x87\xF7\xFD\xCDS\xB0\x1A\xBA\xFC\x1Fl\xC9E\a\xAD\x828\xF3\xA8|\xC4N\xC2\xB1V\xD9>\xB2mm\x04A\x1A\xC1\x9AG\xC0\xAC\x15|-x\x91\xAB\a\xA2e\xB1z\x83\xDD\x98Kw@\xD8\xEEP\xEB\xC7kX\b\x06\x97WU}'\xF8\n\xE6\xB5\x15\xE7\xA7\x93\xF9\xF1\x80\xE6By?\x16\xD32\x9D\x11vA)\n1\t\xEF\x0F[\xF8\xF3\xA7\xA9\xF7R\r\xBB\xF8-t\xAC\xA6I\x1F\x1F\xCE{\x05\xA7\x85=\xBE\xCF\xA2\xA7\xAA#\x85f\xFE\xC5\x16\x12~[\xE21w\x91\x02\t\xDF~~\xE4\x8A\xE0\xECA\xAC\x17,\x04\xE0\xBCy\xA4\x89xD\x06\x8B;K\xA0\xBC\x84\xE2\xB0\x82\xB52\xBE\x04\x1C\x03\xED\x82>u7\x14\xCFu\x9F\x821m\xCF\t\x14\x86\xD1'\x02\x03\x01\x00\x01\xA3\x81\xAE0\x81\xAB0\x0E\x06\x03U\x1D\x0F\x01\x01\xFF\x04\x04\x03\x02\x01\x860\x0F\x06\x03U\x1D\x13\x01\x01\xFF\x04\x050\x03\x01\x01\xFF0\x1D\x06\x03U\x1D\x0E\x04\x16\x04\x14\xF00sc\xF2\xEF\x1D\xAC\xCC\xE6\t2\xC1\xFAyz\xB1iPh0\x1F\x06\x03U\x1D#\x04\x180\x16\x80\x14+\xD0iG\x94v\t\xFE\xF4k\x8D.@\xA6\xF7GM\x7F\b^06\x06\x03U\x1D\x1F\x04/0-0+\xA0)\xA0'\x86%http://www.apple.com/appleca/root.crl0\x10\x06\n*\x86H\x86\xF7cd\x06\x02\x04\x04\x02\x05\x000\r\x06\t*\x86H\x86\xF7\r\x01\x01\x05\x05\x00\x03\x82\x01\x01\x00={\x8F\xAD\x1F\f\"\x8A\x9BK\xA3\xCF\xF8+\xB0\x1Fh\xE1\f\xF7\x9C$\x83\x16\x03-\xD3\xB2\xA8\xD0C\xE8\xAF<\x97&\xC8\xAD\xD5,\xC4LUS\x01I\xD0\xE2\xB4\xFB\xE6\xDBr\xD1\x98\xBB\xFC\x9B\xC8N\xB7\x8F\xCCe\x86\x7FD\xB9\xDA'*N\xDF\xCB\xDF\xD3}\xDFAq\xF8\xB3\xC0\x1D\xA2\n3\xB9\xEC+\xC5sr\xFB\xE1\xCA]\x8E/4\xF4k\xC4O\x0F\xC8\x8A\xAC\x0F\xFBo%n\xB7\xAE\x8E\xC7\xE4\x02\xB8 N]VLI\x97\xB1$t~\xC9\x93\x934\x8C\x99\xD1\xA7\xC0\x1C\xD3\xD4\xC2\xAEi\xEB\x9F\x9FW\xE2h\xC7\xCA\xD5\xC5\"\x82dAX\xFEx\xD1\xCA\xC1\xF96jkD\xF7\xB3\x86rzd@\x171\x9D\xBC\xACu\xF0\xFA3Q\xE5\xBD\x01jX?\xF0\x00\xAE\x99\\\n\xC2\xC9\xE9^\x1C\x87\x02\xEC\xA0\bUA*\x9B\x8Cd\x85\x8EP\x03\xCD\xE0\x11\xAF\xCEr\x19\xEBR\xF3\xAF\x92\xAD\x93.\x94\x9D\xD6\xAF\xFF\xC0&\xF1\xDE\x94\x92\x1C\xD9\xBC=6\xCCU\xFA8\xDB\x00\x00\x0510\x82\x05-0\x82\x04\x15\xA0\x03\x02\x01\x02\x02\bK,\x91H\x1D\x9B}\xA00\r\x06\t*\x86H\x86\xF7\r\x01\x01\x05\x05\x000\x81\x851\v0\t\x06\x03U\x04\x06\x13\x02US1\x130\x11\x06\x03U\x04\n\f\nApple Inc.1&0$\x06\x03U\x04\v\f\x1DApple Certification Authority1907\x06\x03U\x04\x03\f0Apple System Integration Certification Authority0\x1E\x17\r110325011332Z\x17\r140324011332Z0i1\x1D0\e\x06\x03U\x04\x03\f\x14DRM Technologies A011&0$\x06\x03U\x04\v\f\x1DApple Certification Authority1\x130\x11\x06\x03U\x04\n\f\nApple Inc.1\v0\t\x06\x03U\x04\x06\x13\x02US0\x82\x01\"0\r\x06\t*\x86H\x86\xF7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0F\x000\x82\x01\n\x02\x82\x01\x01\x00\xB4\x06m~es\x97\xE1\xBFI\xB1\xFA\x9A\".\xA7\xD3q\x81 kIA\x15\xC2\xDB`z\xC6\xA2\xB7Mz/\x8E\xC1c\a\x1C\x04\xCC\x93\xD8\xE0\r\xC8\xB8\xF2[\xCEm\xFAB\xCB\x10@\xC2$\n\xA7\xE4\x1D&\x82\x8A>0\x86]\xED\x178\xEE\x87\xAB\xBD\xE8HJIw\x85.\xB7\x91\x84\x9B)}A\x05\xA0y\xF5\xAD\x8C\xC1\v\xD8\x9Di\xE7\x9C\xB2\xA9F\xD0K\xFE\t\x18P$\x8AYG+\"UG\xEDQ\"\x9DB\xE9\x9D\xEE\x81\xC3G\xCD\xE4o\n*?O+\xD2\x04\xD0\xB8\x8C\xE8d\x98\xDF\xCE`S\x9B\x88\x1A\xCF\xD4\xC2\rte\xBF\xF3\x85\x87_K\x87\x10\xA2\x87\x8Am>@U\x0E\xF9\x9F\x99\xCC2\x93\x83Q\x88\xC9\xB9\xF8^\xC9\x19_\x17\xE7k\x9B|:\xDD\xFFh\xDF\xD4\xD14Ut\xEC\xF7K\xE8\x1C\x90u\x85\xF2\xFCC\xFF\xA5D#R?\xFB\xF5!\xE3\x83\x16?\xBE\nt\xF9<t\x99j\xFE?\xD2Z\xA1P\xE3.\x8BH\r\"&;\xD5\x9EI\x02\x03\x01\x00\x01\xA3\x82\x01\xBA0\x82\x01\xB60\x1D\x06\x03U\x1D\x0E\x04\x16\x04\x14\xD2$#\xFB\xEB\xE8\x8E\x8Fq\x9C\x84\xEEbs=\xE9^$\t/0\f\x06\x03U\x1D\x13\x01\x01\xFF\x04\x020\x000\x1F\x06\x03U\x1D#\x04\x180\x16\x80\x14\xF00sc\xF2\xEF\x1D\xAC\xCC\xE6\t2\xC1\xFAyz\xB1iPh0\x82\x01\x0E\x06\x03U\x1D \x04\x82\x01\x050\x82\x01\x010\x81\xFE\x06\t*\x86H\x86\xF7cd\x05\x010\x81\xF00(\x06\b+\x06\x01\x05\x05\a\x02\x01\x16\x1Chttp://www.apple.com/appleca0\x81\xC3\x06\b+\x06\x01\x05\x05\a\x02\x020\x81\xB6\f\x81\xB3Reliance on this certificate by any party assumes acceptance of the then applicable standard terms and conditions of use, certificate policy and certification practice statements.0/\x06\x03U\x1D\x1F\x04(0&0$\xA0\"\xA0 \x86\x1Ehttp://crl.apple.com/asica.crl0\x0E\x06\x03U\x1D\x0F\x01\x01\xFF\x04\x04\x03\x02\x05\xA00\x13\x06\n*\x86H\x86\xF7cd\x06\f\x01\x01\x01\xFF\x04\x02\x05\x000\r\x06\t*\x86H\x86\xF7\r\x01\x01\x05\x05\x00\x03\x82\x01\x01\x00}y\xA7cnA;\xBE\xC1\xCE\xB1\x8C\xFAm0 \xB8\xBAI0\x92=\x1DU\xCE\xB9\xC2-Kb\xC5\xCA@\xF6\xB7\xBC\xB1\xF6\xD2\xA6\xFA\xAD\x01kO\x1C\xCC\xAE\xCEF \xFF\xC2\xB3\xC0,wO\xD0\x13DL\x87\xC7a-\x0F\xC7\xCCC.7:7\xFD\xAE\x98\x9A\x12\xB6I\xB0\xAAw\xD3S\x81\x96\x80\xCD\x84\xDBs\xAAG\xA8 V6\xC2\xD9\xA5\xE9\f<\"\x1Dy\xEF\xE7\xB0O\t}^\xFB\xB2\"\xA3\xB6\xF7#%\t\x83y\xA84V\x84\xE6E\xAD\"\xA1\x1CU\x9C\xA2/\x1F\xB6!\xB9\xFF\xD8\x0F\xC9s\tv\xF0\x03\x17\x19\x8F\xE9\xA3\xFC\xE6B\xCB_d\x86\x96\x8Ch?\xC2\xA0XB\xD4\x9Fvm\x95\xBF\xC0\xF7\xDB\x14t\xFCZ\xA8\x82\xC7\xA6\xFCV\x8A7\xB7\xC8r\x9C\xBC\x9BD\xD1F\xE2\x8D$\xD9\x7F'y\xF1t\xB9\xC5\xB2\xB0\xC2\xE1&\x06\xE4\xFF\xAF\xA5\v\xD9\xA3\x1E\x95\xDBD\x91\xCC\xE9K\x022\x03\xE6R\xF6\xA7*Z#4\xD0\x1D\x17\xF2\xEB\xEA\xC2y\n\xE9")]))])
                    #     self.unzipped_output_buffer += biplist.writePlistToString(getSessionCertificateResponse)


    def hasNextObj(self):
        if len(self.unzipped_input) == 0:
            return False
        cmd, inter1, inter2, data = struct.unpack('!BBBH', self.unzipped_input[:5])
        if cmd in (3,4): #ping pong
            return True
        if cmd == 2:
            #print "expect: ", data+5,  " received: ", len(self.unzipped_input)
            return ((data + 5) < len(self.unzipped_input))
    
    def read_next_object_from_unzipped(self):
        cmd, inter1, inter2, data = struct.unpack('!BBBH', self.unzipped_input[:5])
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
