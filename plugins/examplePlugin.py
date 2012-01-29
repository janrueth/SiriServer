#!/usr/bin/python
# -*- coding: utf-8 -*-


from plugin import *

class examplePlugin(Plugin):
    
    @register("de-DE", ".*Sinn.*Leben.*")
    @register("en-US", ".*Meaning.*Life.*")
    def meaningOfLife(self, speech, language):
        if language == 'de-DE':
            answer = self.ask(u"Willst du das wirklich wissen?")
            self.say(u"Du hast \"{0}\" gesagt!".format(answer))
        else:
            self.say("I shouldn't tell you!")
        self.complete_request()
