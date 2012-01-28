#!/usr/bin/python
# -*- coding: utf-8 -*-


from plugin import *

class examplePlugin(Plugin):
    
    @register("de-DE", ".*Sinn.*Leben.*")
    @register("en-US", ".*Meaning.*Life.*")
    def meaningOfLife(self, speech, language):
        if language == 'de-DE':
            self.say(u"Das sollte ich dir nicht sagen!")
        else:
            self.say("I shouldn't tell you!")
        self.complete_request()
