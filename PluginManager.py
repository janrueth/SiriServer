
import os
import re
import logging

from plugin import Plugin, __criteria_key__, NecessaryModuleNotFound, ApiKeyNotFoundException
from types import FunctionType


logger = logging.getLogger("logger")
pluginPath = "plugins"

__config_file__ = "plugins.conf"
__apikeys_file__ = "apiKeys.conf"



plugins = dict()
apiKeys = dict()

def load_plugins():
    with open(__config_file__, "r") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            # just load the whole shit...
            try:
                __import__(pluginPath+"."+line,  globals(), locals(), [], -1)
            except NecessaryModuleNotFound as e:
                logger.critical("Failed loading plugin due to missing module: "+str(e))
            except ApiKeyNotFoundException as e:
                logger.critical("Failed loading plugin due to missing API key: "+str(e))
            except:
                logger.exception("Plugin loading failed")
            
    # as they are loaded in the order in the file we will have the same order in __subclasses__()... I hope

    for clazz in Plugin.__subclasses__():
        # look at all functions of a class lets filter them first
        methods = filter(lambda x: type(x) == FunctionType, clazz.__dict__.values())
        # now we check if the method is decorated by register
        for method in methods:
            if __criteria_key__ in method.__dict__:
                criterias = method.__dict__[__criteria_key__]
                for lang, regex in criterias.items():
                    if not lang in plugins:
                        plugins[lang] = []
                    # yeah... save the regex, the clazz and the method, shit just got loaded...
                    plugins[lang].append((regex, clazz, method))


def reload_api_keys():
    apiKeys = dict()
    load_api_keys()

def load_api_keys():
    with open(__apikeys_file__, "r") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            kv = line.split("=", 1)
            try:
                apiName = str.lower(kv[0]).strip()
                kv[1] = kv[1].strip()
                apiKey = kv[1][1:len(kv[1])-1] #stip the ""
                apiKeys[apiName] = apiKey
            except:
                logger.critial("There was an error parsing an API in the line: "+ line)

def getAPIKeyForAPI(APIname):
    apiName = str.lower(APIname) 
    if apiName in apiKeys:
        return apiKeys[apiName]
    return None

def getPlugin(speech, language):
    if language in plugins:
        for (regex, clazz, method) in plugins[language]:
            if regex.match(speech) != None:
                return (clazz, method)
    return (None, None)
                



