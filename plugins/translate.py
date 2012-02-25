#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author: SNXRaven (Jonathon Nickols)
# This requires that you have installed bingtrans module from: https://github.com/bahn/bingtrans
# This requires that you get your own api key from: http://www.bing.com/developers/

import bingtrans
import re

from plugin import *
bing_api_key = APIKeyForAPI("bing")
bingtrans.set_app_id(bing_api_key)
class bing_translate(Plugin):
    
    @register("en-US", "(Translate [a-zA-Z0-9]+)")
    def snx_translate(self, speech, language):
        match = re.match(u"Translate (.*\D.*) from (english|spanish|french|italian|estonian|finnish|Greek|Arabic|czech|dutch|hebrew|russian|polish|portuguese|romanian|swedish|turkish|indonesian|hungarian) to (english|spanish|french|italian|estonian|finnish|greek|arabic|czech|dutch|hebrew|russian|polish|portuguese|romanian|swedish|turkish|indonesian|hungarian)", speech, re.IGNORECASE)
        text = match.group(1)
        lang1 = match.group(2).replace('english', 'en').replace('spanish', 'es').replace('french', 'fr').replace('italian','it').replace('estonian','et').replace('finnish','fi').replace('greek','el').replace('arabic','ar').replace('czech' ,'cs').replace('dutch' ,'nl').replace('hebrew' ,'he').replace('russian' ,'ru').replace('polish' ,'pl').replace('portuguese' ,'pt').replace('romanian' ,'ro').replace('swedish' ,'sv').replace('turkish' ,'tr').replace('indonesian' ,'id').replace('hungarian' ,'id')
        lang2 = match.group(3).replace('english', 'en').replace('spanish', 'es').replace('french', 'fr').replace('italian','it').replace('estonian','et').replace('finnish','fi').replace('greek','el').replace('arabic','ar').replace('czech' ,'cs').replace('dutch' ,'nl').replace('hebrew' ,'he').replace('russian' ,'ru').replace('polish' ,'pl').replace('portuguese' ,'pt').replace('romanian' ,'ro').replace('swedish' ,'sv').replace('turkish' ,'tr').replace('indonesian' ,'id').replace('hungarian' ,'id')
        self.say("Here is your translation:\n")
        self.say(bingtrans.translate(text, lang1, lang2), ' ')
        self.complete_request()

  