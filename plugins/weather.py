#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author: Sebastian Koch
import re
import urllib2, urllib, uuid
import json
import random


from plugin import *
from datetime import date
from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.forecastObjects import *

#Obtain API Key from wundergrounds.com
weatherApiKey = APIKeyForAPI('wundergrounds')

class SiriWeatherFunctions():
    def __init__(self):
        self.conditionTerm="clear"
        self.night=False
        self.result=dict()
    def __missing__(self, key):
        result = self[key] = D()
        return result

    def swapCondition(self,conditionTerm="clear", night=False):
        conditionsArray={"cloudy":{"conditionCodeIndex":26,"conditionCode":"Cloudy","night":{"conditionCodeIndex":27,"conditionCode":"MostlyCloudyNight"}},"rain":{"conditionCodeIndex":11,"conditionCode":"Showers"},"unknown":{"conditionCodeIndex":26,"conditionCode":"Cloudy"},"partlycloudy":{"conditionCodeIndex":30,"conditionCode":"PartlyCloudyDay","night":{"conditionCodeIndex":29,"conditionCode":"PartlyCloudyNight"}},"tstorms":{"conditionCodeIndex":4,"conditionCode":"Thunderstorms"},"sunny":{"conditionCodeIndex":32,"conditionCode":"Sunny","night":{"conditionCodeIndex":31,"conditionCode":"ClearNight"}},"snow":{"conditionCodeIndex":16,"conditionCode":"Snow"},"sleet":{"conditionCodeIndex":18,"conditionCode":"Sleet"},"partlysunny":{"conditionCodeIndex":30,"conditionCode":"PartlyCloudyDay","night":{"conditionCodeIndex":29,"conditionCode":"PartlyCloudyNight"}},"mostlysunny":{"conditionCodeIndex":34,"conditionCode":"FairDay","night":{"conditionCodeIndex":33,"conditionCode":"FairNight"}},"mostlycloudy":{"conditionCodeIndex":28,"conditionCode":"MostlyCloudyDay","night":{"conditionCodeIndex":27,"conditionCode":"MostlyCloudyNight"}},"hazy":{"conditionCodeIndex":21,"conditionCode":"Haze","night":{"conditionCodeIndex":29,"conditionCode":"PartlyCloudyNight"}},"fog":{"conditionCodeIndex":20,"conditionCode":"Foggy"},"flurries":{"conditionCodeIndex":13,"conditionCode":"SnowFlurries"},"clear":{"conditionCodeIndex":32,"conditionCode":"Sunny","night":{"conditionCodeIndex":31,"conditionCode":"ClearNight"}},"chancetstorms":{"conditionCodeIndex":38,"conditionCode":"ScatteredThunderstorms"},"chancesnow":{"conditionCodeIndex":42,"conditionCode":"ScatteredSnowShowers"},"chancesleet":{"conditionCodeIndex":6,"conditionCode":"MixedRainAndSleet"},"chancerain":{"conditionCodeIndex":40,"conditionCode":"ScatteredShowers"},"chanceflurries":{"conditionCodeIndex":13,"conditionCode":"SnowFlurries"}}
        self.conditionTerm=conditionTerm.replace("nt_","")
        self.night = night

        if (conditionsArray[self.conditionTerm].has_key("night")) and (self.night==True):
            self.result["conditionCode"]=conditionsArray[self.conditionTerm]["night"]["conditionCode"]
            self.result["conditionCodeIndex"]=conditionsArray[self.conditionTerm]["night"]["conditionCodeIndex"]
        else:
            self.result["conditionCode"]=conditionsArray[self.conditionTerm]["conditionCode"]
            self.result["conditionCodeIndex"]=conditionsArray[self.conditionTerm]["conditionCodeIndex"]

        return self.result



