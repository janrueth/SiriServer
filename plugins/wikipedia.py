#!/usr/bin/python
# -*- coding: utf-8 -*-

#need help? ask john-dev
#will add list response support for "unfound" search strings, since wikipedia-api is case sensivity only, it's not implented yet..
#at least it's prepared for..
#btw, can't modify wikipedias language since WebSearch (class) decides that on it's own..

import re
import urllib2, urllib
import json
import time
 
from plugin import *
 
from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView, OpenLink
from siriObjects.websearchObjects import WebSearch

 
class wikiPedia(Plugin):
    
    @register("de-DE", "wikipedia (.*)")    
    @register("en-US", "wikipedia (.*)")
    @register("fr-FR", u".*cherche (.*) sur wikipedia|.*cherche (.*) sur wiki|.*(wikipedia|wiki) (.*)")
    def askWiki(self, speech, language, regex):
        wikiLanguage=language[0:2]
        searchString = regex.group(regex.lastindex).strip()
        #searchString=searchString.replace(' ','_')
        url = "http://{0}.wikipedia.org/w/api.php?format=json&action=query&titles={1}&prop=revisions&rvprop=content".format(wikiLanguage,urllib.quote_plus(str(searchString.encode("utf-8"))))
        try:
            jsonString = urllib2.urlopen(url, timeout=3).read()
        except:
            jsonString = None
        if jsonString != None:
            response = json.loads(jsonString)
            if response['query']['pages'].keys()[0] > 0:
                pageId=response['query']['pages'].keys()[0]
                title=response['query']['pages'][pageId]['title']
                if language=="de-DE":
                    self.say(u"Nach \"{0}\" suchen...".format(title), None)
                elif language=="fr-FR":
                    self.say(u"Recherche de \"{0}\"...".format(title), None)
                else:
                    self.say(u"Searching for \"{0}\"...".format(title), None)
                wikiSearch = WebSearch(refId=self.refId,query=searchString,provider="Wikipedia")
                time.sleep(2)
                self.sendRequestWithoutAnswer(wikiSearch)
                self.complete_request()
            else:                
                if language=="de-DE":
                    self.say('Ich habe nichts zu \"{0}\" auf Wikipedia gefunden'.format(searchString))
                elif language=="fr-FR":
                    self.say(u'Je n\'ai rien trouvé sur Wikipedia pour \"{0}\"'.format(searchString))
                else:
                    self.say("Nothing found for \"{0}\" on Wikipedia".format(searchString))
        else:
                if language=="de-DE":
                    self.say('Ich konnte keine Verbindung zu Wikipedia aufbauen.')
                elif language=="fr-FR":
                    self.say(u'Je n\'arrive pas à me connecter à Wikipedia.')
                else:
                    self.say("Couldn't establish connection to Wikipedia")
        self.complete_request()
