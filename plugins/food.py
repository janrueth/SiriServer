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
from siriObjects.mapObjects import SiriMapItemSnippet,SiriLocation, SiriMapItem

yelp_api_key = APIKeyForAPI("yelp")
 
class food(Plugin):
    @register("en-US", "(find nearest|find nearby|find closest|show closeset|show nearby).* ([\w ]+)")
    def food(self, speech, language, regex):
        mapGetLocation = self.getCurrentLocation()
        latitude = mapGetLocation.latitude
        longitude = mapGetLocation.longitude
        Title = regex.group(regex.lastindex)
        Query = urllib.quote_plus(Title.encode("utf-8"))
	random_results = random.randint(2,15)
	foodurl = "http://api.yelp.com/business_review_search?term={0}&lat={1}&long={2}&radius=10&limit={3}&ywsid={4}".format(str(Query),latitude,longitude,random_results,str(yelp_api_key))
	try:
	     jsonString = urllib2.urlopen(foodurl, timeout=3).read()
	except:
	     jsonString = None	
        if jsonString != None:
		response = json.loads(jsonString)
	if response['message']['text'] == 'OK':
		self.say('I found '+str(random_results)+' for '+str(Query)+' near you:')
		for result in response['businesses']:
			name = result['name']
			street = result['address1']
			city = result['city']
			stateCode = result['state']
			countryCode= result['country_code'];
			lat = result['latitude']
			lng = result['longitude']
			distance = "{0:.2f}".format(result['distance'])
			view = AddViews(self.refId, dialogPhase="Completion")
			mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(name, Location(label=street,latitude=lat,longitude=lng, street=street))])
			view.views = [AssistantUtteranceView(text="Distance : "+str(distance)+" miles", dialogIdentifier="FoodMap"), mapsnippet]
			self.sendRequestWithoutAnswer(view)
	else:
		self.say("Could not get Restaurant Data!");		
        self.complete_request()
