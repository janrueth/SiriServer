#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Alex 'apexad' Martin

import re
import urllib2, urllib, uuid
import json
import random

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.systemObjects import GetRequestOrigin,Location
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.localsearchObjects import ActionableMapItem
from siriObjects.mapObjects import SiriMapItemSnippet,SiriLocation, SiriMapItem

yahoo_api_key = APIKeyForAPI("yahoo")
 
class food(Plugin):
    
    @register("en-US", "(.*pizza.*)|(.*taco.*)|(.*burger.*)")
    def food(self, speech, language):
        mapGetLocation = self.getCurrentLocation()
        latitude = mapGetLocation.latitude
        longitude = mapGetLocation.longitude
        url = u"http://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&sensor=false&language={2}".format(str(latitude),str(longitude), language)
        try:
            jsonString = urllib2.urlopen(url, timeout=3).read()
        except:
            pass
        if jsonString != None:
            response = json.loads(jsonString)
            if response['status'] == 'OK':
                components = response['results'][0]['address_components']              
                street = filter(lambda x: True if "route" in x['types'] else False, components)[0]['long_name']
                stateLong= filter(lambda x: True if "administrative_area_level_1" in x['types'] or "country" in x['types'] else False, components)[0]['long_name']
                postalCode= filter(lambda x: True if "postal_code" in x['types'] else False, components)[0]['long_name']
		if (speech.count("pizza") > 0 or speech.count("Pizza") > 0):
		    foodType = "pizza"
		if (speech.count("taco") > 0 or speech.count("Taco") > 0):
		    foodType = "taco"
		if (speech.count("burger") > 0 or speech.count("Burger") > 0):
		    foodType = "burger"
	        foodurl = u"http://local.yahooapis.com/LocalSearchService/V3/localSearch?appid={0}&query={1}&zip={2}&results=5&output=json".format(str(yahoo_api_key),str(foodType),postalCode)
		try:
		    jsonString = urllib2.urlopen(foodurl, timeout=3).read()
        	except:
            	    pass
        	if jsonString != None:
            	    response = json.loads(jsonString)
            	if response['ResultSet']['totalResultsReturned'] >= 2:
			for result in response['ResultSet']['Result']:
				the_header = result['Title']
				name = the_header
				street = result['Address']
				vicinity = street;
				city = result['City']
				stateLong = response['ResultSet']['Result'][0]['State']
				countryCode= 'US';
				lat = result['Latitude']
				lng = result['Longitude']
				#distance = self.haversine_distance(location.latitude, location.longitude, lat, lng)
				distance = 0.4
				#Location=SiriLocation(the_header, street, city, stateLong, countryCode, postalCode, lat, lng)
				#mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(the_header, Location)])
				#view.views = [AssistantUtteranceView(text=Distance, dialogIdentifier="Map#test"), mapsnippet]
				view = AddViews(self.refId, dialogPhase="Completion")
				mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(name, Location(label=vicinity,latitude=lat,longitude=lng, street=vicinity))])
				view.views = [AssistantUtteranceView(text="Distance : "+str(distance)+" km", dialogIdentifier="Map#test"), mapsnippet]
				self.sendRequestWithoutAnswer(view)

		else:
			self.say("Could not get Restaurant Data!");		
            else:
                if language=="de-DE":
                    self.say('Die Googlemaps informationen waren ungenügend!','Fehler')
                else:
                    self.say('The Googlemaps response did not hold the information i need!','Error')
        else:
            if language=="de-DE":
                self.say('Ich konnte keine Verbindung zu Googlemaps aufbauen','Fehler')
            else:
                self.say('Could not establish a conenction to Googlemaps','Error');
        self.complete_request()
