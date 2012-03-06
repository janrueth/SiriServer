#!/usr/bin/python
# -*- coding: utf-8 -*-
# siriServer GoogleVoice Plugin_NODB 1.0 
#Author: SNXRaven (Jonathon Nickols)
# This requires: http://code.google.com/p/pygooglevoice/ is installed

from plugin import *
from googlevoice import Voice
from googlevoice.util import input
import re

class raven_test(Plugin):


    @register("en-US", "(Send.*text.*message to [a-zA-Z0-9]+)")
    def r_gvsms(self, speech, language):
        match = re.match(u"Send text message to (.*\d.*) say (.*\D.*)", speech, re.IGNORECASE)
        phoneNumber = match.group(1)
        text = match.group(2)
        voice = Voice()
        voice.login('googleemail@gmail.com', 'googlepass')
        voice.send_sms(phoneNumber, text)
        self.say('Your message has been sent!')
        self.complete_request()
