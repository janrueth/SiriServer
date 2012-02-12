#!/usr/bin/python
# -*- coding: utf-8 -*-


#from plugin import *
from oauth import oauth
from oauthtwitter import OAuthApi
import pprint
import ConfigParser

def getTwitterSession():
    config = ConfigParser.RawConfigParser()
    config.read('twitter.cfg')
    consumer = config.items("consumer")
    oauth = config.items("oauth")
    return OAuthApi(consumer[0][1], consumer[1][1], oauth[0][1], oauth[1][1])

class twitterPlugin(Plugin):
    def __init__(self, method, speech, language):
        super(Plugin, self).__init__()
        self.session = getTwitterSession()
     
    @register("en-US", ".*Tweet.*")
    def tweet(self, speech, language):
        response = self.ask("Do you want me to tweet: %s?" % speech)
        if response == yes:
            session.UpdateStatus(speech)
        self.complete_request()
