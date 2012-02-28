#!/usr/bin/python
# -*- coding: utf-8 -*-

import cPickle,base64
import uuid 

db_type = "mysql"

__mysql_host__ = "localhost"
__mysql_user__ = "root"
__mysql_password__ = "pass"
__mysql_database__ = "googlesiri"

if db_type == "mysql":
    try:
        import MySQLdb as mdb
    except:
        print "You must install MySQLdb to use MySQL with SiriServer. Try python-mysql or easy_install"
        exit()

def setup():
    conn = getConnection()
    c = conn.cursor()
    c.execute("""CREATE DATABASE IF NOT EXISTS googlesiri DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;""")
    c.execute("""CREATE TABLE IF NOT EXISTS `assistants` (`id` int(255) unsigned NOT NULL AUTO_INCREMENT,`assistantId` text NOT NULL,`speechId` text NOT NULL,`censorSpeech` text NOT NULL,`timeZoneId` text NOT NULL,`language` text NOT NULL,`region` text NOT NULL,`firstName` text NOT NULL,`nickName` text NOT NULL,`date_created` datetime NOT NULL, PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;""")    
    c.close()
    conn.close()

def getConnection():
    return mdb.connect(__mysql_host__, __mysql_user__, __mysql_password__, __mysql_database__, use_unicode=True,charset='utf8')


class Assistant(object):
    def __init__(self):
        self.assistantId = None
        self.speechId= None    
        self.censorSpeech = None
        self.timeZoneId = None
        self.language = None
        self.region = None
        self.nickName = u''
        self.firstName=u''
