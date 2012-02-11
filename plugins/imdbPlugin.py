#!/usr/bin/python
# -*- coding: utf-8 -*-
# IMDb Plugin
# Par Cédric Boverie (cedbv)
# Requires IMDbPy. Install IMDbPY or download it from http://imdbpy.sourceforge.net

import re
from plugin import *

from siriObjects.uiObjects import AddViews
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine

try:
   from imdb import IMDb
   import imdb.helpers
except ImportError:
   raise NecessaryModuleNotFound("IMDb library not found. Please install IMDbPy library! e.g. sudo easy_install IMDbPy (or sudo apt-get install python-imdbpy)")


class imdbPlugin(Plugin):
    
    res = {
        'who_is': {
            'fr-FR': u"(Qui (joue|a joue|a joué) dans le film|Qui joue dans|.*acteurs? de|.*acteurs? du film|Qui (es|est|étais|etais|était|etait) dans le film) (.*)",
        },
        'search_actor': {
            'fr-FR': u"Je recherche les acteurs du film {0}...",
        },
        'here_actor': {
            'fr-FR': u"Voici les acteurs du film {0} : ",
        },
        'no_actor': {
            'fr-FR': u"Je ne trouve pas les acteurs du film {0}.",
        },
        'when_is': {
            'fr-FR': u"(.*sorti .*film|.*date.*film) (.*)",
        },
        'search_date': {
            'fr-FR': u"Je recherche l'année de sortie du film {0}...",
        },
        'here_date': {
            'fr-FR': u"{0} est sorti en {1}.",
        },
        'no_date': {
            'fr-FR': u"Je ne trouve pas l'année de sortie du film {0}.",
        },
        'ratings': {
            'fr-FR': u"(.*(regarder|regardé|voir|vaut|vaux).*film) (.*)",
        },
        'search_ratings': {
            'fr-FR': u"Je recherche la notation du film {0}...",
        },
        'here_ratings': {
            'fr-FR': u"{0} est noté {1} sur 10.",
        },
        'no_ratings': {
            'fr-FR': u"Je ne trouve pas la notation du film {0}.",
        },
        'director': {
            'fr-FR': u"(.*(réalisé|realisé|realise|r(é|e)alisai(s|t)).*film) (.*)",
        },
        'search_director': {
            'fr-FR': u"Je recherche le réalisateur du film {0}...",
        },
        'here_director': {
            'fr-FR': u"{0} a été réalisé par {1}.",
        },
        'no_director': {
            'fr-FR': u"Je ne trouve pas le réalisateur du film {0}.",
        },
        'cover': {
            'fr-FR': u"(.*(affiche|la fiche).*film) (.*)",
        },
        'search_cover': {
            'fr-FR': u"Je recherche l'affiche du film {0}...",
        },
        'here_cover': {
            'fr-FR': u"Voici l'affiche du film {0} :",
        },
        'no_cover': {
            'fr-FR': u"Je ne trouve pas l'affiche du film {0}.",
        },
        'dont_find_movie': {
            'fr-FR': u"Je ne trouve pas le film {0}",
        },
    }

    def searchMovie(self, title, language):
        ia = IMDb()
        search_result = ia.search_movie(title.encode("utf-8"))
        if not search_result:
            dontfind = self.res["dont_find_movie"][language];
            self.say(dontfind.format(title))
            self.complete_request()
            return None
        infos = search_result[0]
        ia.update(infos)
        return infos

    @register("fr-FR", res["who_is"]["fr-FR"])
    def actors(self, speech, language, regex):

        query = regex.group(regex.lastindex).strip()
        search_actor = self.res["search_actor"][language]
        self.say(search_actor.format(query))
        infos = self.searchMovie(query,language)
        
        if infos != None:
            try:
                hereactor = self.res["here_actor"][language];
                self.say(hereactor.format(infos["title"]))
                actors = ""
                for people in infos["cast"]:
                    actors += people["name"] + ", \n"
                self.say(actors)
            except:
                noactor = self.res["no_actor"][language];
                self.say(noactor.format(infos["title"]))

        self.complete_request()
        

    @register("fr-FR", res["when_is"]["fr-FR"])
    def releasedate(self, speech, language, regex):

        query = regex.group(regex.lastindex).strip()
        search_date = self.res["search_date"][language]
        self.say(search_date.format(query))
        infos = self.searchMovie(query,language)
        
        if infos != None:
            try:
                here_date = self.res["here_date"][language];
                self.say(here_date.format(infos["title"],infos["year"]))
            except:
                nodate = self.res["no_date"][language];
                self.say(nodate.format(infos["title"]))

        self.complete_request()

    @register("fr-FR", res["ratings"]["fr-FR"])
    def movierating(self, speech, language, regex):

        query = regex.group(regex.lastindex).strip()
        search_ratings = self.res["search_ratings"][language]
        self.say(search_ratings.format(query))
        infos = self.searchMovie(query,language)
        
        if infos != None:
            try:
                here_ratings = self.res["here_ratings"][language];
                self.say(here_ratings.format(infos["title"],str(infos['rating'])))
            except:
                noratings = self.res["no_ratings"][language];
                self.say(noratings.format(infos["title"]))

        self.complete_request()

    @register("fr-FR", res["director"]["fr-FR"])
    def moviedirector(self, speech, language, regex):

        query = regex.group(regex.lastindex).strip()
        search_director = self.res["search_director"][language]
        self.say(search_director.format(query))
        infos = self.searchMovie(query,language)
        
        if infos != None:
            try:
                here_director = self.res["here_director"][language];
                self.say(here_director.format(infos["title"],infos["director"][0]))
            except:
                nodirector = self.res["no_director"][language];
                self.say(nodirector.format(infos["title"]))

        self.complete_request()

    @register("fr-FR", res["cover"]["fr-FR"])
    def moviecover(self, speech, language, regex):

        query = regex.group(regex.lastindex).strip()
        search = self.res["search_cover"][language]
        self.say(search.format(query))
        infos = self.searchMovie(query,language)
        
        ImageURL = None
        if infos != None:
            try:
                here = self.res["here_cover"][language];
                self.say(here.format(infos["title"]))
                ImageURL = infos["cover url"]
            except:
                no = self.res["no_cover"][language];
                self.say(no.format(infos["title"]))

        if ImageURL != None:
            ImageUrlBig = imdb.helpers.fullSizeCoverURL(infos)
            if ImageUrlBig != None:
                ImageURL = ImageUrlBig
            view = AddViews(self.refId, dialogPhase="Completion")
            ImageAnswer = AnswerObject(title=infos["title"],lines=[AnswerObjectLine(image=ImageURL)])
            view1 = AnswerSnippet(answers=[ImageAnswer])
            view.views = [view1]
            self.sendRequestWithoutAnswer(view)

        self.complete_request()
