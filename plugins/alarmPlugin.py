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
    
    # localizations are sorted by title, fragment, and language, based upon
    # dialogIdentifiers.
    # i.e., for dialogIdentifier 'Alarm#settingAlarm' in en-US, one would
    # access localizations['Alarm']['settingAlarm']['en-US']
    localizations = {
        'Alarm': {
            'alarmConflict': {
                'en-US': 'You already have an alarm set at {}.'
            }, 'alarmWasSet': {
                'en-US': u'I\u2019ve set an alarm for {}:'
            }, 'settingAlarm': {
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
        m = re.match(self.res['setAlarm'][language], speech, re.IGNORECASE)

        hour = 0
        minute = 0

        if m.group('relative'):
            # person has specified an alarm in relative time ("in 8 hours")
            offset = parse_alarm_length(m.group('relative'), language)
            target_time = localtime(time() + offset)
            # TODO: local time selection?
            hour = target_time.tm_hour
            minute = target_time.tm_min
        elif m.group('absolute'):
            # relative time ("at 7 a.m.")
            hour = int(m.group('hour'))
            if m.group('minute'):
                minute = int(m.group('minute'))
            else:
                minute = 0
            if hour < 12 and re.match(self.res['pmClues'][language], speech, re.IGNORECASE):
                hour += 12
            elif hour == 12 and re.match(self.res['midnightClues'][language], speech, re.IGNORECASE):
                hour = 0
                print("{0:0=2}:{1:0=2}".format(hour, minute))
        elif re.match(self.res['midnightClues'][language], speech, re.IGNORECASE):
            hour = 0
            minute = 0
        elif re.match(self.res['noonClues'][language], speech, re.IGNORECASE):
            hour = 12
            minute = 0
        else:
            # ask what time?
            self.say('Set an alarm for what time?')
            self.complete_request()
            return

        speakableTime = '{}:{:0<2}'.format(hour, minute)
        
        response = self.getResponseForRequest(AlarmSearch(refId=self.refId, hour=hour, minute=minute))
        assert(response['class'] == 'SearchCompleted')

        results = response['properties']['results']
        if len(results) > 0:
            # found an alarm already
            alarm = AlarmObject()
            alarm.initWithPList(response['properties']['results'][0])

            self.AddViewsHelper('Alarm#alarmConflict', language,
                    'Clarification',
                    args=speakableTime,
                    addlViews=AlarmSnippet(alarms=[alarm]))

            self.complete_request()
            return
        
        self.AddViewsHelper('Alarm#settingAlarm', language, 'Reflection')
        
        alarm = AlarmObject(enabled=True, minute=minute, hour=hour, frequency=['Never'])
        response = self.getResponseForRequest(AlarmCreate(self.refId, alarmToCreate=alarm))
        assert(response['class'] == 'CreateCompleted')
        alarm.identifier = response['properties']['alarmId']

        self.AddViewsHelper('Alarm#alarmWasSet', language, 'Completion',
                args=speakableTime,
                addlViews=AlarmSnippet(alarms=[alarm]))

        self.complete_request()


    def AddViewsHelper(self, dialogIdentifier=None, language='en-US',
                       dialogPhase='Completion', args=None, addlViews=None):
        view = AddViews(self.refId, dialogPhase=dialogPhase)
        if dialogIdentifier:
            title, fragment = dialogIdentifier.split('#')
        
            args = args or []

            if type(args) is not list and type(args) is not dict:
                args = [args]
            
            speakableText = self.localizations[title][fragment][language]

            if type(args) is dict:
                speakableText = speakableText.format(**args)
            else:
                speakableText = speakableText.format(*args)

            view.views += [AssistantUtteranceView(
                            speakableText=speakableText,
                            dialogIdentifier=dialogIdentifier)]

        if addlViews and type(addlViews) is list:
            view.views += addlViews
        elif addlViews:
            view.views += [addlViews]
        
        self.sendRequestWithoutAnswer(view)

