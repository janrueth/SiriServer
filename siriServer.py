#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import biplist
except ImportError:
    print "You need to install biplist package on your system! e.g. \"sudo easy_install biplist\""
    exit(-1)

try:
    from M2Crypto import BIO, RSA, X509
except ImportError:
    print "You must install M2Crypto on your system! (this might require openssl and SWIG) e.g. \"sudo easy_install m2crypto\""
    exit(-1)

import sys
if sys.version_info < (2, 6):
    print "You must use python 2.6 or greater"
    exit(-1)

import socket, ssl, zlib, binascii, time, select, struct, uuid, json, asyncore, re, threading, logging, pprint, sqlite3
from optparse import OptionParser
from email.utils import formatdate

import speex
import flac
import db
from db import Assistant

import PluginManager

from siriObjects import speechObjects, baseObjects, uiObjects, systemObjects
from siriObjects.baseObjects import ObjectIsCommand
from siriObjects.speechObjects import StartSpeech, StartSpeechRequest, StartSpeechDictation, SpeechPacket, SpeechFailure, FinishSpeech
from siriObjects.systemObjects import CancelRequest, CancelSucceeded, GetSessionCertificate, GetSessionCertificateResponse, CreateSessionInfoRequest, CommandFailed
from httpClient import AsyncOpenHttp

from sslDispatcher import ssl_dispatcher

import signal, os

