#!/usr/bin/python
# -*- coding: utf-8 -*-

##Author: Alexandre Daoud
##Script: Translation plugin for Siri Server using Bing API
##Version: 1.0 - With German Language
import re
import urllib2, urllib
import json
from urllib2 import urlopen
from xml.etree import ElementTree as ET

from plugin import *

#appid to connect to bing API http://www.microsoft.com/web/post/using-the-free-bing-translation-apis
appid = APIKeyForAPI("bingTranslate")

#dictionary for language name --> code conversion

languages = {"arabic": "ar", "czech": "cs","check": "cs","czech language": "cs","danish": "da","german": "de","english": "en","estonian": "et","finnish": "fi","french": "fr","dutch": "nl","greek": "el","hebrew": "he","haitian creole": "ht","hungarian": "hu","indonesian": "id","italian": "it","japanese": "ja","korean": "ko","lithuanian": "lt","latvian": "lv","norwegian": "no","polish": "pl","portuguese": "pt","romanian": "ro","spanish": "es","russian": "ru","slovak": "sk","slovene": "sl","swedish": "sv","thai": "th","turkish": "tr","ukranian": "uk","vietnamese": "vi","simplified chinese": "zh-CHS","traditional chinese": "zh-CHT"}

languagesde = {"arabisch": "ar", "tschechisch": "cs","dänisch": "da","deutsch": "de","englisch": "en","estnisch": "et","finnisch": "fi","französisch": "fr","holländer": "nl","griechisch": "el","hebräisch": "he","haiti-kreolisch": "ht","ungarisch": "hu","indonesier": "id","italienisch": "it","japanisch": "ja","koreanisch": "ko","litauisch": "lt","lettisch": "lv","norwegisch": "no","politur": "pl","portugiesisch": "pt","rumänisch": "ro","spanisch": "es","russisch": "ru","slowakisch": "sk","slowenisch": "sl","schwedisch": "sv","thailändisch": "th","türkisch": "tr","ukrainisch": "uk","vietnamesisch": "vi","vereinfachtes chinesisch": "zh-CHS","traditionelles chinesisch": "zh-CHT"}  

class translator(Plugin):

    @register("en-US", ".*Translate.*to.*")
    @register("de-DE", ".*Übersetze.*zu.*")
    def translation(self, speech, language):
	sirilang = language	
	if sirilang == "en-US": self.say("Translating...")
	if sirilang == "de-DE": self.say("Ich übersetze...")
#the next line is necessary as we need to remove only the last instance of into (into could appear in the translation query)
	if sirilang == "en-US": text1=(speech[::-1].replace("to"[::-1], "xxxxxx"[::-1], 1))[::-1] 
	if sirilang == "en-US": text = text1.replace("Translate ","",1).replace("translate ","",1)
	if sirilang == "de-DE": text1=(speech[::-1].replace("zu"[::-1], "xxxxxx"[::-1], 1))[::-1] 
	if sirilang == "de-DE": text = text1.replace("Übersetze ","",1).replace("übersetze ","",1)
	phrase = text.split(" xxxxxx ")[0].replace(" ","%20")
	language = text.split(" xxxxxx ")[1]
#manage the communication with the API, parse and output this data
	if language in languages:
		if sirilang == "en-US": langcode = languages[language]
		if sirilang == "de-DE": langcode = languages[language]
		bing = "http://api.microsofttranslator.com/v2/Http.svc/Translate?appId={0}&text={1}&from={2}&to={3}".format(appid,phrase,sirilang.split("-")[0],langcode)
		source = urlopen(bing)
		xml = str(source.read())
		source.close()
		translated = xml.replace('<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">','').replace("</string>","")
		self.say(translated)
		self.complete_request()
#exception if language is not recognised
	else:
		if sirilang == "en-US": self.say("Sorry, I don't recognise the language \"{0}\"...".format(language))
		if sirilang == "de-DE": self.say("Entschuldigung, Ich erkenne \"{0}\" nicht ...".format(language))
		self.complete_request()

	#self.complete_request()
