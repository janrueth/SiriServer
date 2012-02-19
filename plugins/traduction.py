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
            'en-US': u"I can't translate {0} in {1}",
            'fr-FR': u"Je n'arrive pas à traduire {0} en {1}",
        }
    }
    
    #see
    # langcode => http://api.microsofttranslator.com/V2/Ajax.svc/GetLanguagesForTranslate?appId={APIKEY}
    # and http://api.microsofttranslator.com/V2/Ajax.svc/GetLanguageNames?locale={languages}&languageCodes={langcode}&appId={APIKEY}
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
            u'thaï' : 'th',
            'turc' : 'tr',
            'ukrainien' : 'uk',
            'vietnamien' : 'vi',
            'flamand' : 'nl',
        },
        'en-US': {
            "arabic": "ar", "czech": "cs","check": "cs","czech language": "cs","danish": "da","german": "de","english": "en","estonian": "et","finnish": "fi","french": "fr","dutch": "nl","greek": "el","hebrew": "he","haitian creole": "ht","hungarian": "hu","indonesian": "id","italian": "it","japanese": "ja","korean": "ko","lithuanian": "lt","latvian": "lv","norwegian": "no","polish": "pl","portuguese": "pt","romanian": "ro","spanish": "es","russian": "ru","slovak": "sk","slovene": "sl","swedish": "sv","thai": "th","turkish": "tr","ukranian": "uk","vietnamese": "vi","simplified chinese": "zh-CHS","traditional chinese": "zh-CHT","chinese": "zh-CHT"
        }
    }

    @register("fr-FR", res["translate"]["fr-FR"])
    @register("en-US", res["translate"]["en-US"])
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
            error = res["error"][language];
            self.say(error.format(term,lang))
        self.complete_request()
