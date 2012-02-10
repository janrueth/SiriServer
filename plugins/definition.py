#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2, urllib
import json
import unicodedata
from plugin import *

class definition(Plugin):
 
    @register("fr-FR", u"(defini|definit|défini|définit|definis|définis|définition|definition) (.*)")
    def define(self, speech, language, regMatched):
        query = regMatched.group(regMatched.lastindex).strip()
        self.say(u"Je recherche la définition de "+query+"...")
        query_clean = self.cleanString(query)
        url = u"http://www.google.com/dictionary/json?callback=dict_api.callbacks.id100&q=" +urllib.quote_plus(query_clean.encode("utf-8"))+ "&sl="+language+"&tl="+language+"&restrict=pr%2Cde&client=te"
        print url
        definition = None
        try:
            jsonString = urllib2.urlopen(url, timeout=3).read()
            jsonString = jsonString.replace(",200,null)","").replace("dict_api.callbacks.id100(","")
            jsonString = jsonString.replace('\\x3c','').replace('\\x3d','').replace('\\x3e','').replace('\\x22','').replace('\\x26','').replace("#39;","'")
            response = json.loads(jsonString)
            definition = response["webDefinitions"][0]["entries"][0]["terms"][0]["text"]
        except:
            pass

        if definition != None:
            self.say(definition);
        else:
            self.say(u"Je n'ai pas trouvé de définition pour " + query)
        
        
        
        self.complete_request()
        
    def cleanString(self, s):
        if isinstance(s,str):
            s = unicode(s,"utf8","replace")
        s=unicodedata.normalize('NFD',s)
        return s.encode('ascii','ignore')
