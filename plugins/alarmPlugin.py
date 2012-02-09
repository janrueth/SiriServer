#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from pprint import pprint as pp

from fractions import Fraction
from time import localtime, time

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject
from siriObjects.alarmObjects import *


def parse_number(s, language):
    # check for simple article usage (a, an, the)
    if re.match(alarmPlugin.res['articles'][language], s, re.IGNORECASE):
        return 1
    f = 0
    for part in s.split(' '):
        f += float(Fraction(part))
    return f


def parse_alarm_length(t, language):
    m = re.search(alarmPlugin.res['alarmLength'][language], t, re.IGNORECASE)
    if m:
        unit = m.group(2)[0]
        count = parse_number(m.group(1), language)
        if unit == 'h':
            return count * 60 * 60
        elif unit == 'm':
            return count * 60
        else:
            # shouldn't ever get here, but just in case...
            return count * 60


class alarmPlugin(Plugin):

    localizations = {
        'Alarm': {
            'settingAlarm': {
               'en-US': u'Setting the alarm\u2026'
            }
        }
    }

    res = {
        'articles': {
            'en-US': 'a|an|the'
        }, 'alarmLength': {
            'en-US': '.*([0-9/ ]|a|an|the)\s+(mins?|minutes?|hrs?|hours?)'
        }, 'alarmTime': {
            'en-US': '.*(?P<hour>2[0-3]|1[0-9]|0?[0-9]):?\s*(?P<minute>[0-5][0-9])?\s*($|[^0-9])'
        }, 'amClues': {
            'en-US': '.*(am|morning|midnight)'
        }, 'midnightClues': {
            'en-US': '.*(am|midnight)'
        }, 'noonClues': {
            'en-US': '.*(noon)'
        }, 'pmClues': {
            'en-US': '.*(pm|evening|afternoon|[^m][^i][^d]night)'
        }, 'setAlarm': {
            'en-US': '.*(wake|set.*alarm).*\s+((?P<relative>([0-9/ ]*|a|an|the)\s+(mins?|minutes?|hrs?|hours?))|(?P<absolute>(?P<hour>2[0-3]|1[0-9]|0?[0-9]):?\s*(?P<minute>[0-5][0-9])?\s*($|[^0-9])))'
        }
    }

    title = 'Alarm'

    @register("en-US", res['setAlarm']['en-US'])
    def setAlarm(self, speech, language):
        #relative_m = re.match(alarmPlugin.res['alarmLength'][language], speech, re.IGNORECASE)
        #absolute_m = re.match(alarmPlugin.res['alarmTime'][language], speech, re.IGNORECASE)
        m = re.match(alarmPlugin.res['setAlarm'][language], speech, re.IGNORECASE)

        hour = 0
        minute = 0

        if m.group('relative'):
            # person has specified an alarm in relative time ("in 8 hours")
            offset = parse_alarm_length(m.group('relative'), language)
            target_time = localtime(time() + offset)
            # TODO: local time selection?
            hour = target_time.tm_hour
            minute = target_time.tm_min
            pass
        elif m.group('absolute'):
            # relative time ("at 7 a.m.")
            hour = int(m.group('hour'))
            if m.group('minute'):
                minute = int(m.group('minute'))
            else:
                minute = 0
            pass
        else:
            # ask what time?
            self.say('Set an alarm for what time?')
            self.complete_request()
            return

        self.say('set an alarm for {}:{}'.format(hour, minute))
        
        response = self.getResponseForRequest(AlarmSearch(refId=self.refId, hour=hour, minute=minute))
        pp(response)
        assert(response['class'] == 'SearchCompleted')

        results = response['properties']['results']
        if len(results) > 0:
            # found an alarm already
            # TODO: handle it
            return
        
        self.reflect('settingAlarm', language)

        self.complete_request()


    def reflect(self, fragment, language):
        view = AddViews(self.refId, dialogPhase='Reflection')
        view.views = [
            AssistantUtteranceView(
                speakableText=self.localizations[self.title][fragment][language],
                dialogIdentifier='{}#{}'.format(self.title, fragment)
            )
        ]
        self.sendRequestWithoutAnswer(view)

