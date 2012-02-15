#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2, urllib
import json

from plugin import *

from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.mapObjects import SiriMapItemSnippet,SiriLocation, SiriMapItem
from siriObjects.systemObjects import GetRequestOrigin,Location

APIKEY = APIKeyForAPI("googleplaces")

class location(Plugin):
    
    @register("fr-FR", u".*(o(u|ù) (est|se trouve|trouv(e|é)r?)) (.*)|.*(recherche|cherche|trouve) (.*) près de moi.*")
    def whereis(self, speech, language, regex):
        keyword = regex.group(regex.lastindex).strip()
        location = self.getCurrentLocation(force_reload=True,accuracy=GetRequestOrigin.desiredAccuracyBest)
        latlong = str(location.latitude)+","+str(location.longitude)
        response = None
        url = "https://maps.googleapis.com/maps/api/place/search/json?location={0}&radius=15000&keyword={1}&sensor=true&key={2}".format(latlong,urllib.quote_plus(keyword.encode("utf-8")),APIKEY)

        try:
            jsonString = urllib2.urlopen(url, timeout=3)
            response = json.load(jsonString);
        except:
            pass
            
        if response["status"] == "OK":
            self.say(u"J'ai trouvé {0} résultats : ".format(len(response["results"])))
            for result in response["results"]:
                ident = result["id"]
                name = result["name"]
                lat = result["geometry"]["location"]["lat"]
                lng = result["geometry"]["location"]["lng"]
                vicinity = result["vicinity"]
                if "rating" in result:
                    rating = result["rating"]
                else:
                    rating = 0.0
        
                view = AddViews(self.refId, dialogPhase="Completion")
                mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(name, Location(label=vicinity,latitude=lat,longitude=lng, street=vicinity))])
                view.views = [AssistantUtteranceView(text="Distance : x km", dialogIdentifier="Map#test"), mapsnippet]
                self.sendRequestWithoutAnswer(view)

        elif response["status"] == "ZERO_RESULTS":
            self.say(u"Pas de résultat")
        else:
            self.say(u"Il m'est impossible de contacter Google pour le moment ! Veuillez réessayer plus tard.")
        self.complete_request()

    @register("de-DE", "(Wo bin ich.*)")     
    @register("en-US", "(Where am I.*)")
    @register("fr-FR", u"((ou|où).*suis.*je.*)")
    def whereAmI(self, speech, language):
        location = self.getCurrentLocation(force_reload=True,accuracy=GetRequestOrigin.desiredAccuracyBest)
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
        self.say(u"Vous êtes "+result)
        self.complete_request()
