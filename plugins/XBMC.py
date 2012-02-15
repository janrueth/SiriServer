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

from siriObjects.uiObjects import AddViews
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine

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
        
    def get_thumburl(self):
        return 'http://%s:%s/vfs/' % (self.host, self.port)

    def play(self,json,item):
        json.Playlist.Clear(playlistid=1)
        json.Playlist.Add(playlistid=1, item=item)
        json.Player.Open({ 'playlistid': 1 })

class XBMC(Plugin):	    

    def addPictureView(self,title,image_url):
        view = AddViews(self.refId, dialogPhase="Completion")
        ImageAnswer = AnswerObject(title=title,lines=[AnswerObjectLine(image=image_url)])
        view1 = AnswerSnippet(answers=[ImageAnswer])
        view.views = [view1]
        self.sendRequestWithoutAnswer(view)
        
    global xbmc
    xbmc = XBMC_object()
            
    @register("en-US", "(xbmc)|(xbmc.* [a-z]+)")
    def test2(self, speech, language):
        global xbmc
        if speech.lower() == 'xbmc':
            self.say("XBMC currently supports the following commands: play [movie or tv show], play latest episode of [tv show], play trailer for [movie] pause, stop, shut down, start and info.")
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
            elif command == 'update library' or command == 'scan':
                json.VideoLibrary.Scan()
            elif command == 'clean library':
                json.VideoLibrary.Clean()
            elif command == 'latest movies':
                recentMovies = json.VideoLibrary.GetRecentlyAddedMovies(properties=['playcount'])['movies']
                movieList = ''
                for movie in recentMovies:
                    if movie['playcount'] > 0:
                        watched = 'Watched: Yes'
                    else:
                        watched = 'Watched: No'
                    movieList = movieList + movie['label'] + '\n' + watched + '\n\n'
                self.say(movieList, "Here you go:")
            elif command == 'latest episodes':
                recentEpisodes = json.VideoLibrary.GetRecentlyAddedEpisodes(properties=['showtitle','season','episode','playcount'])['episodes']
                episodeList = ''
                for episode in recentEpisodes:
                    ep = '%s\nS%02dE%02d: %s\n' % (episode['showtitle'],episode['season'],episode['episode'],episode['label'])
                    if episode['playcount'] > 0:
                        watched = 'Watched: Yes'
                    else:
                        watched = 'Watched: No'
                    episodeList = episodeList + ep + watched + '\n\n'
                self.say(episodeList, "Here you go:")
            elif 'play trailer of' in command or 'play trailer for' in command or 'play trailer 4' in command:
                if 'play trailer of' in command:
                    title = command.replace('play trailer of ','')
                elif 'play trailer for' in command:
                    title = command.replace('play trailer for ', '')
                elif 'play trailer 4' in command:
                    title = command.replace('play trailer 4 ', '')
                result = json.VideoLibrary.GetMovies()
                stripped_title = ''.join(ch for ch in title if ch.isalnum()).lower()
                for movie in result['movies']:
                    if stripped_title in ''.join(ch for ch in movie['label'] if ch.isalnum()).lower():
                        movieid = movie['movieid']
                        trailer = json.VideoLibrary.GetMovieDetails(movieid=movieid, properties= ['trailer'])['moviedetails']['trailer']
                        break
                if trailer:
                    xbmc.play(json,{'file':trailer})
                else:
                    self.say("It seems that there is no trailer available for this movie.")
            elif 'play' in command or 'plate' in command or 'place' in command or 'played' in command or 'start' in command:
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
                        self.say('%s starting'%(matches[0]))
                        details = json.VideoLibrary.GetMovieDetails(movieid=movieid, properties= ['thumbnail','year','rating'])['moviedetails']
                        image_url = "%s%s" % (xbmc.get_thumburl(),details['thumbnail'])
                        title = "%s (%s) - %s/10" % (details['label'],details['year'],round(details['rating'],1))
                        self.addPictureView(title,image_url)
                        xbmc.play(json,{'movieid': movieid})
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
                            self.say(names,None)
                        else:
                            result = json.VideoLibrary.GetEpisodes(tvshowid=tvshowid,properties=['playcount','showtitle','season','episode'])
                            if latest_episode == True:
                                episode = result['episodes'][len(result['episodes'])-1]
                                episodeid = episode['episodeid']
                                play = True
                                if episode['playcount'] > 0:
                                    self.say("Warning: it seems that you already watched this episode.",None)
                            else: 
                                allwatched = True
                                for episode in result['episodes']:
                                    if episode['playcount'] == 0:
                                        episodeid=episode['episodeid']
                                        allwatched = False
                                        play = True
                                        break
                                if allwatched == True:
                                    self.say('There are no unwatched and/or new episodes of %s' %(title))
                                    play = False
                            if play == True:
                                details = json.VideoLibrary.GetTVShowDetails(tvshowid=tvshowid, properties= ['thumbnail','rating'])['tvshowdetails']
                                image_url = "%s%s" % (xbmc.get_thumburl(),details['thumbnail'])
                                title = "%s - %s/10" % (details['label'],round(details['rating'],1))
                                self.say('Playing %s, season %s, episode %s.' %(episode['showtitle'], episode['season'], episode['episode']))
                                self.addPictureView(title,image_url)
                                xbmc.play(json,{ 'episodeid': episodeid })
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
