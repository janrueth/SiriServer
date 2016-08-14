#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from pprint import pprint as pp

from fractions import Fraction
from datetime import datetime, time, timedelta

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

def parse_alarm_time(t, language):
    if t == 'midnight':
        return (0, 0)
    elif t == 'noon':
        return (12, 0)
    m = re.match(alarmPlugin.res['alarmTime'][language], t, re.IGNORECASE)
    if m:
        hour = int(m.group('hour'))
        if m.group('minute'):
            minute = int(m.group('minute'))
        else:
            minute = 0
        if m.group('qual') == 'pm' and hour < 12:
            hour += 12
        return (hour, minute)


class alarmPlugin(Plugin):
    
    # localizations are sorted by title, fragment, and language, based upon
    # dialogIdentifiers.
    # i.e., for dialogIdentifier 'Alarm#settingAlarm' in en-US, one would
    # access localizations['Alarm']['settingAlarm']['en-US']
    localizations = {
        'Alarm': {
            'alarmConflict': {
                'en-US': 'You already have an alarm set at {}.'
            }, 'alarmTimeWasChanged': {
                'en-US': 'I changed your alarm to {}.'
            }, 'alarmWasSet': {
                'en-US': u'I\u2019ve set an alarm for {}:'
            }, 'changingAlarm': {
                'en-US': u'Updating the alarm\u2026'
            }, 'noAlarmAtThatTime': {
                'en-US': u'There\u2019s no alarm at {}. You do have these, though:'
            }, 'settingAlarm': {
                'en-US': u'Setting the alarm\u2026'
            }
        },
        'timeFormat': {
            'en-US': '%-I:%M %p'
        }
    }

    res = {
        'articles': {
            'en-US': 'a|an|the'
        }, 'alarmLength': {
            'en-US': '.*([0-9/ ]|a|an|the)\s+(mins?|minutes?|hrs?|hours?)'
        }, 'alarmTime': {
            'en-US': '([^0-9]*(?P<hour>[0-9]{1,2}):?\s*(?P<minute>[0-9]{2})?\s*(?P<qual>am|pm)?|noon|midnight)(\s|$)'
        }, 'amClues': {
            'en-US': '.*(am|morning|midnight)'
        }, 'midnightClues': {
            'en-US': '.*(am|midnight)'
        }, 'noonClues': {
            'en-US': '.*(noon)'
        }, 'pmClues': {
            'en-US': '.*(pm|evening|afternoon|[^m][^i][^d]night)'
        }, 'changeAlarm': {
            'en-US': '.*(change|move).*[^0-9]+(?P<time1>([0-9]{1,2}):?\s*([0-9]{2})?\s*(am|pm)?|noon|midnight)\s.*alarm.*[^0-9]+(?P<time2>([0-9]{1,2}):?\s*([0-9]{2})?\s*(am|pm)?|noon|midnight)(\s|$)'
        }, 'setAlarm': {
            'en-US': '.*(wake|set.*alarm).*[^0-9]+((?P<relative>([0-9/ ]*|a|an|the)\s+(mins?|minutes?|hrs?|hours?))|(?P<absolute>([0-9]{1,2}):?\s*([0-9]{2})?\s*(am|pm)?|noon|midnight))(\s|$)'
        }
    }

    @register("en-US", res['setAlarm']['en-US'])
    def setAlarm(self, speech, language):
        m = re.match(self.res['setAlarm'][language], speech, re.IGNORECASE)

        hour = 0
        minute = 0

        if m.group('relative'):
            # person has specified an alarm in relative time ("in 8 hours")
            offset = parse_alarm_length(m.group('relative'), language)
            # target_time = localtime(time() + offset)
            target_time = datetime.now() + timedelta(seconds=offset)
            # TODO: local time selection?
            hour = target_time.hour
            minute = target_time.minute
        elif m.group('absolute'):
            # absolute time ("at 7 a.m.")
            hour, minute = parse_alarm_time(m.group('absolute'), language)
        else:
            # ask what time?
            self.say('Set an alarm for what time?')
            self.complete_request()
            return
        
        target_time = time(hour, minute)
        speakableTime = target_time.strftime(self.localizations['timeFormat'][language])
        
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
    

    @register("en-US", res['changeAlarm']['en-US'])
    def changeAlarm(self, speech, language):
        m = re.match(self.res['changeAlarm'][language], speech, re.IGNORECASE)
        
        time1 = time(*parse_alarm_time(m.group('time1'), language))
        time2 = time(*parse_alarm_time(m.group('time2'), language))
        speakableTime1 = time1.strftime(self.localizations['timeFormat'][language])
        speakableTime2 = time2.strftime(self.localizations['timeFormat'][language])

        response = self.getResponseForRequest(AlarmSearch(refId=self.refId, hour=time1.hour, minute=time1.minute))
        assert(response['class'] == 'SearchCompleted')
        
        results = response['properties']['results']
        self.AddViewsHelper('Alarm#changingAlarm', language, 'Reflection')

        if len(results) == 0:
            # didn't find a matching alarm
            # find ALL the alarms
            response = self.getResponseForRequest(AlarmSearch(refId=self.refId))
            assert(response['class'] == 'SearchCompleted')

            results = response['properties']['results']

            alarms = []
            for r in results:
                alarm = AlarmObject()
                alarm.initWithPList(r)
                alarms += [alarm]

            self.AddViewsHelper('Alarm#noAlarmAtThatTime', language, 'Summary',
                    args=speakableTime1,
                    addlViews=AlarmSnippet(alarms=alarms))

            self.complete_request()
            return

        alarm = AlarmObject()
        alarm.initWithPList(response['properties']['results'][0])

        response = self.getResponseForRequest(AlarmUpdate(self.refId, alarmId=alarm.identifier, hour=time2.hour, minute=time2.minute))
        assert(response['class'] == 'UpdateCompleted')
        
        self.AddViewsHelper('Alarm#alarmTimeWasChanged', language, 'Completion',
                args=speakableTime2,
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

