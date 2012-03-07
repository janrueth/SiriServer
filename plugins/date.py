#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import date
import locale 
from plugin import *

class talkToMe(Plugin):   
        
    @register("de-DE", ".*Dein.*Status.*")
    @register("en-US", ".*Your.*Status.*")
    @register("fr-FR", ".*Votre.*Statut.*")
    def ttm_uptime_status(self, speech, language):
        uptime = os.popen("uptime").read()
        if language == 'de-DE':
            self.say('Hier ist der Status:')
            self.say(uptime, ' ')
        elif language == 'fr-FR':
            self.say('Voici votre statut:')
            self.say(uptime, ' ')
        else:
            self.say('Here is the status:')
            self.say(uptime, ' ')
        self.complete_request()     
    
    
    @register("de-DE", "(Welcher Tag.*)|(Welches Datum.*)")
    @register("en-US", "(What Day.*)|(What.*Date.*)")
    @register("fr-FR", "(Quel jour.*)|(Quelle date.*)")
    
    def ttm_say_date(self, speech, language):
        now = date.today()
        if language == 'de-DE':
            locale.setlocale(locale.LC_ALL, 'de_DE')
            result=now.strftime("Heute ist %A, der %d.%m.%Y (Kalenderwoche: %W)")
            self.say(result)
        elif language == 'fr-FR':
            locale.setlocale(locale.LC_ALL, 'fr_FR')
            result=now.strftime("Il est %A, et nous sommes le %d.%m.%Y (Semaine: %W)")
            self.say(result)
        else:
            locale.setlocale(locale.LC_ALL, 'en_US')
            result=now.strftime("Today is %A the %d.%m.%Y (Week: %W)")
            self.say(result)
        self.complete_request()
