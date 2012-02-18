#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2, urllib
import json

from plugin import *

from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.clockObjects import ClockSnippet, ClockObject

####### geonames.org API username ######
geonames_user="test2"

class timePlugin(Plugin):
    
    localizations = {"currentTime": 
                        {"search":{"de-DE": "Es wird gesucht ...", "en-US": "Looking up ...", "fr-FR": "Je cherche..."}, 
                         "currentTime": {"de-DE": "Es ist @{fn#currentTime}", "en-US": "It is @{fn#currentTime}", "fr-FR": u"Il est @{fn#currentTime}"}}, 
                     "currentTimeIn": 
                        {"search":{"de-DE": "Es wird gesucht ...", "en-US": "Looking up ...", "fr-FR": "Je cherche..."}, 
                         "currentTimeIn": 
                                {
                                "tts": {"de-DE": u"Die Uhrzeit in {0},{1} ist @{{fn#currentTimeIn#{2}}}:", "en-US": "The time in {0},{1} is @{{fn#currentTimeIn#{2}}}:", "fr-FR": u"A {0},{1}, il est @{{fn#currentTimeIn#{2}}}:"},
                                "text": {"de-DE": u"Die Uhrzeit in {0}, {1} ist @{{fn#currentTimeIn#{2}}}:", "en-US": "The time in {0}, {1} is @{{fn#currentTimeIn#{2}}}:", "fr-FR":u"A {0}, {1}, il est @{{fn#currentTimeIn#{2}}}:"}
                                }
                        },
                    "failure": {
                                "de-DE": "Ich kann dir die Uhr gerade nicht anzeigen!", "en-US": "I cannot show you the clock right now", "fr-FR": u"Désolé, j'ai perdu ma montre."
                                }
                    }

    @register("de-DE", "(Wie ?viel Uhr.*)|(.*Uhrzeit.*)")     
    @register("en-US", "(What.*time.*)|(.*current time.*)")
    @register("fr-FR", "(.*Quel.*heure.*)|(.*heure actuelle.*)")
    def currentTime(self, speech, language):
        #first tell that we look it up
        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [AssistantUtteranceView(text=timePlugin.localizations['currentTime']['search'][language], speakableText=timePlugin.localizations['currentTime']['search'][language], dialogIdentifier="Clock#getTime")]
        self.sendRequestWithoutAnswer(view)
        
        # tell him to show the current time
        view = AddViews(self.refId, dialogPhase="Summary")
        view1 = AssistantUtteranceView(text=timePlugin.localizations['currentTime']['currentTime'][language], speakableText=timePlugin.localizations['currentTime']['currentTime'][language], dialogIdentifier="Clock#showTimeInCurrentLocation")
        clock = ClockObject()
        clock.timezoneId = self.connection.assistant.timeZoneId
        view2 = ClockSnippet(clocks=[clock])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()
    
    @register("de-DE", "(Wieviel Uhr.*in ([\w ]+))|(Uhrzeit.*in ([\w ]+))")
    @register("en-US", "(What.*time.*in ([\w ]+))|(.*current time.*in ([\w ]+))")
    @register("fr-FR", u"(Quel.*heure.*(à|a|en) ([\w ]+))|(.*heure actuelle.*(à|a|en) ([\w ]+))")
    def currentTimeIn(self, speech, language):
        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [AssistantUtteranceView(text=timePlugin.localizations['currentTimeIn']['search'][language], speakableText=timePlugin.localizations['currentTimeIn']['search'][language], dialogIdentifier="Clock#getTime")]
        self.sendRequestWithoutAnswer(view)
        
        error = False
        countryOrCity = re.match(u"(?u).* (in|a|à|en) ([\w ]+)$", speech, re.IGNORECASE)
        if countryOrCity != None:
            countryOrCity = countryOrCity.group(countryOrCity.lastindex).strip()
            # lets see what we got, a country or a city... 
            # lets use google geocoding API for that
            url = u"http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false&language={1}".format(urllib.quote_plus(countryOrCity.encode("utf-8")), language)
            # lets wait max 3 seconds
            jsonString = None
            try:
                jsonString = urllib2.urlopen(url, timeout=3).read()
            except:
                pass
            if jsonString != None:
                response = json.loads(jsonString)
                # lets see what we have...
                if response['status'] == 'OK':
                    components = response['results'][0]['address_components']
                    types = components[0]['types'] # <- this should be the city or country
                    if "country" in types:
                        # OK we have a country as input, that sucks, we need the capital, lets try again and ask for capital also
                        components = filter(lambda x: True if "country" in x['types'] else False, components)
                        url = u"http://maps.googleapis.com/maps/api/geocode/json?address=capital%20{0}&sensor=false&language={1}".format(urllib.quote_plus(components[0]['long_name'].encode("utf-8")), language)
                            # lets wait max 3 seconds
                        jsonString = None
                        try:
                            jsonString = urllib2.urlopen(url, timeout=3).read()
                        except:
                            pass
                        if jsonString != None:
                            response = json.loads(jsonString)
                            if response['status'] == 'OK':
                                components = response['results'][0]['address_components']
                # response could have changed, lets check again, but it should be a city by now 
                if response['status'] == 'OK':
                    # get latitude and longitude
                    location = response['results'][0]['geometry']['location']
                    url = u"http://api.geonames.org/timezoneJSON?lat={0}&lng={1}&username={2}".format(location['lat'], location['lng'], geonames_user)
                    jsonString = None
                    try:
                        jsonString = urllib2.urlopen(url, timeout=3).read()
                    except:
                        pass
                    if jsonString != None:
                        timeZoneResponse = json.loads(jsonString)
                        if "timezoneId" in timeZoneResponse:
                            timeZone = timeZoneResponse['timezoneId']
                            city = filter(lambda x: True if "locality" in x['types'] or "administrative_area_level_1" in x['types'] else False, components)[0]['long_name']
                            country = filter(lambda x: True if "country" in x['types'] else False, components)[0]['long_name']
                            countryCode = filter(lambda x: True if "country" in x['types'] else False, components)[0]['short_name']
                            
                            view = AddViews(self.refId, dialogPhase="Summary")
                            view1 = AssistantUtteranceView(text=timePlugin.localizations['currentTimeIn']['currentTimeIn']['text'][language].format(city, country, timeZone), speakableText=timePlugin.localizations['currentTimeIn']['currentTimeIn']['tts'][language].format(city, country, timeZone), dialogIdentifier="Clock#showTimeInOtherLocation")
                            clock = ClockObject()
                            clock.timezoneId = timeZone
                            clock.countryCode = countryCode
                            clock.countryName = country
                            clock.cityName = city
                            clock.unlocalizedCityName = city
                            clock.unlocalizedCountryName = country
                            view2 = ClockSnippet(clocks=[clock])
                            view.views = [view1, view2]
                            self.sendRequestWithoutAnswer(view)
                        else:
                            error = True
                    else:
                        error = True
                else:
                    error = True
            else:
                error = True
        else:
            error = True
        if error:
            view = AddViews(self.refId, dialogPhase="Completion")
            view.views = [AssistantUtteranceView(text=timePlugin.localizations['failure'][language], speakableText=timePlugin.localizations['failure'][language], dialogIdentifier="Clock#cannotShowClocks")]
            self.sendRequestWithoutAnswer(view)
        self.complete_request()