#        m = re.match(timerPlugin.res['setTimer'][language], speech, re.IGNORECASE)
#        timer_length = ' '.join(m.group(1, 2))
#        duration = parse_timer_length(timer_length, language)
#
#        view = AddViews(self.refId, dialogPhase="Reflection")
#        view.views = [
#            AssistantUtteranceView(
#                speakableText=timerPlugin.localizations['Timer']['settingTimer'][language],
#                dialogIdentifier="Timer#settingTimer")]
#        self.sendRequestWithoutAnswer(view)
#
#        # check the current state of the timer
#        response = self.getResponseForRequest(TimerGet(self.refId))
#        if response['class'] == 'CancelRequest':
#            self.complete_request()
#            return
#        timer_properties = response['properties']['timer']['properties']
#        timer = TimerObject(timerValue=timer_properties['timerValue'],
#                state=timer_properties['state'])
#
#        if timer.state == "Running":
#            # timer is already running!
#            view = AddViews(self.refId, dialogPhase="Completion")
#            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyRunning'][language], dialogIdentifier="Timer#timerIsAlreadyRunning")
#            view2 = TimerSnippet(timers=[timer], confirm=True)
#            view.views = [view1, view2]
#            utterance = self.getResponseForRequest(view)
#            #if response['class'] == 'StartRequest':
#            view = AddViews(self.refId, dialogPhase="Reflection")
#            view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['settingTimer'][language], dialogIdentifier="Timer#settingTimer")]
#            self.sendRequestWithoutAnswer(view)
#
#            if re.match('\^timerConfirmation\^=\^no\^', utterance):
#                # user canceled
#                view = AddViews(self.refId, dialogPhase="Completion")
#                view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['wontSetTimer'][language], dialogIdentifier="Timer#wontSetTimer")]
#                self.sendRequestWithoutAnswer(view)
#                self.complete_request()
#                return
#            else:
#                # user wants to set the timer still - continue on
#                pass
#
#        if duration > 24 * 60 * 60:
#            view = AddViews(self.refId, dialogPhase='Clarification')
#            view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['durationTooBig'][language], dialogIdentifier='Timer#durationTooBig')]
#            self.sendRequestWithoutAnswer(view)
#            self.complete_request()
#            return
#
#        # start a new timer
#        timer = TimerObject(timerValue = duration, state = "Running")
#        response = self.getResponseForRequest(TimerSet(self.refId, timer=timer))
#        
#        print(timerPlugin.localizations['Timer']['timerWasSet'][language].format(timer_length))
#        view = AddViews(self.refId, dialogPhase="Completion")
#        view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasSet'][language].format(timer_length), dialogIdentifier="Timer#timerWasSet")
#        view2 = TimerSnippet(timers=[timer])
#        view.views = [view1, view2]
#        self.sendRequestWithoutAnswer(view)
#        self.complete_request()
#
#    @register("en-US", res['resetTimer']['en-US'])
#    def resetTimer(self, speech, language):
#        response = self.getResponseForRequest(TimerGet(self.refId))
#        timer_properties = response['properties']['timer']['properties']
#        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])
#
#        if timer.state == "Running" or timer.state == 'Paused':
#            response = self.getResponseForRequest(TimerCancel(self.refId))
#            if response['class'] == "CancelCompleted":
#                view = AddViews(self.refId, dialogPhase="Completion")
#                view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasReset'][language], dialogIdentifier="Timer#timerWasReset")]
#                self.sendRequestWithoutAnswer(view)
#            self.complete_request()
#        else:
#            view = AddViews(self.refId, dialogPhase="Completion")
#            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
#            view2 = TimerSnippet(timers=[timer])
#            view.views = [view1, view2]
#
#            self.sendRequestWithoutAnswer(view)
#            self.complete_request()
#
#    @register("en-US", res['resumeTimer']['en-US'])
#    def resumeTimer(self, speech, language):
#        response = self.getResponseForRequest(TimerGet(self.refId))
#        timer_properties = response['properties']['timer']['properties']
#        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])
#
#        if timer.state == "Paused":
#            response = self.getResponseForRequest(TimerResume(self.refId))
#            if response['class'] == "ResumeCompleted":
#                view = AddViews(self.refId, dialogPhase="Completion")
#                view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasResumed'][language], dialogIdentifier="Timer#timerWasResumed")
#                view2 = TimerSnippet(timers=[timer])
#                view.views = [view1, view2]
#                self.sendRequestWithoutAnswer(view)
#            self.complete_request()
#        else:
#            view = AddViews(self.refId, dialogPhase="Completion")
#            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
#            view2 = TimerSnippet(timers=[timer])
#            view.views = [view1, view2]
#
#            self.sendRequestWithoutAnswer(view)
#            self.complete_request()
#
#    @register("en-US", res['pauseTimer']['en-US'])
#    def pauseTimer(self, speech, language):
#        response = self.getResponseForRequest(TimerGet(self.refId))
#        timer_properties = response['properties']['timer']['properties']
#        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])
#
#        if timer.state == "Running":
#            response = self.getResponseForRequest(TimerPause(self.refId))
#            if response['class'] == "PauseCompleted":
#                view = AddViews(self.refId, dialogPhase="Completion")
#                view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasPaused'][language], dialogIdentifier="Timer#timerWasPaused")]
#                self.sendRequestWithoutAnswer(view)
#            self.complete_request()
#        elif timer.state == "Paused":
#            view = AddViews(self.refId, dialogPhase="Completion")
#            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyPaused'][language], dialogIdentifier="Timer#timerIsAlreadyPaused")
#            view2 = TimerSnippet(timers=[timer])
#            view.views = [view1, view2]
#
#            self.sendRequestWithoutAnswer(view)
#            self.complete_request()
#        else:
#            view = AddViews(self.refId, dialogPhase="Completion")
#            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
#            view2 = TimerSnippet(timers=[timer])
#            view.views = [view1, view2]
#
#            self.sendRequestWithoutAnswer(view)
#            self.complete_request()
#
#    @register("en-US", res['showTimer']['en-US'])
#    def showTimer(self, speech, language):
#        response = self.getResponseForRequest(TimerGet(self.refId))
#        timer_properties = response['properties']['timer']['properties']
#        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])
#
#        view = AddViews(self.refId, dialogPhase="Summary")
#        view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['showTheTimer'][language], dialogIdentifier="Timer#showTheTimer")
#        view2 = TimerSnippet(timers=[timer])
#        view.views = [view1, view2]
#        self.sendRequestWithoutAnswer(view)
#        self.complete_request()