class weatherPlugin(Plugin):
    localizations = {"weatherForecast":
                        {"search":{
                            0:{"de-DE": u"Einen Moment Geduld bitte...", "en-US": "Checking my sources...", "fr-FR": u"Je vérifie mes sources..."},
                            1:{"de-DE": u"Ich suche nach der Vorhersage ...", "en-US": "Please wait while I check that...", "fr-FR": "Je regarde..."},
                            2:{"de-DE": u"Einen Moment bitte ...", "en-US": "One moment please...", "fr-FR":"Un instant..."},
                            3:{"de-DE": u"Ich suche nach Wetterdaten...", "en-US": "Trying to get weather data for this location...","fr-FR": u"Je récupère la météo de cet endroit..."},
                            },
                        "forecast":{
                            "DAILY": {
                                0:{"de-DE": u"Hier ist die Vorhersage für {0}, {1}", "en-US": u"Here is the forecast for {0}, {1}", "fr-FR": u"Voici les prévisions pour {0}, {1}"},
                                1:{"de-DE": u"Hier ist die Wetterprognose für {0}, {1}", "en-US": u"This is the forecast for {0}, {1}", "fr-FR": u"Voilà les prévisions pour {0}, {1}"},
                                2:{"de-DE": u"Ich habe folgende Vorhersage für {0}, {1} gefunden", "en-US": u"I found the following forecast for {0}, {1}", "fr-FR": u"J'ai trouvé les prévisions suivantes pour {0}, {1}."},
                                },
                            "HOURLY": {
                                0:{"de-DE": u"Hier ist die heutige Vorhersage für {0}, {1}", "en-US": u"Here is today's forecast for {0}, {1}","fr-FR": u"Voici les prévisions d'aujourd'hui pour {0}, {1}."},
                                1:{"de-DE": u"Hier ist die Wetterprognose von heute für {0}, {1}", "en-US": u"This is today's forecast for {0}, {1}", "fr-FR": u"Voici les prévisions d'aujourd'hui pour {0}, {1}."},
                                2:{"de-DE": u"Ich habe folgende Tagesprognose für {0}, {1} gefunden", "en-US": u"I found the following hourly forecast for {0}, {1}","fr-FR": u"J'ai trouvé les prévisions pour {0}, {1}."},
                                }
                        },
                        "failure": {
                                   "de-DE": "Ich konnte leider keine Wettervorhersage finden!", "en-US": "I'm sorry but I could not find the forecast for this location!","fr-FR": u"Je suis désolé, je ne trouve pas cet endroit !"
                                   }
                        }
                    }

    @register("de-DE", "(.*Wetter.*)|(.*Vorhersage.*)")
    @register("en-US", "(.*Weather.*)|(.*forecast.*)")
    @register("fr-FR", u".*(Météo|prévision|Quel.*temps|(fais|fait|faire).*(chaud|froid)).*|j.*chaud.*|.*température.*|.*heure.*soleil.*")
    def weatherForecastLookUp(self, speech, language):
        speech = speech.replace(u".","").lower()
        viewType ="DAILY"
        if (speech.count("today") > 0 or speech.count("current") > 0 or speech.count(" for today") > 0) and language=="en-US":
            viewType = "HOURLY"
            speech = speech.replace("todays","")
            speech = speech.replace("today","")
            speech = speech.replace("currently","")
            speech = speech.replace("current","")
            speech = speech.replace(" for today"," in ")
            speech = speech.replace(" for "," in ")
        if (speech.count("aujourd'hui") > 0 or speech.count("actuel") > 0 or speech.count("maintenant") > 0 or speech.count(" pour aujourd'hui") > 0 or speech.count("fait") > 0 and language == "fr-FR"):
            viewType = "HOURLY"
            speech = speech.replace(" pour aujourd'hui","")
            speech = speech.replace("aujourd'hui","")
            speech = speech.replace("pour maintenant","")
            speech = speech.replace("de maintenant","")
            speech = speech.replace("maintenant","")
            speech = speech.replace("actuellement","")
            speech = speech.replace("actuelle","")
            speech = speech.replace("actuel","")
        if (speech.count("heute") > 0 or speech.count("moment") > 0 or speech.count(u"nächsten Stunden") > 0 or speech.count(u"für heute") > 0) and language=="de-DE":
            viewType = "HOURLY"
            speech = speech.replace("heute","")
            speech = speech.replace("im moment","")
            speech = speech.replace("momentan","")
            speech = speech.replace("aktuelle","")
            speech = speech.replace("aktuell","")
            speech = speech.replace(u"in den nächsten Stunden","")
            speech = speech.replace(u"für heute","")

        if language=="en-US":
            speech = speech.replace(" for "," in ")
        elif language=="de-DE":
            speech = speech.replace(u"in den nächsten Tagen","")
            speech = speech.replace(u"in den nächsten paar Tagen","")
            speech = speech.replace(u"in der nächsten Woche","")
            speech = speech.replace(u"nächste Woche","")
            speech = speech.replace(u" für "," in ")
        elif language=="fr-FR":
            speech = speech.replace(u"du soleil","soleil")
            speech = speech.replace(u"de coucher","coucher").replace("du coucher","").replace(u"de levé","").replace("de lever","")

        error = False
        view = AddViews(refId=self.refId, dialogPhase="Reflection")
        randomNumber = random.randint(0,3)
        view.views = [AssistantUtteranceView(weatherPlugin.localizations['weatherForecast']['search'][randomNumber][language], weatherPlugin.localizations['weatherForecast']['search'][randomNumber][language])]
        self.connection.send_object(view)






        countryOrCity = re.match(u"(?u).* (a |à |de |pour |dans |en |in )(.*)", speech, re.IGNORECASE)
        if countryOrCity != None:
            countryOrCity = countryOrCity.group(countryOrCity.lastindex).strip()
            print "found forecast"
            # lets see what we got, a country or a city...
            # lets use google geocoding API for that
            url = "http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false&language={1}".format(urllib.quote_plus(countryOrCity.encode("utf-8")), language)
            print url
        elif countryOrCity == None:
            currentLocation=self.getCurrentLocation()
            url = "http://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&sensor=false&language={2}".format(str(currentLocation.latitude),str(currentLocation.longitude), language)
            print url
            # lets wait max 3 seconds
        jsonString = None
        try:
            jsonString = urllib2.urlopen(url, timeout=3).read()
        except:
            pass
        if jsonString != None:
            response = json.loads(jsonString)
            # lets see what we have...
            if response['status'] == 'OK':
                components = response['results'][0]['address_components']
                types = components[0]['types'] # <- this should be the city or country
                if "country" in types:
                    # OK we have a country as input, that sucks, we need the capital, lets try again and ask for capital also
                    components = filter(lambda x: True if "country" in x['types'] else False, components)
                    url = "http://maps.googleapis.com/maps/api/geocode/json?address=capital%20{0}&sensor=false&language={1}".format(urllib.quote_plus(components[0]['long_name']), language)
                    print url
                    # lets wait max 3 seconds
                    jsonString = None
                    try:
                        jsonString = urllib2.urlopen(url, timeout=3).read()
                    except:
                        pass
                    if jsonString != None:
                        response = json.loads(jsonString)
                        if response['status'] == 'OK':
                            components = response['results'][0]['address_components']
            # response could have changed, lets check again, but it should be a city by now
            if response['status'] == 'OK':
                # get latitude and longitude
                location = response['results'][0]['geometry']['location']

                city = ""
                country = ""
                state = ""
                stateLong = ""
                countryCode = ""
                shortName = ""
                longName = ""
                try:
                    city = filter(lambda x: True if "locality" in x['types'] or "administrative_area_level_1" in x['types'] else False, components)[0]['long_name']
                    country = filter(lambda x: True if "country" in x['types'] else False, components)[0]['long_name']
                    state = filter(lambda x: True if "administrative_area_level_1" in x['types'] or "country" in x['types'] else False, components)[0]['short_name']
                    stateLong = filter(lambda x: True if "administrative_area_level_1" in x['types'] or "country" in x['types'] else False, components)[0]['long_name']
                    countryCode = filter(lambda x: True if "country" in x['types'] else False, components)[0]['short_name']
                except:
                    pass

                url = "http://api.wunderground.com/api/{0}/geolookup/conditions/forecast7day//hourly7day/astronomy/q/{1},{2}.json".format(weatherApiKey, location['lat'], location['lng'])
                print url
                 # lets wait max 3 seconds
                jsonString = None
                try:
                    jsonString = urllib2.urlopen(url, timeout=5).read()
                except:
                    pass
                if jsonString != None:
                    response = json.loads(jsonString)
                    # lets see what we have...
                    if response.has_key("error")==False:
                        weatherTemp=dict()
                        if response.has_key("current_observation"):
                            if response.has_key("moon_phase"):
                                if (int(response["moon_phase"]["current_time"]["hour"]) > int(response["moon_phase"]["sunset"]["hour"])) or (int(response["moon_phase"]["current_time"]["hour"]) < int(response["moon_phase"]["sunrise"]["hour"])):
                                    weatherTempNightTime = True

                                else:
                                   weatherTempNightTime = False
                            else:
                                weatherTempNightTime = False

                            conditionSwapper = SiriWeatherFunctions()
                            dayOfWeek=[] #
                            for i in range(1,8):
                                dayOfWeek.append(i % 7 + 1)

                            tempNight=weatherTempNightTime
                            weatherTemp["currentTemperature"] =str(response["current_observation"]["temp_c"])

                            dailyForecasts=[]
                            for x in range(0,6):
                                forecastDate = date(int(response["forecast"]["simpleforecast"]["forecastday"][x]["date"]["year"]),int(response["forecast"]["simpleforecast"]["forecastday"][x]["date"]["month"]),int(response["forecast"]["simpleforecast"]["forecastday"][x]["date"]["day"]))

                                weatherTemp["tempCondition"] = conditionSwapper.swapCondition(conditionTerm=response["forecast"]["simpleforecast"]["forecastday"][x]["icon"], night=tempNight)
                                dailyForecasts.append(SiriForecastAceWeathersDailyForecast(timeIndex=(dayOfWeek[date.weekday(forecastDate)]), highTemperature=response["forecast"]["simpleforecast"]["forecastday"][x]["high"]["celsius"], lowTemperature=response["forecast"]["simpleforecast"]["forecastday"][x]["low"]["celsius"], condition=SiriForecastAceWeathersConditions(conditionCode=weatherTemp["tempCondition"]["conditionCode"], conditionCodeIndex=weatherTemp["tempCondition"]["conditionCodeIndex"])))
                                tempNight=False

                            hourlyForecasts=[]
                            for x in range(0,10):
                                if response["hourly_forecast"][x]:
                                    if (int(response["moon_phase"]["current_time"]["hour"]) <= int(response["hourly_forecast"][x]["FCTTIME"]["hour"])) or (int(response["forecast"]["simpleforecast"]["forecastday"][0]["date"]["day"]) < int(response["hourly_forecast"][x]["FCTTIME"]["mday"])) or (int(response["forecast"]["simpleforecast"]["forecastday"][0]["date"]["month"]) < int(response["hourly_forecast"][x]["FCTTIME"]["mon"])):
                                        if response.has_key("hourly_forecast")==True:
                                            weatherTemp=dict()
                                            if response.has_key("current_observation"):
                                                if response.has_key("moon_phase"):
                                                    if (int(response["moon_phase"]["sunset"]["hour"]) < int(response["hourly_forecast"][x]["FCTTIME"]["hour"])) or (int(response["moon_phase"]["sunrise"]["hour"]) > int(response["hourly_forecast"][x]["FCTTIME"]["hour"])):
                                                         weatherTempCon = conditionSwapper.swapCondition(conditionTerm=response["hourly_forecast"][x]["icon"], night=True)


                                                    else:
                                                       weatherTempCon = conditionSwapper.swapCondition(conditionTerm=response["hourly_forecast"][x]["icon"], night=False)

                                                else:
                                                    weatherTempCon = conditionSwapper.swapCondition(conditionTerm=response["hourly_forecast"][x]["icon"], night=True)


                                        hourlyForecasts.append(SiriForecastAceWeathersHourlyForecast(timeIndex=response["hourly_forecast"][x]["FCTTIME"]["hour"], chanceOfPrecipitation=int(response["hourly_forecast"][x]["pop"]), temperature=response["hourly_forecast"][x]["temp"]["metric"],  condition=SiriForecastAceWeathersConditions(conditionCode=weatherTempCon["conditionCode"], conditionCodeIndex=weatherTempCon["conditionCodeIndex"])))

                            weatherTemp["currentCondition"] = conditionSwapper.swapCondition(conditionTerm=response["current_observation"]["icon"], night=weatherTempNightTime)
                            currentTemperature=str(response["current_observation"]["temp_c"])
                            currentDate=date(int(response["forecast"]["simpleforecast"]["forecastday"][0]["date"]["year"]),int(response["forecast"]["simpleforecast"]["forecastday"][0]["date"]["month"]),int(response["forecast"]["simpleforecast"]["forecastday"][0]["date"]["day"]))
                            view = AddViews(self.refId, dialogPhase="Summary")

                            currentConditions=SiriForecastAceWeathersCurrentConditions(dayOfWeek=dayOfWeek[int(date.weekday(currentDate))],temperature=currentTemperature, condition=SiriForecastAceWeathersConditions(conditionCode=weatherTemp["currentCondition"]["conditionCode"], conditionCodeIndex=weatherTemp["currentCondition"]["conditionCodeIndex"]))

                            aceWethers=[SiriForecastAceWeathers(extendedForecastUrl = response["location"]["wuiurl"], currentConditions=currentConditions, hourlyForecasts=hourlyForecasts, dailyForecasts=dailyForecasts, weatherLocation=SiriForecastAceWeathersWeatherLocation(), units=SiriForecastAceWeathersUnits(), view=viewType, )]
                            weather = SiriForecastSnippet(aceWeathers=aceWethers)
                            speakCountry = stateLong if country == "United States" else country
                            if language=="de-DE":
                                speakCountry = stateLong + " (" + country + ")" if country == "USA" else country

                            if city == "":
                                city = components[0]['short_name']
                            if country == "":
                                speakCountry = components[0]['long_name']

                            rep = None
                            if viewType == "HOURLY":
                                if speech.count(u"chaud") > 0:
                                    rep = u"Oui, il fait chaud, {0}°C à {1}, {2}."
                                elif speech.count(u"froid") > 0:
                                    rep = u"Non, pas très froid, {0}°C à {1}, {2}."
                                elif speech.count(u"température") > 0:
                                    rep = u"La température actuelle est de {0}°C à {1}, {2}."
                            print response["moon_phase"]

                            if speech.count(u"soleil") > 0 and speech.count(u"heure") > 0:
                                #If not present, not really important...
                                try:
                                    rep = u"Le soleil se lève à {0}:{1} et se couche à {2}:{3}".format(response["moon_phase"]["sunrise"]["hour"],response["moon_phase"]["sunrise"]["minute"],response["moon_phase"]["sunset"]["hour"],response["moon_phase"]["sunset"]["minute"])
                                except:
                                    pass

                            if rep == None:
                                randomNumber = random.randint(0,2)
                                rep = weatherPlugin.localizations['weatherForecast']['forecast'][viewType][randomNumber][language].format(city,speakCountry)
                            else:
                                rep = rep.format(response["current_observation"]["temp_c"],city,speakCountry)

                            view.views = [AssistantUtteranceView(text=rep,speakableText=rep, dialogIdentifier="Weather#forecastCommentary"), weather]
                            self.sendRequestWithoutAnswer(view)
                        else:
                            error = True
                    else:
                        error = True
                else:
                    error = True
            else:
                error = True
        else:
            error = True



        if error:
            self.say(weatherPlugin.localizations['weatherForecast']['failure'][language])
        self.complete_request()