## we should implement such a command if we cannot get the location however some structures are not implemented yet
#{"class"=>"AddViews",
#    "properties"=>
#        {"temporary"=>false,
#            "dialogPhase"=>"Summary",
#            "scrollToTop"=>false,
#            "views"=>
#                [{"class"=>"AssistantUtteranceView",
#                 "properties"=>
#                 {"dialogIdentifier"=>"Common#unresolvedExplicitLocation",
#                 "speakableText"=>
#                 "Ich weiß leider nicht, wo das ist. Wenn du möchtest, kann ich im Internet danach suchen.",
#                 "text"=>
#                 "Ich weiß leider nicht, wo das ist. Wenn du möchtest, kann ich im Internet danach suchen."},
#                 "group"=>"com.apple.ace.assistant"},
#                 {"class"=>"Button",
#                 "properties"=>
#                 {"commands"=>
#                 [{"class"=>"SendCommands",
#                  "properties"=>
#                  {"commands"=>
#                  [{"class"=>"StartRequest",
#                   "properties"=>
#                   {"handsFree"=>false,
#                   "utterance"=>
#                   "^webSearchQuery^=^Amerika^^webSearchConfirmation^=^Ja^"},
#                   "group"=>"com.apple.ace.system"}]},
#                  "group"=>"com.apple.ace.system"}],
#                 "text"=>"Websuche"},
#                 "group"=>"com.apple.ace.assistant"}]},
#    "aceId"=>"fbec8e13-5781-4b27-8c36-e43ec922dda3",
#    "refId"=>"702C0671-DB6F-4914-AACD-30E84F7F7DF3",
#    "group"=>"com.apple.ace.assistant"}
