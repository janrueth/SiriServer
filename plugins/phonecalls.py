#!/usr/bin/python
# -*- coding: utf-8 -*-

from plugin import *
from siriObjects.baseObjects import ObjectIsCommand
from siriObjects.contactObjects import PersonSearch, PersonSearchCompleted


responses = {
'notFound': 
    {'de-DE': u"Entschuldigung, ich konnte niemanden in deinem Telefonbuch gefunden der so heißt",
     'en-US': u"Sorry, I did not find a match in your phone book"
    },
'devel':
    {'de-DE': u"Entschuldigung, aber diese Funktion befindet sich noch in der Entwicklungsphase",
     'en-US': u"Sorry this feature is still under development"
    }
}

class phonecallPlugin(Plugin):
    
    def searchUserByName(personToLookup):
        search = PersonSearch(self.refId, name=personToLookup)
        answerObj = self.getResponseForRequest(search)
        if ObjectIsCommand(answerObj, PersonSearchCompleted):
            answer = PersonSearchCompleted(answerObj)
            return answer.results if answer.results != None else []
        else:
            raise StopPluginExecution("Unknown response: {0}".format(answerObj))
        return []
                                      
    
    def call(person):
        pass
    
    @register("de-DE", "ruf. ([\w ]+) an")
    @register("en-US", "(make a )?call (to )?([\w ]+)")
    def makeCall(self, speech, language, regex):
        self.say(responses['devel'][language])
        self.complete_request()
        return 
        personToCall = regex.group(regex.lastindex)
        
        options = searchUserByName(persontoCall)
        if len(options) > 0:
            pass
        # what is siri doing here We should probably list the possible users
        # and continue asking for one specific until we found the correct one
        # 
        else:
             self.say(responses['notFound'][language])                         
        self.complete_request()
    
