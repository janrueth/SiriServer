# Author: Gustavo Hoirisch, Pieter Janssens
#
#
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
# Note: This XBMC plugin is designed for XBMC RPC V3, this means that it works best with XBMC Eden and up.

from plugin import *
import urllib2, urllib, socket, struct, logging, re

try: 
    import jsonrpclib
except ImportError: 
    raise NecessaryModuleNotFound('XBMC plugin will not work: JSONRPCLIB not installed. To install, run "easy_install jsonrpclib"')
    

class XBMC_object():
    def __init__(self, host='appletv.local', port='8080', username=None, password=None, mac_address=None):
        self.username = username
        self.password = password
        self.port = port
        self.host = host
        self.mac_address = mac_address
        
    def get_url(self):
        return 'http://%s%s:%s' %(self.get_user_pass(), self.host, self.port)
        
    def get_user_pass(self):
        if self.username != None and self.password != None:
            return '%s:%s@' % (self.username, self.password)
        
        return ''

class XBMC(Plugin):
    global xbmc
    xbmc = XBMC_object()
            
    @register("en-US", "(xbmc)|(xbmc.* [a-z]+)")
    def test2(self, speech, language):
        global xbmc
        if speech.lower() == 'xbmc':
            self.say("XBMC currently supports the following commands: play [movie or tv show], pause, stop, shut down, start and info.")
        else:
            firstword, command=speech.split(' ',1)
            json = jsonrpclib.Server('%s/jsonrpc' % (xbmc.get_url()))
            if command == 'stop':
                try:
                    json.Player.Stop(playerid=1)
                except:
                    self.say('Nothing to stop...')
            elif command == 'play' or command == 'pause' or command == 'plate' or command == 'place' or command == 'pas' or command == 'paws':
                try:
                    json.Player.PlayPause(playerid=1)
                except:
                    self.say('Nothing to play/pause')
            elif 'play' in command or 'plate' in command or 'place' in command or 'played' in command or 'start' in command: #this elif needs to be located below command == 'play' part
                command, title=command.split(' ',1)
                if 'first occurrence' in title:
                    first_match = True
                    title = title.replace(' first occurrence', '')
                else:
                    first_match = False
                print 'Searching for: '+title
                result = json.VideoLibrary.GetMovies()
                stripped_title = ''.join(ch for ch in title if ch.isalnum()).lower()
                matches = []
                for movie in result['movies']:
                    if stripped_title in ''.join(ch for ch in movie['label'] if ch.isalnum()).lower():
                        movieid = movie['movieid']
                        matches.append(movie['label'])
                        if first_match == True:
                            break
                if len(matches) > 0:
                    if len(matches) > 1:
                        self.say("Found multiple matches for '%s':" %(title))
                        names = ''
                        for x in matches:
                            names = names + x + '\n' 
                        self.say(names, None)
                        self.say("To play the first one add 'first occurrence' at the end of your command")
                    else:
                        json.Playlist.Clear(playlistid=1)
                        json.Playlist.Add(playlistid=1, item={ 'movie' + 'id': movieid })
                        json.Player.Open({ 'playlistid': 1 })
                        self.say('%s starting'%(matches[0]))
                else:
                    result = json.VideoLibrary.GetTVShows()
                    tvmatches = []
                    
                    if 'thelatestepisodeof' in stripped_title:
                        stripped_title = stripped_title.replace('thelatestepisodeof','')
                        latest_episode = True
                    elif 'latestepisodeof' in stripped_title:
                        stripped_title = stripped_title.replace('latestepisodeof','')
                        latest_episode = True
                    elif 'latestepisode' in stripped_title:
                        stripped_title = stripped_title.replace('latestepisode','')
                        latest_episode = True
                    else:
                        latest_episode = False
                    
                    for tvshow in result['tvshows']:
                        if stripped_title in ''.join(ch for ch in tvshow['label'] if ch.isalnum()).lower():
                            tvshowid = tvshow['tvshowid']
                            matches.append(tvshow['label'])
                    if len(matches) > 0:
                        if len(matches) > 1:
                            self.say("Found multiple matches for '%s':" %(title))
                            names = ''
                            for x in matches:
                                names = names + x + '\n'
                            self.say(names, None)
                        else:
                            result = json.VideoLibrary.GetEpisodes(tvshowid=tvshowid,properties=['playcount','showtitle','season','episode'])
                            print (result['episodes'])
                            print (len(result['episodes']))
                            if latest_episode == True:
                                episode = result['episodes'][len(result['episodes'])-1]
                                if episode['playcount'] > 0:
                                    self.say("Warning: it seems that you already watched this episode.")
                                self.say('Playing %s, season %s, episode %s.' %(episode['showtitle'], episode['season'], episode['episode']))
                                json.Playlist.Clear(playlistid=1)
                                json.Playlist.Add(playlistid=1, item={ 'episode' + 'id': episode['episodeid'] })
                                json.Player.Open({ 'playlistid': 1 })
                            else: 
                                allwatched = True
                                for episode in result['episodes']:
                                    if episode['playcount'] == 0:
                                        episodeid=episode['episodeid']
                                        self.say('Playing %s, season %s, episode %s.' %(episode['showtitle'], episode['season'], episode['episode']))
                                        json.Playlist.Clear(playlistid=1)
                                        json.Playlist.Add(playlistid=1, item={ 'episode' + 'id': episodeid })
                                        json.Player.Open({ 'playlistid': 1 })
                                        allwatched = False
                                        break
                                if allwatched == True:
                                    self.say('There are no unwatched and/or new episodes of %s' %(title))
                    else:
                        self.say('No movies or TV shows matching: %s.' % (title))
            elif command == 'info':
                self.say("XBMC URL: %s" %(xbmc.get_url()), None)
                info = """username: %s\
                password: %s\
                hostname: %s\
                port: %s """ %(xbmc.username, xbmc.password, xbmc.host, xbmc.port)
                self.say(info, None)
            elif command == 'shut down' or command == 'shutdown' or command == 'turn off':
                self.say("XBMC going down")
                json.System.Shutdown()
            elif command == 'boot' or command == 'start' or command == 'boot up':
                addr_byte = xbmc.mac_address.split(':')
                hw_addr = struct.pack('BBBBBB',
                int(addr_byte[0], 16),
                int(addr_byte[1], 16),
                int(addr_byte[2], 16),
                int(addr_byte[3], 16),
                int(addr_byte[4], 16),
                int(addr_byte[5], 16))
                msg = '\xff' * 6 + hw_addr * 16
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                s.sendto(msg, ("255.255.255.255", 9))
            else:
                self.say("XBMC command not recognized: %s."%(command))
        self.complete_request()
