#!/usr/bin/python                                                                                                                                                                   
# -*- coding: utf-8 -*-                                                                                                                                                             

from plugin import *
from siriObjects.websearchObjects import WebSearch

class wwwSearch(Plugin):

    @register("en-US", "(web search.*)|(web.*)")
    def webSearch(self, speech, language):

        if (speech.find('Web search') == 0):
            speech = speech.replace('Web search', ' ',1)
        elif (speech.find('Web') == 0):
            speech = speech.replace('Web',' ',1)
        speech = speech.strip()
        if speech == "":
            speech = self.ask("What is your query?")

        search = WebSearch(refId="", aceId="", query=speech)
        self.send_object(search)
        self.complete_request()


