#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2, urllib
import json

from plugin import *

from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.mapObjects import SiriMapItemSnippet,SiriLocation, SiriMapItem

class maptest(Plugin):
    
    @register("de-DE", ".*test map.*")     
    @register("en-US", "(test map.*)")
    @register("fr-FR", "(test carte.*)|(test plan.*)")
    def mapDisplay(self, speech, language):
        view = AddViews(self.refId, dialogPhase="Completion")
        mapsnippet = SiriMapItemSnippet(items=[SiriMapItem()])
        view.views = [AssistantUtteranceView(text="Testing map", dialogIdentifier="Map#test"), mapsnippet]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()
        
    @register("de-DE", "(Wo bin ich.*)")     
    @register("en-US", "(Where am I.*)")
    @register("fr-FR", u"((ou|où).*suis.*je.*)")
    def whereAmI(self, speech, language):
        location = self.getCurrentLocation(force_reload=True)
        url = "http://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&sensor=false&language={2}".format(str(location.latitude),str(location.longitude), language)
        jsonString = None
        city = ""
        country = ""
        state = ""
        stateLong = ""
        countryCode = ""
        result = ""
        street = ""
        postal_code = ""
        try:
	        jsonString = urllib2.urlopen(url, timeout=3).read()
	        response = json.loads(jsonString)
	        components = response['results'][0]['address_components']
	        result = response['results'][0]['formatted_address'];
        except:
	        pass
        if components != None:
            city = filter(lambda x: True if "locality" in x['types'] or "administrative_area_level_1" in x['types'] else False, components)[0]['long_name']
            country = filter(lambda x: True if "country" in x['types'] else False, components)[0]['long_name']
            state = filter(lambda x: True if "administrative_area_level_1" in x['types'] or "country" in x['types'] else False, components)[0]['short_name']
            stateLong = filter(lambda x: True if "administrative_area_level_1" in x['types'] or "country" in x['types'] else False, components)[0]['long_name']
            countryCode = filter(lambda x: True if "country" in x['types'] else False, components)[0]['short_name']
            street = filter(lambda x: True if "route" in x['types'] else False, components)[0]['short_name']
            street_number = filter(lambda x: True if "street_number" in x['types'] else False, components)[0]['short_name']
            street = street + " " + street_number
            postal_code = filter(lambda x: True if "postal_code" in x['types'] else False, components)[0]['short_name']

        view = AddViews(self.refId, dialogPhase="Completion")
        mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(result, SiriLocation(result, street, city, state, countryCode, postal_code, location.latitude, location.longitude))])
        view.views = [AssistantUtteranceView(text="Recherche de votre emplacement...", dialogIdentifier="Map#test"), mapsnippet]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()