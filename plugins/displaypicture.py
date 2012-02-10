#displaypicture.py

#Google Image Plugin v0.2
#by Ryan Davis (neoshroom)
#feel free to add to, mess with and use this plugin with original attribution
#additional Google Image functions to add can be found at:
#https://developers.google.com/image-search/v1/jsondevguide#request_format

#usage: say "display a picture of william shakespeare" 
#(or anything else you want a picture of)

import re
import urllib2, urllib
import json

from plugin import *
from plugin import __criteria_key__

from siriObjects.uiObjects import AddViews
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine

class define(Plugin):
    
    @register("de-DE", "(zeig mir|zeige|zeig).*(bild|zeichnung) (vo. ein..|vo.|aus)* ([\w ]+)")
    @register("en-US", "(display|show me|show).*(picture|image|drawing|illustration) (of|an|a)* ([\w ]+)")
    def defineword(self, speech, language, regex):
        Title = regex.group(regex.lastindex)
        Query = urllib.quote_plus(Title.encode("utf-8"))
        SearchURL = u'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&imgsz=small|medium|large|xlarge&q=' + str(Query)
        try:
            jsonResponse = urllib2.urlopen(SearchURL).read()
            jsonDecoded = json.JSONDecoder().decode(jsonResponse)
            ImageURL = jsonDecoded['responseData']['results'][0]['unescapedUrl']
            view = AddViews(self.refId, dialogPhase="Completion")
            ImageAnswer = AnswerObject(title=str(Title),lines=[AnswerObjectLine(image=ImageURL)])
            view1 = AnswerSnippet(answers=[ImageAnswer])
            view.views = [view1]
            self.sendRequestWithoutAnswer(view)
            self.complete_request()
        except (urllib2.URLError):
            self.say("Sorry, a connection to Google Images could not be established.")
            self.complete_request()
