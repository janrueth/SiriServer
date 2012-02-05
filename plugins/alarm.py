#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from fractions import Fraction

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject
from siriObjects.timerObjects import *


def parse_number(s):
    # check for simple article usage (a, an, the)
    if re.match('a|an|the', s):
        return 1
    f = 0
    for part in s.split(' '):
        f += float(Fraction(part))
    return f


def parse_timer_length(t):
    m = re.search(alarm.res['timerLength'], t, re.IGNORECASE)
    if m:
        unit = m.group(2)[0]
        count = parse_number(m.group(1))
        if unit == 'h':
            return count * 60 * 60
        elif unit == 'm':
            return count * 60
        elif unit == 's':
            return count
        else:
            # shouldn't ever get here, but just in case...
            return count * 60


class alarm(Plugin):

    localizations = {
        'setTimer': {
            "settingTimer": {
                "en-US": u"Setting the timer\u2026"
            }, "timerWasSet": {
                "en-US": "Your timer is set for {0}."
            }, "timerIsAlreadyRunning": {
                "en-US": u"Your timer\u2019s already running:"
            }
        }, 'resetTimer': {
            'timerWasReset': {
                'en-US': u'I\u2019ve canceled the timer.'
            }, 'timerIsAlreadyStopped': {
                'en-US': u'It\u2019s already stopped.'
            }
        }, 'resumeTimer': {
            'timerWasResumed': {
                'en-US': u'It\u2019s resumed.'
            }
        }, 'pauseTimer': {
            'timerWasPaused': {
                'en-US': u'It\u2019s paused.'
            }, 'timerIsAlreadyPaused': {
                'en-US': u'It\u2019s already paused.'
            }
        }, 'showTimer': {
            'showTheTimer': {
                'en-US': u'Here\u2019s the timer:'
            }
        }
    }

    res = {
        'setTimer': '.*timer.*\s+([0-9/ ]*|a|an|the)\s+'
                    '(secs?|seconds?|mins?|minutes?|hrs?|hours?)',
            'resetTimer': '.*(cancel|reset|stop).*timer',
            'resumeTimer': '.*(resume|unfreeze|continue).*timer',
            'pauseTimer': '.*(pause|freeze|hold).*timer',
            'showTimer': '.*show.*timer',
            'timerLength': '([0-9/ ]*|a|an|the)\s+'
                           '(secs?|seconds?|mins?|minutes?|hrs?|hours?)'
    }

    @register("en-US", res['setTimer'])
    def setTimer(self, speech, language):
        m = re.match(alarm.res['setTimer'], speech, re.IGNORECASE)
        timer_length = ' '.join(m.group(1, 2))
        duration = parse_timer_length(timer_length)

        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [
            AssistantUtteranceView(
                speakableText=alarm.localizations['setTimer']['settingTimer'][language],
                dialogIdentifier="Timer#settingTimer")]
        self.sendRequestWithoutAnswer(view)

        # check the current state of the timer
        response = self.getResponseForRequest(TimerGet(self.refId))
        if response['class'] == 'CancelRequest':
            self.complete_request()
            return
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue=timer_properties['timerValue'],
                state=timer_properties['state'])

        if timer.state == "Running":
            # timer is already running!
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=alarm.localizations['setTimer']['timerIsAlreadyRunning'][language], dialogIdentifier="Timer#timerIsAlreadyRunning")
            view2 = TimerSnippet(timers=[timer], confirm=True)
            view.views = [view1, view2]
            # self.sendRequestWithoutAnswer(view)
            # self.complete_request()
            response = self.getResponseForRequest(view)

            # currently freezing springboard if response is handled
            # TODO: fix this
            self.complete_request()
            return

            # utterance = response['properties']['utterance']
            # if re.match('\^timerConfirmation\^=\^yes\^', utterance):
                # view = AddViews(self.refId, dialogPhase="Reflection")
                # view.views = [AssistantUtteranceView(speakableText=alarm.localizations['setTimer']['settingTimer'][language], dialogIdentifier="Timer#settingTimer")]
                # self.sendRequestWithoutAnswer(view)
                # continue on below
            # else:
                # user canceled - complete the request and get out
                # self.complete_request()
                # return

        # start a new timer
        timer = TimerObject(timerValue = duration, state = "Running")
        response = self.getResponseForRequest(TimerSet(self.refId, timer=timer))
        
        print(alarm.localizations['setTimer']['timerWasSet'][language].format(timer_length))
        view = AddViews(self.refId, dialogPhase="Completion")
        view1 = AssistantUtteranceView(speakableText=alarm.localizations['setTimer']['timerWasSet'][language].format(timer_length), dialogIdentifier="Timer#timerWasSet")
        view2 = TimerSnippet(timers=[timer])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
    
        self.complete_request()

    @register("en-US", res['resetTimer'])
    def resetTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        if timer.state == "Running" or timer.state == 'Paused':
            response = self.getResponseForRequest(TimerCancel(self.refId))
            if response['class'] == "CancelCompleted":
                view = AddViews(self.refId, dialogPhase="Completion")
                view.views = [AssistantUtteranceView(speakableText=alarm.localizations['resetTimer']['timerWasReset'][language], dialogIdentifier="Timer#timerWasReset")]
                self.sendRequestWithoutAnswer(view)
            self.complete_request()
        else:
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=alarm.localizations['resetTimer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()

    @register("en-US", res['resumeTimer'])
    def resetTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        if timer.state == "Paused":
            response = self.getResponseForRequest(TimerResume(self.refId))
            if response['class'] == "ResumeCompleted":
                view = AddViews(self.refId, dialogPhase="Completion")
                view1 = [AssistantUtteranceView(speakableText=alarm.localizations['resumeTimer']['timerWasResumed'][language], dialogIdentifier="Timer#timerWasResumed")]
                view2 = TimerSnippet(timers=[timer])
                view.views = [view1, view2]
                self.sendRequestWithoutAnswer(view)
            self.complete_request()
        else:
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=alarm.localizations['resetTimer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()

    @register("en-US", res['pauseTimer'])
    def resetTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        if timer.state == "Running":
            response = self.getResponseForRequest(TimerPause(self.refId))
            if response['class'] == "PauseCompleted":
                view = AddViews(self.refId, dialogPhase="Completion")
                view.views = [AssistantUtteranceView(speakableText=alarm.localizations['pauseTimer']['timerWasPaused'][language], dialogIdentifier="Timer#timerWasPaused")]
                self.sendRequestWithoutAnswer(view)
            self.complete_request()
        elif timer.state == "Paused":
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=alarm.localizations['pauseTimer']['timerIsAlreadyPaused'][language], dialogIdentifier="Timer#timerIsAlreadyPaused")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()
        else:
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=alarm.localizations['resetTimer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()


    @register("en-US", res['showTimer'])
    def showTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        view = AddViews(self.refId, dialogPhase="Completion")
        view1 = [AssistantUtteranceView(speakableText=alarm.localizations['showTimer']['showTheTimer'][language], dialogIdentifier="Timer#showTheTimer")]
        view2 = TimerSnippet(timers=[timer])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()
