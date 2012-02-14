#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from fractions import Fraction

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject
from siriObjects.timerObjects import *


def parse_number(s, language):
    # check for simple article usage (a, an, the)
    if re.match(timerPlugin.res['articles'][language], s, re.IGNORECASE):
        return 1
    f = 0
    for part in s.split(' '):
        f += float(Fraction(part))
    return f


def parse_timer_length(t, language):
    m = re.search(timerPlugin.res['timerLength'][language], t, re.IGNORECASE)
    if m:
        unit = m.group(2)[0]
        count = parse_number(m.group(1), language)
        if unit == 'h':
            return count * 60 * 60
        elif unit == 'm':
            return count * 60
        elif unit == 's':
            return count
        else:
            # shouldn't ever get here, but just in case...
            return count * 60


class timerPlugin(Plugin):

    localizations = {
        'Timer': {
<<<<<<< HEAD
            'durationTooBig': {
               'en-US': 'Sorry, I can only set timers up to 24 hours.', 'fr-FR': u"Désolé mais je ne peux pas programmer le minuteur plus de 24 heures."
            }, "settingTimer": {
                "en-US": u"Setting the timer\u2026", "fr-FR": u"Programmation du minuteur"
            }, 'showTheTimer': {
                'en-US': u'Here\u2019s the timer:', "fr-FR": u"Voici le minuteur"
            }, 'timerIsAlreadyPaused': {
                'en-US': u'It\u2019s already paused.', "fr-FR": u"Le minuteur est déjà en pause !"
            }, "timerIsAlreadyRunning": {
                "en-US": u"Your timer\u2019s already running:", "fr-FR": u"Un minuteur est déjà en cours"
            }, 'timerIsAlreadyStopped': {
                'en-US': u'It\u2019s already stopped.', "fr-FR": u"Le minuteur est déjà arrếté !"
            }, 'timerWasPaused': {
                'en-US': u'It\u2019s paused.', "fr-FR": u"Le minuteur est en pause."
            }, 'timerWasReset': {
                'en-US': u'I\u2019ve canceled the timer.'
            }, 'timerWasResumed': {
                'en-US': u'It\u2019s resumed.', "fr-FR": u"Le minuteur a repris."
            }, "timerWasSet": {
                "en-US": "Your timer is set for {0}.", "fr-FR": u"Votre minuteur est programmé pour {0}"
            }, "wontSetTimer": {
                "en-US": "OK.", "fr-FR": u"D'accord"
=======
            "settingTimer": {
                "en-US": u"Setting the timer\u2026", "fr-FR": u"Programmation du minuteur"
            }, "timerWasSet": {
                "en-US": "Your timer is set for {0}.", "fr-FR": u"Votre minuteur est programmé pour {0}"
            }, "timerIsAlreadyRunning": {
                "en-US": u"Your timer\u2019s already running:", "fr-FR": u"Un minuteur est déjà en cours"
            }, "wontSetTimer": {
                "en-US": "OK.", "fr-FR": u"D'accord"
            }, 'timerWasReset': {
                'en-US': u'I\u2019ve canceled the timer.', "fr-FR": u"J'ai annulé le minuteur."
            }, 'timerIsAlreadyStopped': {
                'en-US': u'It\u2019s already stopped.', "fr-FR": u"Le minuteur est déjà arrếté !"
            }, 'timerWasResumed': {
                'en-US': u'It\u2019s resumed.', "fr-FR": u"Le minuteur a repris."
            }, 'timerWasPaused': {
                'en-US': u'It\u2019s paused.', "fr-FR": u"Le minuteur est en pause."
            }, 'timerIsAlreadyPaused': {
                'en-US': u'It\u2019s already paused.', "fr-FR": u"Le minuteur est déjà en pause !"
            }, 'showTheTimer': {
                'en-US': u'Here\u2019s the timer:', "fr-FR": u"Voici le minuteur"
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
            }
        }
    }

    res = {
<<<<<<< HEAD
        'articles': {
            'en-US': 'a|an|the', 'fr-FR': 'une|pour'
        }, 'pauseTimer': {
            'en-US': '.*(pause|freeze|hold).*timer', 'fr-FR': '(.*pause.*minuteur.*)|(.*minuteur.*pause.*)'
=======
        'setTimer': {
            'en-US': '.*timer.*\s+([0-9/ ]*|a|an|the)\s+(secs?|seconds?|mins?|minutes?|hrs?|hours?)', 'fr-FR': '.*minuteur.*\s+([0-9/ ]*|une|deux|trois|quatre|cinq|six|sept|huit|neuf)\s+(secondes?|minutes?|heures?)'
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
        }, 'resetTimer': {
            'en-US': '.*(cancel|reset|stop).*timer', 'fr-FR': u'.*(annule|déprogramme).*minuteur'
        }, 'resumeTimer': {
            'en-US': '.*(resume|thaw|continue).*timer', 'fr-FR': '.*(reprends|continue|remets).*minuteur'
<<<<<<< HEAD
        }, 'setTimer': {
            'en-US': '.*timer.*\s+([0-9/ ]*|a|an|the)\s+(secs?|seconds?|mins?|minutes?|hrs?|hours?)', 'fr-FR': '.*minuteur.*\s+([0-9/ ]*|une|deux|trois|quatre|cinq|six|sept|huit|neuf)\s+(secondes?|minutes?|heures?)'
=======
        }, 'pauseTimer': {
            'en-US': '.*(pause|freeze|hold).*timer', 'fr-FR': '(.*pause.*minuteur.*)|(.*minuteur.*pause.*)'
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
        }, 'showTimer': {
            'en-US': '.*(show|display|see).*timer', 'fr-FR': '.*montre.*minuteur'
        }, 'timerLength': {
            'en-US': '([0-9/ ]*|a|an|the)\s+(secs?|seconds?|mins?|minutes?|hrs?|hours?)', 'fr-FR': '([0-9/ ]*|une|deux|trois|quatre|cinq|six|sept|huit|neuf)\s+(secondes?|minutes?|heures?)'
<<<<<<< HEAD
=======
        }, 'articles': {
            'en-US': 'a|an|the', 'fr-FR': 'un|une|pour'
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
        }
    }

    @register("en-US", res['setTimer']['en-US'])
    @register("fr-FR", res['setTimer']['fr-FR'])
    def setTimer(self, speech, language):
        m = re.match(timerPlugin.res['setTimer'][language], speech, re.IGNORECASE)
        timer_length = ' '.join(m.group(1, 2))
        duration = parse_timer_length(timer_length, language)

        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [
            AssistantUtteranceView(
                speakableText=timerPlugin.localizations['Timer']['settingTimer'][language],
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
            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyRunning'][language], dialogIdentifier="Timer#timerIsAlreadyRunning")
            view2 = TimerSnippet(timers=[timer], confirm=True)
            view.views = [view1, view2]
            utterance = self.getResponseForRequest(view)
            #if response['class'] == 'StartRequest':
            view = AddViews(self.refId, dialogPhase="Reflection")
            view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['settingTimer'][language], dialogIdentifier="Timer#settingTimer")]
            self.sendRequestWithoutAnswer(view)

            if re.match('\^timerConfirmation\^=\^no\^', utterance):
                # user canceled
                view = AddViews(self.refId, dialogPhase="Completion")
                view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['wontSetTimer'][language], dialogIdentifier="Timer#wontSetTimer")]
                self.sendRequestWithoutAnswer(view)
                self.complete_request()
                return
            else:
                # user wants to set the timer still - continue on
                pass

        if duration > 24 * 60 * 60:
            view = AddViews(self.refId, dialogPhase='Clarification')
            view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['durationTooBig'][language], dialogIdentifier='Timer#durationTooBig')]
            self.sendRequestWithoutAnswer(view)
            self.complete_request()
            return

        # start a new timer
        timer = TimerObject(timerValue = duration, state = "Running")
        response = self.getResponseForRequest(TimerSet(self.refId, timer=timer))
        
        print(timerPlugin.localizations['Timer']['timerWasSet'][language].format(timer_length))
        view = AddViews(self.refId, dialogPhase="Completion")
        view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasSet'][language].format(timer_length), dialogIdentifier="Timer#timerWasSet")
        view2 = TimerSnippet(timers=[timer])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()

    @register("en-US", res['resetTimer']['en-US'])
    @register("fr-FR", res['resetTimer']['fr-FR'])
    def resetTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        if timer.state == "Running" or timer.state == 'Paused':
            response = self.getResponseForRequest(TimerCancel(self.refId))
            if response['class'] == "CancelCompleted":
                view = AddViews(self.refId, dialogPhase="Completion")
                view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasReset'][language], dialogIdentifier="Timer#timerWasReset")]
                self.sendRequestWithoutAnswer(view)
            self.complete_request()
        else:
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()

    @register("en-US", res['resumeTimer']['en-US'])
    @register("fr-FR", res['resumeTimer']['fr-FR'])
    def resumeTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        if timer.state == "Paused":
            response = self.getResponseForRequest(TimerResume(self.refId))
            if response['class'] == "ResumeCompleted":
                view = AddViews(self.refId, dialogPhase="Completion")
                view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasResumed'][language], dialogIdentifier="Timer#timerWasResumed")
                view2 = TimerSnippet(timers=[timer])
                view.views = [view1, view2]
                self.sendRequestWithoutAnswer(view)
            self.complete_request()
        else:
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()

    @register("en-US", res['pauseTimer']['en-US'])
    @register("fr-FR", res['pauseTimer']['fr-FR'])
    def pauseTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        if timer.state == "Running":
            response = self.getResponseForRequest(TimerPause(self.refId))
            if response['class'] == "PauseCompleted":
                view = AddViews(self.refId, dialogPhase="Completion")
                view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasPaused'][language], dialogIdentifier="Timer#timerWasPaused")]
                self.sendRequestWithoutAnswer(view)
            self.complete_request()
        elif timer.state == "Paused":
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyPaused'][language], dialogIdentifier="Timer#timerIsAlreadyPaused")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()
        else:
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()

    @register("en-US", res['showTimer']['en-US'])
    @register("fr-FR", res['showTimer']['fr-FR'])
    def showTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        view = AddViews(self.refId, dialogPhase="Summary")
        view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['showTheTimer'][language], dialogIdentifier="Timer#showTheTimer")
        view2 = TimerSnippet(timers=[timer])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()
