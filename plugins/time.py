#!/usr/bin/python
# -*- coding: utf-8 -*-


from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject

class ClockSnippet(AceObject):
    def __init__(self, clocks=None):
        super(ClockSnippet, self).__init__("Snippet", "com.apple.ace.clock")
        self.clocks = clocks if clocks != None else []

    def to_plist(self):
        self.add_property('clocks')
        return super(ClockSnippet, self).to_plist()

class ClockObject(DomainObject):
    def __init__(self):
        super(ClockObject, self).__init__("com.apple.ace.clock")
        self.unlocalizedCountryName = None
        self.unlocalizedCityName = None
        self.timezoneId = None
        self.countryName = None
        self.countryCode = None
        self.cityName = None
        self.alCityId = None
    
    def to_plist(self):
        self.add_property('unlocalizedCountryName')
        self.add_property('unlocalizedCityName')
        self.add_property('timezoneId') 
        self.add_property('countryName')
        self.add_property('countryCode')
        self.add_property('cityName')
        self.add_property('alCityId')
        return super(ClockObject, self).to_plist()

class time(Plugin):
    
    localizations = {"currentTime": {"search":{"de-DE": "Es wird gesucht ...", "en-US": "Looking up ..."}, "currentTime": {"de-DE": "Es ist @{fn#currentTime}", "en-US": "It is @{fn#currentTime}"}}}

    @register("de-DE", "(Wieviel Uhr.*)|(.*Uhrzeit.*)")
    @register("en-US", "(What time.*)|(.*current time.*)")
    def currentTime(self, speech, language):
        #first tell that we look it up
        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [AssistantUtteranceView(text=time.localizations['currentTime']['search'][language], speakableText=time.localizations['currentTime']['search'][language], dialogIdentifier="Clock#getTime")]
        self.sendRequestWithoutAnswer(view)
        
        # tell him to show the current time
        view = AddViews(self.refId, dialogPhase="Summary")
        view1 = AssistantUtteranceView(text=time.localizations['currentTime']['currentTime'][language], speakableText=time.localizations['currentTime']['currentTime'][language], dialogIdentifier="Clock#showTimeInCurrentLocation")
        clock = ClockObject()
        clock.timezoneId = self.connection.assistant.timeZoneId
        view2 = ClockSnippet(clocks=[clock])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()

