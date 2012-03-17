#!/usr/bin/python
# -*- coding: utf-8 -*-
#Created by Erich Budianto (praetorians)

from plugin import *
import random
import re
import urllib2, urllib, uuid
import json
from urllib2 import urlopen
from xml.dom import minidom

class horoscope(Plugin):
	
        @register ("en-GB", "(Tell me the horoscope for [a-zA-Z]+)|(Horoscope for [a-zA-Z]+)|(Horoscope for [a-zA-Z]+)|(The horoscope for [a-zA-Z]+)")
	@register ("en-US", "(Tell me the horoscope for [a-zA-Z]+)|(Horoscope for [a-zA-Z]+)|(Horoscope for [a-zA-Z]+)|(The horoscope for [a-zA-Z]+)")
	@register ("fr-FR", "(Quel est mon horoscope pour [a-zA-Z]+)|(Horoscope pour [a-zA-Z]+)|(Horoscope pour [a-zA-Z]+)|(Votre horoscope pour [a-zA-Z]+)")
	def horoscope_zodiac(self, speech, language):
	    zodiac = speech.replace('Quel est ','').replace('votre ','').replace('Votre ', '').replace('horoscope','').replace('Horoscope','').replace('pour ', '').replace('Tell me the','').replace('for','').replace('The','').replace(' ','')
            print ("Zodiac: {0}".format(zodiac))
            linkurl = 'http://widgets.fabulously40.com/horoscope.json?sign=%s' % zodiac
            print linkurl
	    req=urllib.urlopen(linkurl)
            full_json=req.read()
	    full=json.loads(full_json)
            try:
                self.say(full['horoscope']['horoscope'])
                
            except KeyError: 
                self.say("Sorry I did not find a horoscope for zodiac {0}".format(zodiac))
            self.complete_request()