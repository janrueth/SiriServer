#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bing Traduction
# Par Cédric Boverie (cedbv)
# Clé API nécessaire disponible sur https://be.ssl.bing.com/webmaster/Developers/

import re
import json
import urllib2, urllib
from plugin import *

APIKEY = APIKeyForAPI("bingtranslation")


class Traduction(Plugin):
    
    @register("fr-FR", u"(Traduit|Traduire)(.*) en anglais")
    def traduire(self, speech, language):

        target = "en"

        query = re.match(u"(Traduit|Traduire)(.*)en anglais", speech, re.IGNORECASE)
        if query != None:
            query = query.group(2).strip()		
		
        traduction = None
        try:
            url = "http://api.bing.net/json.aspx?Query=%s&Translation.SourceLanguage=fr&Translation.TargetLanguage=%s&Version=2.2&AppId=%s&Sources=Translation" % (urllib.quote_plus(query.encode("utf-8")),target,APIKEY)
            response = urllib2.urlopen(url, timeout=3).read()
            jsonObj = json.loads(response);
            traduction = jsonObj["SearchResponse"]["Translation"]["Results"][0]["TranslatedTerm"]
        except:
            pass

        if traduction != None:
            self.say(traduction)
        else:
            self.say(u"Désolé, je n'arrive pas à traduire cette expression.")
        self.complete_request()
