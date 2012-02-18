#!/usr/bin/python
# -*- coding: utf-8 -*-

# Use iPhone App API

import re
import xml.etree.ElementTree as ET
import urllib2, urllib
import random
from plugin import *


class vieDeMerde(Plugin):
    
    @register("fr-FR", ".*vie.*(merde|merd).*")
    def fuckMyLife(self, speech, language):
        vdm = None
        lang = language[:2]
        try:
            response = urllib2.urlopen("http://www.vdm-iphone.com/v8/{0}/random.php?cat=all&num_page=0".format(lang), timeout=5).read()
            xml = ET.fromstring(response)
            vdms = xml.findall("item")
            vdm = random.choice(vdms)
        except:
            pass

        if vdm != None:
            self.say(vdm.find("text").text)
            url = vdm.find("short_url").text.replace("//","")
            button = Button(text=u"Lire sur VDM", commands=[OpenLink(ref=url)])
            self.send_object(AddViews(self.refId, views=[button]))
        else:
            if language == "fr-FR":
                self.say(u"Désolé, aujourd'hui est une journée tellement merdique que je n'arrive pas pas à lire VDM.")
            
        self.complete_request()
