# Author: Gustavo Hoirisch
#
#
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#

from plugin import *
import urllib2, urllib, jsonrpclib, socket, struct

class XBMC_object():
    def __init__(self, host='localhost', port='8080', username=None, password=None):
        self.username = username
        self.password = password
        self.port = port
        self.host = host
        
    def get_url(self):
        return 'http://%s%s:%s' %(self.get_user_pass(), self.host, self.port)
        
    def get_user_pass(self):
        if self.username != None and self.password != None:
            return '%s:%s' % (username, password)
        
        return ''

class XBMC(Plugin):
    global xbmc
    xbmc = XBMC_object()
    
    @register("en-US", "(xbmc)|(xbmc.* [a-z]+)")
    def test2(self, speech, language):
        global xbmc
        command = re.match(".* ([a-z, ]+)$", speech, re.IGNORECASE)
        if command != None:
            command = command.group(1).strip()
            json = jsonrpclib.Server('%s/jsonrpc' % (xbmc.get_url()))
            if command == 'stop':
                json.Player.Stop(playerid=1)
            elif command == 'play' or command == 'pause' or command == 'plate' or command == 'place':
                json.Player.PlayPause(playerid=1)
            elif command == 'info':
                self.say("XBMC URL: %s" %(xbmc.get_url()))
            else:
                self.say("XBMC command not recognized: %s."%(command))
            
        else:
            self.say("XBMC currently supports the following commands: play, pause, stop and info.")
        
        self.complete_request()
