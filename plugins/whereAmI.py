#!/usr/bin/python
# -*- coding: utf-8 -*-

#need help? ask john-dev
 
import re
import urllib2, urllib
import json
 
from plugin import *
 
from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.systemObjects import GetRequestOrigin, Location
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.mapObjects import SiriMapItem, SiriMapItemSnippet

class whereAmI(Plugin):
    
    @register("de-DE", "(Wo bin ich.*)")    
    @register("en-US", "(Where am I.*)")
    def whereAmI(self, speech, language):
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
                postalCode=""
                try:
                    city = filter(lambda x: True if "locality" in x['types'] or "administrative_area_level_1" in x['types'] else False, components)[0]['long_name']
                except:
                    city=""
                countryCode = filter(lambda x: True if "country" in x['types'] else False, components)[0]['short_name']
                view = AddViews(self.refId, dialogPhase="Completion")
                if language == "de-DE":
                    the_header="Dein Standort"
                else:
                    the_header="Your location"
                s_Location=Location(the_header, street, city, stateLong, countryCode, postalCode, latitude, longitude)
                mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(the_header, s_Location)])
                view.views = [AssistantUtteranceView(text=the_header, dialogIdentifier="Map"), mapsnippet]
                self.sendRequestWithoutAnswer(view)
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

    @register("de-DE", "(Wo liegt.*)")    
    @register("en-US", "(Where is.*)")
    def whereIs(self, speech, language):
        if language == "de-DE":
            the_location = re.match("(?u).* liegt ([\w ]+)$", speech, re.IGNORECASE)
        else:
            the_location = re.match("(?u).* is ([\w ]+)$", speech, re.IGNORECASE)
        if the_location != None:
            the_location = the_location.group(1).strip()
            the_location = the_location[0].upper()+the_location[1:]
        else:
            if language == "de-DE":
                self.say('Ich habe keinen Ort gefunden!',None)
            else:
                self.say('No location found!',None)
            self.complete_request()  
        url = u"http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false&language={1}".format(urllib.quote_plus(the_location.encode("utf-8")), language)
        jsonString=None
        try:
            jsonString = urllib2.urlopen(url, timeout=3).read()
        except:
            pass
        if jsonString != None:
            response = json.loads(jsonString)
            if response['status'] == 'OK':
                location = response['results'][0]['geometry']['location']
                city=response['results'][0]['address_components'][0]['long_name']
                try:
                    country=response['results'][0]['address_components'][2]['long_name']
                    countryCode=response['results'][0]['address_components'][2]['short_name']
                except:
                    country=the_location
                    countryCode=the_location
                if language=="de-DE":
                    the_header=u"Hier liegt {0}".format(the_location)
                else:
                    the_header=u"Here is {0}".format(the_location)
                view = AddViews(self.refId, dialogPhase="Completion")
                s_Location=Location(the_header, city, city, "", countryCode, "", str(location['lat']), str(location['lng']))
                mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(the_header, s_Location, "BUSINESS_ITEM")])
                view.views = [AssistantUtteranceView(text=the_header, dialogIdentifier="Map"), mapsnippet]
                self.sendRequestWithoutAnswer(view)
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
        
        
                       