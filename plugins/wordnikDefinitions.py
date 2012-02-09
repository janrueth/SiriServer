#!/usr/bin/python
# -*- coding: utf-8 -*-

#Wordnik plugin
#by Ryan Davis (neoshroom)
#feel free to add to, mess with, use this plugin with original attribution
#additional Wordnik functions to add can be found at:
#http://developer.wordnik.com/docs/

from plugin import *
from plugin import __criteria_key__
#you will need to install the Wordnik API to use this
#this can be done from the commandline by typing: easy_install Wordnik

from wordnik import Wordnik

#if below does not have a long alphanumeric string for the api key, you can get yours at http://developer.wordnik.com/ (first you sign up for a username in the upp$
########################################################

wordnik_api_key = "" # PUT YOUR API KEY HERE in " "

#########################################################

if wordnik_api_key == "":
   raise Exception("APIKeyNotFound", "You must specify a wordnik API key")
w = Wordnik(api_key=wordnik_api_key)

class define(Plugin):
    
    @register("en-US", "define ([\w ]+)")
    def defineword(self, speech, language):
        matcher = self.defineword.__dict__[__criteria_key__][language]
        regMatched = matcher.match(speech)
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
