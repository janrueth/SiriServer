#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: WebScript
#Todo: Nothing that I know
#For: SiriServer
#Commands: The same as in original Wolfram Alpha in Siri
#If you find bug: email me - admin@game-host.eu

import re, urlparse
import urllib2, urllib
import json
from urllib2 import urlopen
from xml.dom import minidom

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine


APPID = APIKeyForAPI("wolframalpha")



class wolfram(Plugin):
    
    @register("de-DE", "(Was ist [a-zA-Z0-9]+)|(Wer ist [a-zA-Z0-9]+)|(Wie viel [a-zA-Z0-9]+)|(Was war [a-zA-Z0-9]+)|(Wer ist [a-zA-Z0-9]+)|(Wie lang [a-zA-Z0-9]+)|(Was ist [a-zA-Z0-9]+)|(Wie weit [a-zA-Z0-9]+)|(Wann ist [a-zA-Z0-9]+)|(Zeig mir [a-zA-Z0-9]+)|(Wie hoch [a-zA-Z0-9]+)|(Wie tief [a-zA-Z0-9]+)")     
    @register("en-US", "(What is [a-zA-Z0-9]+)|(Who is [a-zA-Z0-9]+)|(How many [a-zA-Z0-9]+)|(What was [a-zA-Z0-9]+)|(Who's [a-zA-Z0-9]+)|(How long [a-zA-Z0-9]+)|(What's [a-zA-Z0-9]+)|(How far [a-zA-Z0-9]+)|(When is [a-zA-Z0-9]+)|(Show me [a-zA-Z0-9]+)|(How high [a-zA-Z0-9]+)|(How deep [a-zA-Z0-9]+)")
    def wolfram(self, speech, language):
        wolframQuestion = speech.replace('who is ','').replace('what is ','').replace('what was ','').replace('Who is ','').replace('What is ','').replace('What was ','').replace('wer ist ','').replace('was ist ', '').replace('Wer ist ','').replace('Was ist ', '').replace('Wie viel ','How much ').replace('Wie lang ','How long ').replace('Wie weit ','How far ').replace('Wann ist ','When is ').replace('Zeig mir ','Show me ').replace('Wie hoch ','How high ').replace('Wie tief ','How deep ').replace('ist','is').replace('der','the').replace('die','the').replace('das','the').replace('wie viel ','how much ').replace('wie lang ','how long ').replace('wie weit ','how far ').replace('wann ist ','when is ').replace('zeig mir ','show me ').replace('wie hoch ','how high ').replace('wie tief ','how deep ').replace('ist','is').replace('der','the').replace('die','the').replace('das','the').replace(' ', '%20').replace(u'ä', 'a').replace(u'ö', 'o').replace(u'ü', 'u').replace(u'ß', 's')
        wolfram_alpha = 'http://api.wolframalpha.com/v1/query.jsp?input=%s&appid=%s' % (wolframQuestion, APPID)
        print wolfram_alpha
        dom = minidom.parse(urlopen(wolfram_alpha))
        count_wolfram = 0
        wolfram0 = 12
        wolfram_pod0 = 12
        wolfram0_img = 12
        wolfram1 = 12
        wolfram_pod1 = 12
        wolfram1_img = 12
        wolfram2 = 12
        wolfram_pod2 = 12
        wolfram2_img = 12
        wolfram3 = 12
        wolfram_pod3 = 12
        wolfram3_img = 12
        wolfram4 = 12
        wolfram_pod4 = 12
        wolfram4_img = 12
        wolfram5 = 12
        wolfram_pod5 = 12
        wolfram5_img = 12
        wolfram6 = 12
        wolfram_pod6 = 12
        wolfram6_img = 12
        wolfram7 = 12
        wolfram_pod7 = 12
        wolfram7_img = 12
        wolfram8 = 12
        wolfram_pod8 = 12
        wolfram8_img = 12
        wolframAnswer = 12
        wolframAnswer2 = 12
        wolframAnswer3 = 12
        wolframAnswer4 = 12
        wolframAnswer8 = 12
        query_list = dom.getElementsByTagName('queryresult')[-1]
        query_type = query_list.getAttribute('error')
        for node in dom.getElementsByTagName('queryresult'):
            for pod in node.getElementsByTagName('pod'):
                xmlTag = dom.getElementsByTagName('plaintext')[count_wolfram].toxml()
                xmlTag2 = dom.getElementsByTagName('subpod')[count_wolfram]
                xmlData=xmlTag.replace('<plaintext>','').replace('</plaintext>','')
                if count_wolfram == 0:
                    if xmlData == "<plaintext/>":
                        image_list = dom.getElementsByTagName('img')[count_wolfram]
                        image_type = image_list.getAttribute('src')
                        wolfram0 = image_type
                        wolfram0_img = 1
                    else:
                        wolfram0 = xmlData
                    wolfram_pod0 = pod.getAttribute('title')
                elif count_wolfram == 1:
                    if xmlData == "<plaintext/>":
                        image_list = dom.getElementsByTagName('img')[count_wolfram]
                        image_type = image_list.getAttribute('src')
                        wolfram1 = image_type
                        wolfram1_img = 1
                    else:
                        wolfram1 = xmlData
                    wolfram_pod1 = pod.getAttribute('title')
                elif count_wolfram == 2:
                    if xmlData == "<plaintext/>":
                        image_list = dom.getElementsByTagName('img')[count_wolfram]
                        image_type = image_list.getAttribute('src')
                        wolfram2 = image_type
                        wolfram2_img = 1
                    else:
                        wolfram2 = xmlData
                    wolfram_pod2 = pod.getAttribute('title')
                elif count_wolfram == 3:
                    if xmlData == "<plaintext/>":
                        image_list = dom.getElementsByTagName('img')[count_wolfram]
                        image_type = image_list.getAttribute('src')
                        wolfram3 = image_type
                        wolfram3_img = 1
                    else:
                        wolfram3 = xmlData
                    wolfram_pod3 = pod.getAttribute('title')
                elif count_wolfram == 4:
                    if xmlData == "<plaintext/>":
                        image_list = dom.getElementsByTagName('img')[count_wolfram]
                        image_type = image_list.getAttribute('src')
                        wolfram4 = image_type
                        wolfram4_img = 1
                    else:
                        wolfram4 = xmlData
                    wolfram_pod4 = pod.getAttribute('title')
                elif count_wolfram == 5:
                    wolfram5 = xmlData
                    wolfram_pod5 = pod.getAttribute('title')
                elif count_wolfram == 6:
                    wolfram6 = xmlData
                    wolfram_pod6 = pod.getAttribute('title')
                elif count_wolfram == 7:
                    wolfram7 = xmlData
                    wolfram_pod7 = pod.getAttribute('title')
                elif count_wolfram == 8:
                    wolfram8 = xmlData
                    wolfram_pod8 = pod.getAttribute('title')
                count_wolfram += 1
        if language == 'de-DE':
            self.say("Dies könnte Ihre Frage zu beantworten:")
        else:
            self.say("This might answer your question:")
        view = AddViews(self.refId, dialogPhase="Completion")
        if wolfram_pod0 != 12:
            if wolfram0_img == 1:
                wolframAnswer = AnswerObject(title=wolfram_pod0,lines=[AnswerObjectLine(image=wolfram0)])
            else:
                wolframAnswer = AnswerObject(title=wolfram_pod0,lines=[AnswerObjectLine(text=wolfram0)])
        else:
            print wolfram_pod0
        if wolfram_pod1 != 12:
            if wolfram1_img == 1:
                wolframAnswer1 = AnswerObject(title=wolfram_pod1,lines=[AnswerObjectLine(image=wolfram1)])
            else:
                wolframAnswer1 = AnswerObject(title=wolfram_pod1,lines=[AnswerObjectLine(text=wolfram1)])
        else:
            print wolfram_pod1
        if wolfram_pod2 != 12:
            if wolfram2_img == 1:
                wolframAnswer2 = AnswerObject(title=wolfram_pod2,lines=[AnswerObjectLine(image=wolfram2)])
            else:
                wolframAnswer2 = AnswerObject(title=wolfram_pod2,lines=[AnswerObjectLine(text=wolfram2)])
        else:
            print wolfram_pod2
        if wolfram_pod3 != 12:
            if wolfram3_img == 1:
                wolframAnswer3 = AnswerObject(title=wolfram_pod3,lines=[AnswerObjectLine(image=wolfram3)])
            else:
                wolframAnswer3 = AnswerObject(title=wolfram_pod3,lines=[AnswerObjectLine(text=wolfram3)])
        else:
            print wolfram_pod3
        if wolfram_pod4 != 12:
            if wolfram4_img == 1:
                wolframAnswer4 = AnswerObject(title=wolfram_pod4,lines=[AnswerObjectLine(image=wolfram4)])
            else:
                wolframAnswer4 = AnswerObject(title=wolfram_pod4,lines=[AnswerObjectLine(text=wolfram4)])
        else:
            print wolfram_pod4
        if wolfram_pod8 != 12:
            if wolfram8_img == 1:
                wolframAnswer8 = AnswerObject(title=wolfram_pod8,lines=[AnswerObjectLine(image=wolfram8)])
            else:
                wolframAnswer8 = AnswerObject(title=wolfram_pod8,lines=[AnswerObjectLine(text=wolfram8)])
        if wolfram_pod0 == 12:
            if APPID == "":
                self.say("Sorry I can't process your request. Your APPID is not set! Please register free dev account at http://wolframalpha.com and edit line 21 with you APPID.")
            else:
                if language == 'de-DE':
                    self.say("Nichts hat sich auf Ihre Anfrage!")
                else:
                    self.say("Nothing was found for your query!")
            self.complete_request()
            view1 = 0
        elif wolfram_pod1 == 12:
            view1 = AnswerSnippet(answers=[wolframAnswer])
        elif wolfram_pod2 == 12:
            view1 = AnswerSnippet(answers=[wolframAnswer, wolframAnswer1])
        elif wolfram_pod3 == 12:
            view1 = AnswerSnippet(answers=[wolframAnswer, wolframAnswer1, wolframAnswer2])
        elif wolfram_pod4 == 12:
            view1 = AnswerSnippet(answers=[wolframAnswer, wolframAnswer1, wolframAnswer2, wolframAnswer3])
        elif wolfram_pod8 == 12:
            view1 = AnswerSnippet(answers=[wolframAnswer, wolframAnswer1, wolframAnswer2, wolframAnswer3, wolframAnswer4])
        else:
            view1 = AnswerSnippet(answers=[wolframAnswer, wolframAnswer1, wolframAnswer2, wolframAnswer3, wolframAnswer4, wolframAnswer8])
        view.views = [view1]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()
