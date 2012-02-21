#!/usr/bin/python
# -*- coding: utf-8 -*-

import cPickle
import MySQLdb as mdb
from uuid import uuid4


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
    return mdb.connect("localhost","root","6xtylm","googlesiri")


class Assistant(object):
    def __init__(self, assistantId=str.upper(str(uuid4())),speechId=str.upper(str(uuid4()))):
        self.assistantId = assistantId
        self.speechId = speechId
        self.censorSpeech = None
        self.timeZoneId = None
        self.language = None
        self.region = None


