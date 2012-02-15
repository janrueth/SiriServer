#!/usr/bin/python
# -*- coding: utf-8 -*-

# Based on the WhereAmI plugins

import re
import urllib2, urllib
import json

from plugin import *

from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.mapObjects import SiriMapItemSnippet,SiriLocation, SiriMapItem
from siriObjects.systemObjects import GetRequestOrigin,Location

APIKEY = APIKeyForAPI("googleplaces")

class location(Plugin):
    
    # temp regex, need to use group name...
    @register("fr-FR", u".*(o(u|ù) (puis.je trouv(e|é)r?)) (.*)|.*(o(ù|u) est|recherche|cherche|trouve) (.*) près de moi.*|.*(o(ù|u) est|recherche|cherche|trouve) (.*) près d'ici.*|.*(o(ù|u) est|recherche|cherche|trouve) (.*) le plus proche.*")
    def whereisPlaces(self, speech, language, regex):
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

    @register("de-DE", "(Wo liegt.*)")    
    @register("en-US", "(Where is.*)")
    @register("fr-FR", u".*(o(ù|u) (est|se trouve|se situe|ce situe)) (.*)")
    def whereIs(self, speech, language, regex):
        the_location = None
        if language == "de-DE":
            the_location = re.match("(?u).* liegt ([\w ]+)$", speech, re.IGNORECASE)
            the_location = the_location.group(1).strip()
        elif language == 'fr-FR':
            the_location == regex.group(regex.lastindex).strip()
        else:
            the_location = re.match("(?u).* is ([\w ]+)$", speech, re.IGNORECASE)
            the_location = the_location.group(1).strip()
            
        if the_location != None:
            the_location = the_location[0].upper()+the_location[1:]
        else:
            if language == "de-DE":
                self.say('Ich habe keinen Ort gefunden!',None)
            elif language == 'fr-FR':
                self.say(u"Désolé, je n'arrive pas à trouver cet endroit !")
            else:
                self.say('No location found!',None)
            self.complete_request() 
            return
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
                elif language =="fr-FR":
                    the_header=u"Voici l'emplacement de {0} :".format(the_location)
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
                elif language == "fr-FR":
                    self.say(u"Les informations demandées ne sont pas sur Google Maps !", u'Erreur')
                else:
                    self.say('The Googlemaps response did not hold the information i need!','Error')
        else:
            if language=="de-DE":
                self.say('Ich konnte keine Verbindung zu Googlemaps aufbauen','Fehler')
            elif language == 'fr-FR':
                self.say(u"Je n'arrive pas à joindre Google Maps.", 'Erreur')
            else:
                self.say('Could not establish a conenction to Googlemaps','Error');
        self.complete_request()        
