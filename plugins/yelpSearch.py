#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Alex 'apexad' Martin

import re
import urllib2, urllib
import json
import random

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.systemObjects import GetRequestOrigin,Location
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.mapObjects import SiriMapItemSnippet,SiriLocation, SiriMapItem

yelp_api_key = APIKeyForAPI("yelp")
 
class food(Plugin):
     @register("en-US", "(find nearest|find nearby|find closest|show closeset|show nearby|where is) (.*)")
     def food(self, speech, language, regex):
          self.say('Searching...',' ')
          mapGetLocation = self.getCurrentLocation()
          latitude = mapGetLocation.latitude
          longitude = mapGetLocation.longitude
          Title = regex.group(regex.lastindex).strip()
          Query = urllib.quote_plus(str(Title.encode("utf-8")))
          random_results = random.randint(2,15)
          foodurl = "http://api.yelp.com/business_review_search?term={0}&lat={1}&long={2}&radius=10&limit={3}&ywsid={4}".format(str(Query),latitude,longitude,random_results,str(yelp_api_key))
          try:
               jsonString = urllib2.urlopen(foodurl, timeout=20).read()
          except:
               jsonString = None
          if jsonString != None:
               response = json.loads(jsonString)
               if response['message']['text'] == 'OK':
                    food_results = []
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
                         food_results.append(SiriMapItem(name, Location(label=street,latitude=lat,longitude=lng, street=street)))
                    mapsnippet = SiriMapItemSnippet(items=food_results)
                    view.views = [AssistantUtteranceView(speakableText='I found '+str(random_results)+' results for '+str(Query).replace('+',' ')+' near you:', dialogIdentifier="FoodMap"), mapsnippet]
                    self.sendRequestWithoutAnswer(view)
               else:
                    self.say("I'm sorry but I did not find any results for "+str(Query).replace('+',' ')+"near you!")
          else:
               self.say("I'm sorry but I did not find any results for "+str(Query)+"near you!")
          self.complete_request()
