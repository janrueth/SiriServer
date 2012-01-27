#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, ssl, sys, zlib, binascii, time, select, struct, biplist
from email.utils import formatdate
import uuid
import speex
import flac
import json
import asyncore
import re

from M2Crypto import BIO, RSA, X509

from siriObjects import speechObjects, baseObjects, uiObjects

from httpClient import AsyncOpenHttp

from sslDispatcher import ssl_dispatcher

caCertFile = open('OrigAppleSubCACert.der')
caCert = X509.load_cert_bio(BIO.MemoryBuffer(caCertFile.read()), format=0)
caCertFile.close()
certFile = open('OrigAppleServerCert.der')
serverCert = X509.load_cert_bio(BIO.MemoryBuffer(certFile.read()), format=0)
certFile.close()



class HandleConnection(ssl_dispatcher):
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
		print "Sending: ", plist
		bplist = biplist.writePlistToString(plist);
		#
		self.unzipped_output_buffer = struct.pack('>BI', 2,len(bplist)) + bplist
		self.flush_unzipped_output() 
	
	def send_pong(self, id):
		self.unzipped_output_buffer = struct.pack('>BI', 4, id)
		self.flush_unzipped_output() 

	def process_recognized_speech(self, googleJson, requestId, dictation):
		if googleJson == None:
			# there was a network failure
			self.send_object(speechObjects.SpeechFailure(requestId, "No connection to Google possible"))
			self.send_object(baseObjects.RequestCompleted(requestID))
		else:
			possible_matches = googleJson['hypotheses']
			if len(possible_matches) > 0:
				best_match = possible_matches[0]['utterance']
				best_match_confidence = possible_matches[0]['confidence']
				print u"Best matching result: \"{0}\" with a confidence of {1}%".format(best_match, round(float(best_match_confidence)*100,2))
				
				# construct a SpeechRecognized
				token = speechObjects.Token(best_match, 0, 0, 1000.0, True, True)
				interpretation = speechObjects.Interpretation([token])
				phrase = speechObjects.Phrase(lowConfidence=False, interpretations=[interpretation])
				recognition = speechObjects.Recognition([phrase])
				recognized = speechObjects.SpeechRecognized(requestId, recognition)
				
				# Send speechRecognized to iDevice
				self.send_object(recognized)
				
				# HERE WE SHOULD INSERT PLUGIN FILTERING
				
				if not dictation:
					# Just for now echo the detected text
					view = uiObjects.AddViews(requestId)
					answer = best_match
					view.views += [uiObjects.AssistantUtteranceView(text=answer, speakableText=answer)]
					self.send_object(view)
				
				# at the end we need to finish the request
				self.send_object(baseObjects.RequestCompleted(requestId))

			

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
					dictation=(object['class'] == 'StartSpeechDictation')
					self.speech[object['aceId']] = (decoder, encoder, dictation)
					
				if object['class'] == 'SpeechPacket':
					(decoder, encoder, dictation) = self.speech[object['refId']]
					pcm = decoder.decode(object['properties']['packets'])
					encoder.encode(pcm)
				
				if object['class'] == 'CancelRequest':
					# we should test if this stil exists..
					del self.speech[object['refId']]

				if object['class'] == 'StartCorrectedSpeechRequest':
					self.process_recognized_speech({u'hypotheses': [{u'confidence': 1.0, u'utterance': str.lower(object['properties']['utterance'])}]}, object['aceId'], False)
				elif object['class'] == 'FinishSpeech':
					(decoder, encoder, dictation) = self.speech[object['refId']]
					decoder.destroy()
					encoder.finish()
					flacBin = encoder.getBinary()
					encoder.destroy()
					del self.speech[object['refId']]
					
					self.httpClient.make_google_request(flacBin, object['refId'], dictation, language='de-DE', allowCurses=True)
					
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
