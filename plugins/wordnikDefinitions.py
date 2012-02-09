#!/usr/bin/python
# -*- coding: utf-8 -*-

#Wordnik plugin
#by Ryan Davis (neoshroom)
#feel free to add to, mess with, use this plugin with original attribution
#additional Wordnik functions to add can be found at:
#http://developer.wordnik.com/docs/

from plugin import *
#you will need to install the Wordnik API to use this
#this can be done from the commandline by typing: easy_install Wordnik
try:
   from wordnik import Wordnik
except ImportError:
   raise NecessaryModuleNotFound("Wordnik library not found. Please install wordnik library! e.g. sudo easy_install wordnik")

#You need a wordnik api key, you can get yours at http://developer.wordnik.com/ (first you sign up for a username in the upp$
########################################################

wordnik_api_key = APIKeyForAPI("wordnik")

#########################################################

w = Wordnik(api_key=wordnik_api_key)

class define(Plugin):
    
    @register("en-US", "define ([\w ]+)")
    def defineword(self, speech, language, regMatched):
        Question = regMatched.group(1)
        output = w.word_get_definitions(Question, limit=1)
        if len(output) == 1:
            answer = dict(output[0])
            if u'text' in answer:
                worddef = answer[u'text']
                if worddef:
                    self.say(worddef, "The definition of {0} is: {1}".format(Question, worddef))
                else:
                    self.say("Sorry, I could not find " + Question + " in the dictionary.")
        else:
            self.say("Sorry, I could not find " + Question + " in the dictionary.")

        self.complete_request()
