#!/usr/bin/python
# -*- coding: utf-8 -*-
# Railtime (utilise l'API iRail)
# Par Cédric Boverie (cedbv)
import re
import json
import urllib2, urllib
from datetime import datetime
import math

from plugin import *

class Railtime(Plugin):
    
    @register("fr-FR", u"(kel|quel|o(ù|u)).*(train | train|gare | gare).*")
    def railtime(self, speech, language, regex):
        gare = None
        lang = language[:2]
        
        try:
            gareOuPasGare = re.match(u".*(au départ de|au départ|a|à|de|dans|pour) (.*)", speech, re.IGNORECASE)
            gare = gareOuPasGare.group(gareOuPasGare.lastindex).strip()
            gare = urllib.quote_plus(gare.encode("utf-8"))
        except:
            pass

        if gare != None:
            response = None
            try:
                url = u"http://api.irail.be/liveboard/?station={0}&format=json&fast=true&lang={1}".format(gare,lang)
                jsonString = urllib2.urlopen(url, timeout=3).read()
                response = json.loads(jsonString)
            except:
                pass
        else:
            # we will try to deduce the station with the location
            location = self.getCurrentLocation(force_reload=True,accuracy=GetRequestOrigin.desiredAccuracyBest)
            latitude = location.latitude
            longitude = location.longitude

            url = u"http://api.irail.be/stations/?format=json&fast=true&lang={0}".format(lang)
            jsonString = urllib2.urlopen(url, timeout=3).read()
            response = json.loads(jsonString)

            max_dist = 999999
            for station in response["station"]:
                id = station["id"]

                dist = self.haversine_distance(latitude,longitude, float(station["locationY"]), float(station["locationX"]))
                if(dist < max_dist):
                    station_choisie = station
                    max_dist = dist
            
            gare = station_choisie["name"]
            url = "http://api.irail.be/liveboard/?id={0}&fast=true&lang={1}&format=json".format(station_choisie["id"],lang)
            print url
            try:
                jsonString = urllib2.urlopen(url, timeout=3)
                response = json.load(jsonString);
            except:
                pass
            
        if response != None:
            number = response["departures"]["number"]
            self.say(u"J'ai trouvé {0} trains au départ de {1} :".format(number,response["station"]))
            print response
            for departure in response["departures"]["departure"]:
                   
                if departure["platform"] == u'':                   
                    string = u"{0}".format(departure["station"])
                else:
                    string = u"{0} sur la voie {1}".format(departure["station"], departure["platform"])
                
                if departure["platforminfo"]["normal"] != "1":
                    string += u" (changement de voie)"
                
                string += u" à {0}.".format(datetime.fromtimestamp(float(departure["time"])).strftime("%H:%M"))
                
                
                if departure["delay"] != "0":
                    if departure["delay"] == "cancel":
                        string += u" Annulé."
                    else:
                        string += u" En retard de {0} minutes.".format(int(departure["delay"])/60)
                   
                self.say(string)
        else:
            self.say(u"Je ne parviens pas à récupérer le liveboard pour {0} !".format(gare))

        self.complete_request()

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        RAD_PER_DEG = 0.017453293
        Rkm = 6371        
        dlon = lon2-lon1
        dlat = lat2-lat1
        dlon_rad = dlon*RAD_PER_DEG
        dlat_rad = dlat*RAD_PER_DEG
        lat1_rad = lat1*RAD_PER_DEG
        lon1_rad = lon1*RAD_PER_DEG
        lat2_rad = lat2*RAD_PER_DEG
        lon2_rad = lon2*RAD_PER_DEG
        
        a = (math.sin(dlat_rad/2))**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(dlon_rad/2))**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return round(Rkm * c,2)
