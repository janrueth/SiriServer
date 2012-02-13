import sys
from PluginManager import *

logging.basicConfig()

load_api_keys()
load_plugins()

lang = 'fr-FR'

while 1:
    speech = sys.stdin.readline()
    (clazz, method) = getPlugin(speech, lang)
    print clazz
    print method
