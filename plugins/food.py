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
	if (speech.count("pizza") > 0 or speech.count("Pizza") > 0):
		foodType = "pizza"
	if (speech.count("taco") > 0 or speech.count("Taco") > 0):
		foodType = "taco"
	if (speech.count("burger") > 0 or speech.count("Burger") > 0):
		foodType = "burger"
	foodurl = "http://local.yahooapis.com/LocalSearchService/V3/localSearch?appid={0}&query={1}&latitude={2}&longitude={3}&results=5&output=json".format(str(yahoo_api_key),str(foodType),latitude,longitude)
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
			stateLong = result['State']
			countryCode= 'US';
			lat = result['Latitude']
			lng = result['Longitude']
			distance = result['Distance']
			view = AddViews(self.refId, dialogPhase="Completion")
			mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(name, Location(label=vicinity,latitude=lat,longitude=lng, street=vicinity))])
			view.views = [AssistantUtteranceView(text="Distance : "+str(distance)+" miles", dialogIdentifier="Map#test"), mapsnippet]
			self.sendRequestWithoutAnswer(view)
	else:
		self.say("Could not get Restaurant Data!");		
        self.complete_request()
