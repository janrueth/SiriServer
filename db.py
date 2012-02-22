#!/usr/bin/python
# -*- coding: utf-8 -*-

import cPickle,base64
import MySQLdb as mdb
import uuid 


__database__ = "database.sqlite3"

def setup():
    conn = getConnection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS `assistants` (
  `id` int(255) unsigned NOT NULL AUTO_INCREMENT,
  `assistantId` text NOT NULL,
  `speechId` text NOT NULL,
  `censorSpeech` text NOT NULL,
  `timeZoneId` text NOT NULL,
  `language` text NOT NULL,
  `region` text NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
        """)
    #conn.commit()
    c.close()
    conn.close()

def getConnection():
    return mdb.connect("localhost","root","","googlesiri")


class Assistant(object):
    def __init__(self):
        self.assistantId = None
        self.speechId= None    
        self.censorSpeech = None
        self.timeZoneId = None
        self.language = None
        self.region = None

def adaptAssistant(assistant):
    return base64.encodestring(cPickle.dumps(assistant))

def convertAssistant(fromDB):
    return cPickle.loads(base64.decodestring(fromDB))
