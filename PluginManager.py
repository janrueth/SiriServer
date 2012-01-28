
import os
import re

from plugin import Plugin, __criteria_key__
from types import FunctionType


pluginPath = "plugins"

config_file = "plugins.conf"

plugins = dict()

def load_plugins():
    with open(config_file, "r") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            # just load the whole shit...
            __import__(pluginPath+"."+line,  globals(), locals(), [], -1)
            
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


def getPlugin(speech, language):
    if language in plugins:
        for (regex, clazz, method) in plugins[language]:
            if regex.match(speech) != None:
                return (clazz, method)
    return None
                



