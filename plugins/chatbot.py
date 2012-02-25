#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Daniel "P4r4doX" Zaťovič
#Edited by boeaja

from plugin import *
import urllib2 
from xml.dom.minidom import parseString

#You can choose your own BOT here : http://pandorabots.com/botmaster/en/~1ce90ef1ac87f6dc9dce531~/mostactive
# EVE
botID = "a9481f8c7e347656"

# A.L.I.C.E
#botID = "f5d922d97e345aa1"



def askBOT(input):	
	#convert symbols to HEX
	input = input.replace(' ', '%20')
	input = input.replace('?', '%3F')
	input = input.replace('$', '%24')
	input = input.replace('+', '%2B')
	input = input.replace(',', '%2C')
	input = input.replace('/', '%2F')
	input = input.replace(':', '%3A') 
	input = input.replace(';', '%3B') 
	input = input.replace('=', '%3D') 
	input = input.replace('@', '%40')	
	file = urllib2.urlopen('http://www.pandorabots.com/pandora/talk-xml?botid=%s&input=%s' % (botID, input))	
	data = file.read()	
	file.close()	
	dom = parseString(data)	
	xmlTag = dom.getElementsByTagName('that')[0].toxml()	
	xmlData=xmlTag.replace('<that>','').replace('</that>','')
	#convert symbols
	xmlData = xmlData.replace('&quot;', '"')
        xmlData = xmlData.replace('&lt;', '<')
        xmlData = xmlData.replace('&gt;', '>')
        xmlData = xmlData.replace('&amp;', '&')
        xmlData = xmlData.replace('<br>', ' ')
	return xmlData

def respond(self, input):
    if input == 'Stop':
        self.say("Nice to chat with you, see u next time")
        self.complete_request()
    else:
        answer = self.ask(askBOT(input))
        respond(self, answer)
    self.complete_request()
                              
class chatBOT(Plugin):

    @register("en-US", "Let's chat")
    def BOT_Message(self, speech, language):
        if language == 'en-US':
            answer = self.ask(u"Ok, Let's chat")
            respond(self, answer)
            #self.say(askBOT(speech))
	    self.complete_request() 