#!/usr/bin/python
# -*- coding: utf-8 -*-

import re



from parsedatetime.parsedatetime import Calendar
from plugin import *

from time import localtime, mktime

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject
from siriObjects.timerObjects import *


class alarm(Plugin):
    
    localizations = {"setTimer":
                        {"settingTimer":{"en-US": u"Setting a timer for {0}\u2026"},
                        "timerWasSet":{"en-US": "Your timer is set for {0}."},
                        "timerIsAlreadyRunning":{"en-US": u"It\u2019s already running."}},
                        }
                    
    @register("en-US", "(Set.*timer.*)|(for .*)")
    def setTimer(self, speech, language):
        timerLength = re.match(".*for ([0-9a-z ,]+)$", speech, re.IGNORECASE)
        if timerLength != None:
        
            timerLength = timerLength.group(1).strip()
            
            view = AddViews(self.refId, dialogPhase="Reflection")
            view.views = [AssistantUtteranceView(text=alarm.localizations['setTimer']['settingTimer'][language].format(timerLength), speakableText=alarm.localizations['setTimer']['settingTimer'][language].format(timerLength), dialogIdentifier="Timer#settingTimer")]
            self.sendRequestWithoutAnswer(view)
        
        
            # check the current state of the timer

            response = self.getResponseForRequest(TimerGet(self.refId))
            
            print(type(response), response)

            timer_properties = response['properties']['timer']['properties']
            timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])
            
            if timer.state == "Running":
                # timer is already running!
                view = AddViews(self.refId, dialogPhase="Completion")
                view1 = AssistantUtteranceView(text=alarm.localizations['setTimer']['timerIsAlreadyRunning'][language], speakableText=alarm.localizations['setTimer']['timerIsAlreadyRunning'][language], dialogIdentifier="Timer#timerIsAlreadyRunning")
                view2 = TimerSnippet(timers=[timer])
                view.views = [view1, view2]
                self.sendRequestWithoutAnswer(view)
            else:
                c = Calendar()
                now = localtime()
                timer_end = c.parse(timerLength, now)
                timer_length = mktime(timer_end[0]) - mktime(now)

                # start a new timer
                timer = TimerObject(timerValue = timer_length, state = "Running")
                
                response = self.getResponseForRequest(TimerSet(self.refId, timer=timer))
                

                view = AddViews(self.refId, dialogPhase="Completion")
                view1 = AssistantUtteranceView(text=alarm.localizations['setTimer']['timerWasSet'][language].format(timerLength), speakableText=alarm.localizations['setTimer']['timerWasSet'][language].format(timerLength), dialogIdentifier="Timer#timerWasSet")
                view2 = TimerSnippet(timers=[timer])
                view.views = [view1, view2]
                self.sendRequestWithoutAnswer(view)
                
            
            
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