class HandleConnection(ssl_dispatcher):
    __not_recognized = {"de-DE": u"Entschuldigung, ich verstehe \"{0}\" nicht.", "en-US": u"Sorry I don't understand {0}"}
    __websearch = {"de-DE": u"Websuche", "en-US": u"Websearch"}
    def __init__(self, conn):
        asyncore.dispatcher_with_send.__init__(self, conn)
        
        self.ssled = False
        self.secure_connection(certfile="server.passless.crt", keyfile="server.passless.key", server_side=True)               

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
        self.httpClient = AsyncOpenHttp(self.handle_google_data, self.handle_google_failure)
        self.gotGoogleAnswer = False
        self.googleData = None
        self.lastRequestId = None
        self.dictation = None
        self.dbConnection = db.getConnection()
        self.assistant = None
        self.sendLock = threading.Lock()
        self.current_running_plugin = None
        self.current_location = None
        self.plugin_lastAceId = None
        self.logger = logging.getLogger("logger")
    
    def handle_ssl_established(self):                
        self.ssled = True

    def handle_ssl_shutdown(self):
        self.ssled = False
            
    def readable(self):
        if self.ssled:
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
                self.logger.debug("--------------------------------------Header start------------------------------------")
                self.logger.debug(self.header)
                self.logger.debug("---------------------------------------Header end-------------------------------------")
                self.binary_mode = True
                self.header_complete = True
        else:
            if not self.consumed_ace:
                self.logger.debug("Received removing ace instruction: {0}".format(repr(self.data[:4])))
                self.data = self.data[4:]
                self.consumed_ace = True
                self.output_buffer = "HTTP/1.1 200 OK\r\nServer: Apache-Coyote/1.1\r\nDate: " +  formatdate(timeval=None, localtime=False, usegmt=True) + "\r\nConnection: close\r\n\r\n\xaa\xcc\xee\x02"
                #self.flush_output_buffer()
            
            # first process outstanding google answers THIS happens at least on each PING
            if self.gotGoogleAnswer:
                self.process_recognized_speech(self.googleData, self.lastRequestId, self.dictation)
                self.lastRequestId = None
                self.dictation = None
                self.googleData = None
                self.gotGoogleAnswer = False
            
            self.process_compressed_data()

    def handle_google_data(self, body, requestId, dictation):
        self.googleData = json.loads(body)
        self.lastRequestId = requestId
        self.dictation = dictation
        self.gotGoogleAnswer = True

    def handle_google_failure(self, requestId, dictation):
        self.googleData = None
        self.lastRequestId = requestId
        self.dictation = dictation
        self.gotGoogleAnswer = True

    def send_object(self, obj):
        self.send_plist(obj.to_plist())

    def send_plist(self, plist):
        self.sendLock.acquire()
        self.logger.debug("Sending:\n{0}".format(pprint.pformat(plist, width=40)))
        bplist = biplist.writePlistToString(plist);
        #
        self.unzipped_output_buffer = struct.pack('>BI', 2,len(bplist)) + bplist
        self.flush_unzipped_output() 
        self.sendLock.release()
    
    def send_pong(self, id):
        self.sendLock.acquire()
        self.unzipped_output_buffer = struct.pack('>BI', 4, id)
        self.flush_unzipped_output() 
        self.sendLock.release()

    def process_recognized_speech(self, googleJson, requestId, dictation):
        if googleJson == None:
            # there was a network failure
            # is this the correct command to send?
            self.send_object(speechObjects.SpeechFailure(requestId, "No connection to Google possible"))
            self.send_object(baseObjects.RequestCompleted(requestId))
        else:
            possible_matches = googleJson['hypotheses']
            if len(possible_matches) > 0:
                best_match = possible_matches[0]['utterance']
                best_match = best_match[0].upper()+best_match[1:]
                best_match_confidence = possible_matches[0]['confidence']
                self.logger.info(u"Best matching result: \"{0}\" with a confidence of {1}%".format(best_match, round(float(best_match_confidence)*100,2)))
                # construct a SpeechRecognized
                token = speechObjects.Token(best_match, 0, 0, 1000.0, True, True)
                interpretation = speechObjects.Interpretation([token])
                phrase = speechObjects.Phrase(lowConfidence=False, interpretations=[interpretation])
                recognition = speechObjects.Recognition([phrase])
                recognized = speechObjects.SpeechRecognized(requestId, recognition)
                
                if not dictation:
                    if self.current_running_plugin == None:
                        plugin = PluginManager.getPluginForImmediateExecution(self.assistant.assistantId, best_match, self.assistant.language, (self.send_object, self.send_plist, self.assistant, self.current_location))
                        if plugin != None:
                            plugin.refId = requestId
                            plugin.connection = self
                            self.current_running_plugin = plugin
                            self.send_object(recognized)
                            self.current_running_plugin.start()
                        else:
                            self.send_object(recognized)
                            view = uiObjects.AddViews(requestId)
                            errorText = HandleConnection.__not_recognized[self.assistant.language] if self.assistant.language in HandleConnection.__not_recognized else HandleConnection.__not_recognized["en-US"]
                            view.views += [uiObjects.AssistantUtteranceView(errorText.format(best_match), errorText.format(best_match))]
                            websearchText = HandleConnection.__websearch[self.assistant.language] if self.assistant.language in HandleConnection.__websearch else HandleConnection.__websearch["en-US"]
                            button = uiObjects.Button(text=websearchText)
                            cmd = systemObjects.SendCommands()
                            cmd.commands = [systemObjects.StartRequest(utterance=u"^webSearchQuery^=^{0}^^webSearchConfirmation^=^Yes^".format(best_match))]
                            button.commands = [cmd]
                            view.views.append(button)
                            self.send_object(view)
                            self.send_object(baseObjects.RequestCompleted(requestId))
                    elif self.current_running_plugin.waitForResponse != None:
                        # do we need to send a speech recognized here? i.d.k
                        self.current_running_plugin.response = best_match
                        self.current_running_plugin.refId = requestId
                        self.current_running_plugin.waitForResponse.set()
                    else:
                        self.send_object(recognized)
                        self.send_object(baseObjects.RequestCompleted(requestId))
                else:
                    self.send_object(recognized)
                    self.send_object(baseObjects.RequestCompleted(requestId))

    def process_compressed_data(self):
        self.unzipped_input += self.decompressor.decompress(self.data)
        self.data = ""
        while self.hasNextObj():
            reqObject = self.read_next_object_from_unzipped()
            if reqObject != None:
                self.logger.debug("Packet with class: {0}".format(reqObject['class']))
                self.logger.debug("packet with content:\n{0}".format(pprint.pformat(reqObject, width=40)))
                
                # first handle speech stuff
                
                if 'refId' in reqObject:
                    # if the following holds, this packet is an answer to a request by a plugin
                    if reqObject['refId'] == self.plugin_lastAceId and self.current_running_plugin != None:
                        if self.current_running_plugin.waitForResponse != None:
                            # just forward the object to the 
                            # don't change it's refId, further requests must reference last FinishSpeech
                            self.logger.info("Forwarding object to plugin")
                            self.plugin_lastAceId = None
                            self.current_running_plugin.response = reqObject if reqObject['class'] != "StartRequest" else reqObject['properties']['utterance']
                            self.current_running_plugin.waitForResponse.set()
                            continue
                
                if ObjectIsCommand(reqObject, StartSpeechRequest) or ObjectIsCommand(reqObject, StartSpeechDictation):
                    self.logger.info("New start of speech received")
                    startSpeech = None
                    if ObjectIsCommand(reqObject, StartSpeechDictation):
                        dictation = True
                        startSpeech = StartSpeechDictation(reqObject)
                    else:
                        dictation = False
                        startSpeech = StartSpeechRequest(reqObject)
            
                    decoder = speex.Decoder()
                    encoder = flac.Encoder()
                    speexUsed = False
                    if startSpeech.codec == StartSpeech.CodecSpeex_WB_Quality8Value:
                        decoder.initialize(mode=speex.SPEEX_MODEID_WB)
                        encoder.initialize(16000, 1, 16)
                        speexUsed = True
                    elif startSpeech.codec == StartSpeech.CodecSpeex_NB_Quality7Value:
                        decoder.initialize(mode=speex.SPEEX_MODEID_NB)
                        encoder.initialize(16000, 1, 16)
                        speexUsed = True
                    elif startSpeech.codec == StartSpeech.CodecPCM_Mono_16Bit_8000HzValue:
                        encoder.initialize(8000, 1, 16)
                    elif startSpeech.codec == StartSpeech.CodecPCM_Mono_16Bit_11025HzValue:
                        encoder.initialize(11025, 1, 16)
                    elif startSpeech.coded == StartSpeech.CodecPCM_Mono_16Bit_16000HzValue:
                        encoder.initialize(16000, 1, 16)
                    elif startSpeech.coded == StartSpeech.CodecPCM_Mono_16Bit_22050HzValue:
                        encoder.initialize(22050, 1, 16)
                    elif startSpeech.coded == StartSpeech.CodecPCM_Mono_16Bit_32000HzValue:
                        encoder.initialize(32000, 1, 16)
                    # we probably need resampling for sample rates other than 16kHz...
                    
                    self.speech[startSpeech.aceId] = (decoder if speexUsed else None, encoder, dictation)
                
                elif ObjectIsCommand(reqObject, SpeechPacket):
                    self.logger.info("Decoding speech packet")
                    speechPacket = SpeechPacket(reqObject)
                    (decoder, encoder, dictation) = self.speech[speechPacket.refId]
                    if decoder:
                        pcm = decoder.decode(speechPacket.packets)
                    else:
                        pcm = SpeechPacket.data # <- probably data... if pcm
                    encoder.encode(pcm)
                        
                elif reqObject['class'] == 'StartCorrectedSpeechRequest':
                    self.process_recognized_speech({u'hypotheses': [{'confidence': 1.0, 'utterance': str.lower(reqObject['properties']['utterance'])}]}, reqObject['aceId'], False)
            
                elif ObjectIsCommand(reqObject, FinishSpeech):
                    self.logger.info("End of speech received")
                    finishSpeech = FinishSpeech(reqObject)
                    (decoder, encoder, dictation) = self.speech[finishSpeech.refId]
                    if decoder:
                        decoder.destroy()
                    encoder.finish()
                    flacBin = encoder.getBinary()
                    encoder.destroy()
                    del self.speech[finishSpeech.refId]
                    
                    self.logger.info("Sending flac to google for recognition")
                    try:
                        self.httpClient.make_google_request(flacBin, finishSpeech.refId, dictation, language=self.assistant.language, allowCurses=True)
                    except AttributeError, TypeError:
                        self.logger.info("Unable to find language record for this assistant. Try turning Siri off and then back on.")
                        
                elif ObjectIsCommand(reqObject, CancelRequest):
                        # this is probably called when we need to kill a plugin
                        # wait for thread to finish a send
                        cancelRequest = CancelRequest(reqObject)
                        if cancelRequest.refId in self.speech:
                            del self.speech[cancelRequest.refId]
                        
                        self.send_object(CancelSucceeded(cancelRequest.aceId))

                elif ObjectIsCommand(reqObject, GetSessionCertificate):
                    getSessionCertificate = GetSessionCertificate(reqObject)
                    response = GetSessionCertificateResponse(getSessionCertificate.aceId, caCert.as_der(), serverCert.as_der())
                    self.send_object(response)

                elif ObjectIsCommand(reqObject, CreateSessionInfoRequest):
                    # how does a positive answer look like?
                    createSessionInfoRequest = CreateSessionInfoRequest(reqObject)
                    fail = CommandFailed(createSessionInfoRequest.aceId)
                    fail.reason = "Not authenticated"
                    fail.errorCode = 0
                    self.send_object(fail)

                    #self.send_plist({"class":"SessionValidationFailed", "properties":{"errorCode":"UnsupportedHardwareVersion"}, "aceId": str(uuid.uuid4()), "refId":reqObject['aceId'], "group":"com.apple.ace.system"})
                    
                elif reqObject['class'] == 'CreateAssistant':
                    #create a new assistant
                    helper = Assistant()
                    c = self.dbConnection.cursor()
                    noError = True
                    try:
                        c.execute("insert into assistants(assistantId, assistant) values (?,?)", (helper.assistantId, helper))
                        self.dbConnection.commit()
                    except sqlite3.Error, e: 
                        noError = False
                    c.close()
                    if noError:
                        self.assistant = helper
                        self.send_plist({"class": "AssistantCreated", "properties": {"speechId": str(uuid.uuid4()), "assistantId": helper.assistantId}, "group":"com.apple.ace.system", "callbacks":[], "aceId": str(uuid.uuid4()), "refId": reqObject['aceId']})
                    else:
                        self.send_plist({"class":"CommandFailed", "properties": {"reason":"Database error", "errorCode":2, "callbacks":[]}, "aceId": str(uuid.uuid4()), "refId": reqObject['aceId'], "group":"com.apple.ace.system"})
            
                elif reqObject['class'] == 'SetAssistantData':
                    # fill assistant 
                    if self.assistant != None:
                        c = self.dbConnection.cursor()
                        objProperties = reqObject['properties'] 
                        self.assistant.censorSpeech = objProperties['censorSpeech']
                        self.assistant.timeZoneId = objProperties['timeZoneId']
                        self.assistant.language = objProperties['language']
                        self.assistant.region = objProperties['region']
                        c.execute("update assistants set assistant = ? where assistantId = ?", (self.assistant, self.assistant.assistantId))
                        self.dbConnection.commit()
                        c.close()

            
                elif reqObject['class'] == 'LoadAssistant':
                    c = self.dbConnection.cursor()
                    c.execute("select assistant from assistants where assistantId = ?", (reqObject['properties']['assistantId'],))
                    self.dbConnection.commit()
                    result = c.fetchone()
                    if result == None:
                        self.send_plist({"class": "AssistantNotFound", "aceId":str(uuid.uuid4()), "refId":reqObject['aceId'], "group":"com.apple.ace.system"})
                    else:
                        self.assistant = result[0]
                        self.send_plist({"class": "AssistantLoaded", "properties": {"version": "20111216-32234-branches/telluride?cnxn=293552c2-8e11-4920-9131-5f5651ce244e", "requestSync":False, "dataAnchor":"removed"}, "aceId":str(uuid.uuid4()), "refId":reqObject['aceId'], "group":"com.apple.ace.system"})
                    c.close()

                elif reqObject['class'] == 'DestroyAssistant':
                    c = self.dbConnection.cursor()
                    c.execute("delete from assistants where assistantId = ?", (reqObject['properties']['assistantId'],))
                    self.dbConnection.commit()
                    c.close()
                    self.send_plist({"class": "AssistantDestroyed", "properties": {"assistantId": reqObject['properties']['assistantId']}, "aceId":str(uuid.uuid4()), "refId":reqObject['aceId'], "group":"com.apple.ace.system"})
                elif reqObject['class'] == 'StartRequest':
                    #this should also be handeled by special plugins, so lets call the plugin handling stuff
                    self.process_recognized_speech({'hypotheses': [{'utterance': reqObject['properties']['utterance'], 'confidence': 1.0}]}, reqObject['aceId'], False)

                    
    def hasNextObj(self):
        if len(self.unzipped_input) == 0:
            return False
        cmd, data = struct.unpack('>BI', self.unzipped_input[:5])
        if cmd in (3,4): #ping pong
            return True
        if cmd == 2:
            #print "expect: ", data+5,  " received: ", len(self.unzipped_input)
            return ((data + 5) < len(self.unzipped_input))
    
    def read_next_object_from_unzipped(self):
        cmd, data = struct.unpack('>BI', self.unzipped_input[:5])
        
        if cmd == 3: #ping
            self.ping = data
            self.logger.info("Received a Ping ({0})".format(data))
            self.logger.info("Returning a Pong ({0})".format(self.pong))
            self.send_pong(self.pong)
            self.pong += 1
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
        ratio = float(len(self.unzipped_output_buffer))/float(len(self.output_buffer)) - 1
        if ratio < 0:
            self.logger.debug("Blowed up by {0:.2f} bytes ({1:.2%}) due to compression".format(-1*ratio*len(self.unzipped_output_buffer),ratio))
        else:
            self.logger.debug("Saved {0:.2f} bytes ({1:.2%}) using compression".format(ratio*len(self.unzipped_output_buffer), ratio))
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
        logging.getLogger("logger").info("Listening on port {0}".format(port))
        signal.signal(signal.SIGTERM, self.handler)
   
    def handler(self, signum, frame):
        if signum == signal.SIGTERM:
            x.info("Got SIGTERM, closing server")
            self.close()
    

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            logging.getLogger("logger").info('Incoming connection from {0}'.format(repr(addr)))
            handler = HandleConnection(sock)

