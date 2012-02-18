#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PluginManager import *

logging.basicConfig()

load_api_keys()
load_plugins()

lang = 'fr-FR'

while 1:
    try:
        speech = sys.stdin.readline().decode("utf-8")
    except:
        exit()
    (clazz, method) = getPlugin(speech, lang)
    print clazz
    print method
