#!/usr/bin/python

# IMDB.py
# Based on Nurfballs SickBeard.py
# v0.1

import re, urlparse
import urllib2, urllib
import json
from urllib2 import urlopen
from xml.dom import minidom

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine

class define(Plugin):
 
    # ------------------------------------------
    # - Display movie info -
    # -------------------------------------------
    #@register("en-US",  "(movie [a-zA-Z0-9]+)")
    @register("en-GB", "(movie)* ([\w ]+)")
    @register("en-US", "(movie)* ([\w ]+)")
    def imdb_info(self,  speech,  language,  regex):
        ShowTitle = regex.group(regex.lastindex)
        Query = urllib.quote_plus(ShowTitle.encode("utf-8"))
        IMDBURL = 'http://www.imdbapi.com/?i=&t=%s' % (str(Query))
        try:
            # Query IMDB
            jsonResponse = urllib2.urlopen(IMDBURL).read()
            jsonDecoded = json.JSONDecoder().decode(jsonResponse)
            
            self.say("Here is the info about the movie:")
            view = AddViews(self.refId, dialogPhase="Completion")

            AnswerString = jsonDecoded['Title'] + ' (' + jsonDecoded['Released'] + ')' + '\n Genre: ' + jsonDecoded['Genre'] + '\n Directors: ' + jsonDecoded['Director'] + '\n Actors: ' + jsonDecoded['Actors'] + '\n Plot: ' + jsonDecoded['Plot'] + '\n Runtime: ' + jsonDecoded['Runtime'] + '\n Rating: ' + jsonDecoded['Rating'] + ' / Voted: ' + jsonDecoded['Votes'] + 'x'
            IMDBAnswerMissed = AnswerObject(title='IMDB:',lines=[AnswerObjectLine(text=AnswerString)]) 

            view1 = 0
            view1 = AnswerSnippet(answers=[IMDBAnswerMissed])
            view.views = [view1]
            self.sendRequestWithoutAnswer(view)
            self.complete_request()
        except (urllib2.URLError):
            self.say("Sorry, a connection to IMDBapi could not be established.")
            self.complete_request()

 
    # ------------------------------------------
    # - Display poster info -
    # -------------------------------------------
    #@register("en-US",  "(poster [a-zA-Z0-9]+)")
    @register("en-GB", "(poster)* ([\w ]+)")
    @register("en-US", "(poster)* ([\w ]+)")
    def imdb_poster(self,  speech,  language,  regex):
        ShowTitle = regex.group(regex.lastindex)
        Query = urllib.quote_plus(ShowTitle.encode("utf-8"))
        IMDBURL = 'http://www.imdbapi.com/?i=&t=%s' % (str(Query))
        try:
            # Query IMDB
            jsonResponse = urllib2.urlopen(IMDBURL).read()
            jsonDecoded = json.JSONDecoder().decode(jsonResponse)
            
            self.say("Here is the movie poster:")
            view = AddViews(self.refId, dialogPhase="Completion")

            AnswerString = jsonDecoded['Poster']
            IMDBAnswerMissed = AnswerObject(title='Movie Poster:',lines=[AnswerObjectLine(image=AnswerString)]) 

            view1 = 0
            view1 = AnswerSnippet(answers=[IMDBAnswerMissed])
            view.views = [view1]
            self.sendRequestWithoutAnswer(view)
            self.complete_request()
        except (urllib2.URLError):
            self.say("Sorry, a connection to IMDBapi could not be established.")
            self.complete_request()