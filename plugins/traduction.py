#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bing Translate
# Par Cédric Boverie (cedbv)
# Clé API nécessaire disponible sur https://be.ssl.bing.com/webmaster/Developers/

import re
import json
import urllib2, urllib
from plugin import *

APIKEY = APIKeyForAPI("bingtranslation")


class Translation(Plugin):
    
    res = {
        'translate': {
            'en-US': u"(Translate)(.*) in (.*)",
            'fr-FR': u"(Traduit|Traduire|Traduis)(.*) en (.*)",
        },
        'not_found': {
            'en-US': u"I don't know this language.",
            'fr-FR': u"Je ne connais pas cette langue.",
        },
        'error': {
            'en-US': u"I can't translate {0}",
            'fr-FR': u"Je n'arrive pas à traduire {0}",
        }
    }
    
    languages = {
        'fr-FR' : {
            'arabe' : 'ar',
            'bulgare' : 'gb',
            'catalan' : 'ca',
            'chinois' : 'zh-CHS',
            'chinois traditionnel' : 'zh-CHT',
            u'tchèque' : 'cs',
            'tcheque' : 'cs',
            'dannois' : 'da',
            'nerlandais' : 'nl',
            u'nérlandais' : 'nl',
            u'néerlandais' : 'nl',
            'anglais' : 'en',
            'estonien' : 'et',
            'finnois' : 'fi',
            u'français' : 'fr',
            'francais' : 'fr',
            'allemand' : 'de',
            'grec' : 'el',
            'haitien' : 'ht',
            u'haïtien' : 'ht',
            'hebreu' : 'he',
            u'hébreu' : 'he',
            'hindi' : 'hi',
            'hongrois' : 'hu',
            u'indonésien' : 'id',
            'indonesien' : 'id',
            'italien' : 'it',
            'japonais' : 'ja',
            u'coréen' : 'ko',
            'coreen' : 'ko',
            'letton' : 'lv',
            'lituanien' : 'lt',
            'norvegien' : 'no',
            u'norvégien' : 'no',
            'polonais' : 'pl',
            'portugais' : 'pt',
            'roumain' : 'ro',
            'russe' : 'ru',
            'slovaque' : 'sk',
            u'slovène' : 'sl',
            'slovene' : 'sl',
            'espagnol' : 'es',
            u'suédois' : 'sv',
            'suedois' : 'sv',
            'thai' : 'th',
            'thaï' : 'th',
            'turc' : 'tr',
            'ukrainien' : 'uk',
            'vietnamien' : 'vi',
            'flamand' : 'nl',
        }
    }

    @register("fr-FR", res["translate"]["fr-FR"])
    def translation(self, speech, language, regex):

        term = regex.group(2).strip()		
        lang = regex.group(3).strip()
        
        languages = self.languages
        res = self.res
        
        if lang in languages[language]:
            target = languages[language][lang]
        else:
            self.say(res["not_found"][language]);
            self.complete_request()
            return False

        traduction = None
        try:
            url = "http://api.bing.net/json.aspx?Query=%s&Translation.SourceLanguage=fr&Translation.TargetLanguage=%s&Version=2.2&AppId=%s&Sources=Translation" % (urllib.quote_plus(term.encode("utf-8")),target,APIKEY)
            response = urllib2.urlopen(url, timeout=3).read()
            jsonObj = json.loads(response);
            traduction = jsonObj["SearchResponse"]["Translation"]["Results"][0]["TranslatedTerm"]
        except:
            pass

        if traduction != None:
            self.say(traduction)
        else:
            error = res['error'][languages];
            self.say(error.format(term))
        self.complete_request()
