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

yahoo_api_key = APIKeyForAPI("yahoo")
 
class yahooLocalSearch(Plugin):
     @register("en-US", "(find|show|where).* (nearest|nearby|closest) (.*)")
     @register("en-GB", "(find|show|where).* (nearest|nearby|closest) (.*)")
     def yahoo_search(self, speech, language, regex):
          self.say('Searching...',' ')
          mapGetLocation = self.getCurrentLocation()
          latitude = mapGetLocation.latitude
          longitude = mapGetLocation.longitude
          Title = regex.group(regex.lastindex).strip()
          Query = urllib.quote_plus(str(Title.encode("utf-8")))
          random_results = random.randint(2,15)
          yahoourl = "http://local.yahooapis.com/LocalSearchService/V3/localSearch?appid={0}&query={1}&latitude={2}&longitude={3}&results=20&sort=distance&output=json".format(str(yahoo_api_key),str(Query),latitude,longitude)
          try:
               jsonString = urllib2.urlopen(yahoourl, timeout=20).read()
          except:
               jsonString = None
          if jsonString != None:
               response = json.loads(jsonString)
               if response['ResultSet']['totalResultsReturned'] >= 1:
                    #response['ResultSet'] = sorted(response['ResultSet']['Result'], key=lambda result: float(result['Distance']))
                    yahoo_results = []
                    for result in response['ResultSet']['Result']:
                         rating = Rating(value=result['Rating']['AverageRating'], providerId='Yahoo', count=result['Rating']['TotalRatings'])
                         details = Business(totalNumberOfReviews=result['Rating']['TotalRatings'],name=result['Title'],rating=rating)
                         if (len(yahoo_results) < random_results):
                              mapitem = MapItem(label=result['Title'], street=result['Address'], stateCode=result['State'], latitude=result['Latitude'], longitude=result['Longitude'])
                              mapitem.detail = details
                              yahoo_results.append(mapitem)
                         else:
                              break
                    mapsnippet = MapItemSnippet(items=yahoo_results)
                    count_min = min(len(response['ResultSet']['Result']),random_results)
                    count_max = max(len(response['ResultSet']['Result']),random_results)
                    view = AddViews(self.refId, dialogPhase="Completion")
                    view.views = [AssistantUtteranceView(speakableText='I found '+str(count_max)+' '+str(Title)+' results... '+str(count_min)+' of them are fairly close to you:', dialogIdentifier="yahooLocalSearchMap"), mapsnippet]
                    self.sendRequestWithoutAnswer(view)
               else:
                    self.say("I'm sorry but I did not find any results for "+str(Title)+" near you!")
          else:
               self.say("I'm sorry but I did not find any results for "+str(Title)+" near you!")
          self.complete_request()
