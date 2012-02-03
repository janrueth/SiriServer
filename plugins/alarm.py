#!/usr/bin/python
# -*- coding: utf-8 -*-

import re


from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject
from siriObjects.timerObjects import *


class alarm(Plugin):
    
    localizations = {"setTimer":
                        {"settingTimer":{"en-US": u"Setting the timer\u2026"},
                        "timerWasSet":{"en-US": "Your timer is set."},
                        "timerIsAlreadyRunning":{"en-US": u"It\u2019s already running, :"}},
                    }
                    
    @register("en-US", "(Set.*timer.*)|(for .*)")
    def setTimer(self, speech, language):
        # timerLength = re.match(".*for ([0-9a-z ,]+)$", speech, re.IGNORECASE)
        # if timerLength != None:
        
        
        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [AssistantUtteranceView(text=alarm.localizations['setTimer']['settingTimer'][language], speakableText=alarm.localizations['setTimer']['settingTimer'][language], dialogIdentifier="Timer#settingTimer")]
        self.sendRequestWithoutAnswer(view)
        
        
        # check the current state of the timer
        response = self.getResponseForRequest(TimerGet(self.refId))['properties']['timer']['properties']
        print(type(response), response)
        timer = TimerObject(timerValue = response['timerValue'], state = response['state'])
        
        if timer.state == "Running":
            # timer is already running!
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(text=alarm.localizations['setTimer']['timerIsAlreadyRunning'][language], speakableText=alarm.localizations['setTimer']['timerIsAlreadyRunning'][language], dialogIdentifier="Timer#timerIsAlreadyRunning")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]
            self.sendRequestWithoutAnswer(view)
        else:
            # start a new timer
            timer = TimerObject(timerValue = 120, state = "Running")
            
            response = self.getResponseForRequest(TimerSet(self.refId, timer=timer))
            
            
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(text=alarm.localizations['setTimer']['timerWasSet'][language], speakableText=alarm.localizations['setTimer']['timerWasSet'][language], dialogIdentifier="Timer#timerWasSet")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]
            self.sendRequestWithoutAnswer(view)
            
        
        
        # timerLength = timerLength.group(1).strip()
        # view = AddViews(self.refId, dialogPhase="Summary")
        # view1 = AssistantUtteranceView(text="Setting a timer for %d minutes." % (2), dialogIdentifier="Alarm#setTimer")
        # timer = TimerObject()
        # timer.value = 120
        # timer.state = "Running"
        # view2 = TimerSnippet(timers=[timer])
        # view.views = [view1, view2]
        # self.sendRequestWithoutAnswer(view)
        # else:
        #     self.say("Didn't quite get that.")
        self.complete_request()