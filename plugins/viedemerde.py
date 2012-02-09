#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as ET
import urllib2, urllib
from plugin import *


class vieDeMerde(Plugin):
    
    @register("fr-FR", "Vie.*(merde|merd)")
    def fuckMyLife(self, speech, language):
        vdm = None
        try:
            response = urllib2.urlopen("http://api.viedemerde.fr/1.0/view/random", timeout=3).read()
            vdm = ET.fromstring(response).find("vdms/vdm/texte")
        except:
            pass

        if vdm != None:
            self.say(vdm.text.replace("&quot;",'"'))
        else:
            self.say(u"Désolé, l'API Vie De Merde autorise très peu de requête.")
        self.complete_request()