#!/usr/bin/python
# -*- coding: utf-8 -*-

# randomfacts.py
#by Nate Li
#based on Casey "Nurfballs" Mullineaux's cat fact plugin

from random import randint
from plugin import *
import os, random



class randomfacts(Plugin):
    
    @register("en-GB","(.*random fact.*)|(.*something *.awesome.*)")
    @register("en-US","(.*random fact.*)|(.*something *.awesome.*)")
    def st_catfact(self, speech, language): 
        filename = "./plugins/randomfacts.txt"
        file = open(filename, 'r')
        #Get the total file size
        file_size = os.stat(filename)[6]
        #Seek to a place int he file which is a random distance away
        #Mod by the file size so that it wraps around to the beginning
        file.seek((file.tell()+random.randint(0, file_size-1))%file_size)
        #Dont use the first readline since it may fall in the middle of a line
        file.readline()
        #this will return the next (complete) line from the file
        line = file.readline()
        file.close
        #here is the random line
        self.say(line)             
        self.complete_request()