# load the certificates
caCertFile = open('OrigAppleSubCACert.der')
caCert = X509.load_cert_bio(BIO.MemoryBuffer(caCertFile.read()), format=0)
caCertFile.close()
certFile = open('OrigAppleServerCert.der')
serverCert = X509.load_cert_bio(BIO.MemoryBuffer(certFile.read()), format=0)
certFile.close()



#setup logging

log_levels = {'debug':logging.DEBUG,
              'info':logging.INFO,
              'warning':logging.WARNING,
              'error':logging.ERROR,
              'critical':logging.CRITICAL
              }

parser = OptionParser()
parser.add_option('-l', '--loglevel', default='info', dest='logLevel', help='This sets the logging level you have these options: debug, info, warning, error, critical \t\tThe standard value is info')
parser.add_option('-p', '--port', default=443, type='int', dest='port', help='This options lets you use a custom port instead of 443 (use a port > 1024 to run as non root user)')
parser.add_option('--logfile', default=None, dest='logfile', help='Log to a file instead of stdout.')
(options, args) = parser.parse_args()

x = logging.getLogger("logger")
x.setLevel(log_levels[options.logLevel])

if options.logfile != None:
    h = logging.FileHandler(options.logfile)
else:
    h = logging.StreamHandler()

f = logging.Formatter(u"%(levelname)s %(funcName)s %(message)s")
h.setFormatter(f)
x.addHandler(h)


#setup database
db.setup()

#load Plugins
PluginManager.load_api_keys()
PluginManager.load_plugins()


#start server
x.info("Starting Server")
server = SiriServer('', options.port)
try:
    asyncore.loop()
except (asyncore.ExitNow, KeyboardInterrupt, SystemExit):
    x.info("Caught shutdown, closing server")
    asyncore.dispatcher.close(server)
    exit()
