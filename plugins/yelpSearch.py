#!/usr/bin/python
# -*- coding: utf-8 -*-
# by Alex 'apexad' Martin
# help from: muhkuh0815 & gaVRos

import re
import urllib2, urllib
import json
import random

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.systemObjects import GetRequestOrigin,Location
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.localsearchObjects import Business, MapItem, MapItemSnippet, Rating

yelp_api_key = APIKeyForAPI("yelp")
 
class yelpSearch(Plugin):
     @register("en-US", "(find|show|where).* (nearest|nearby|closest) (.*)")
     @register("en-GB", "(find|show|where).* (nearest|nearby|closest) (.*)")
     def yelp_search(self, speech, language, regex):
          self.say('Searching...',' ')
          mapGetLocation = self.getCurrentLocation()
          latitude = mapGetLocation.latitude
          longitude = mapGetLocation.longitude
          Title = regex.group(regex.lastindex).strip()
          Query = urllib.quote_plus(str(Title.encode("utf-8")))
          random_results = random.randint(2,15)
          yelpurl = "http://api.yelp.com/business_review_search?term={0}&lat={1}&long={2}&radius=3&limit=20&ywsid={3}".format(str(Query),latitude,longitude,str(yelp_api_key))
          try:
               jsonString = urllib2.urlopen(yelpurl, timeout=20).read()
          except:
               jsonString = None
          if jsonString != None:
               response = json.loads(jsonString)
               if (response['message']['text'] == 'OK') and (len(response['businesses'])):
                    response['businesses'] = sorted(response['businesses'], key=lambda business: float(business['distance']))
                    yelp_results = []
                    for result in response['businesses']:
                         rating = Rating(value=result['avg_rating'], providerId='YELP', count=result['review_count'])
                         details = Business(totalNumberOfReviews=result['review_count'],name=result['name'],rating=rating)
                         if (len(yelp_results) < random_results):
                              mapitem = MapItem(label=result['name'], street=result['address1'], stateCode=result['state_code'], postalCode=result['zip'],latitude=result['latitude'], longitude=result['longitude'])
                              mapitem.detail = details
                              yelp_results.append(mapitem)
                         else:
                              break
                    mapsnippet = MapItemSnippet(items=yelp_results)
                    count_min = min(len(response['businesses']),random_results)
                    count_max = max(len(response['businesses']),random_results)
                    view = AddViews(self.refId, dialogPhase="Completion")
                    view.views = [AssistantUtteranceView(speakableText='I found '+str(count_max)+' '+str(Title)+' results... '+str(count_min)+' of them are fairly close to you:', dialogIdentifier="yelpSearchMap"), mapsnippet]
                    self.sendRequestWithoutAnswer(view)
               else:
                    self.say("I'm sorry but I did not find any results for "+str(Title)+" near you!")
          else:
               self.say("I'm sorry but I did not find any results for "+str(Title)+" near you!")
          self.complete_request()
