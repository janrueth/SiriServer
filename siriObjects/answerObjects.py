#!/usr/bin/python
# -*- coding: utf-8 -*-

from siriObjects.baseObjects import AceObject, ClientBoundCommand


class SiriAnswerSnippet(AceObject):
    def __init__(self, answers=None):
        super(SiriAnswerSnippet, self).__init__("Snippet", "com.apple.ace.answer")
        self.answers = answers if answers != None else []
        self.confirmationOptions = None
    
    def to_plist(self):
        self.add_property('answers')
        self.add_property('confirmationOptions')
        return super(SiriAnswerSnippet, self).to_plist()

class SiriAnswer(AceObject):
    def __init__(self, title=None, lines=None):
        super(SiriAnswer, self).__init__("Object", "com.apple.ace.answer")
        self.title = title
        self.lines = lines if lines != None else []
    
    def to_plist(self):
        self.add_property('title')
        self.add_property('lines')
        return super(SiriAnswer, self).to_plist()

class SiriAnswerLine(AceObject):
    def __init__(self, text="", image=""):
        super(SiriAnswerLine, self).__init__("ObjectLine", "com.apple.ace.answer")
        self.text = text
        self.image = image
    
    def to_plist(self):
        self.add_property('text')
        self.add_property('image')
        return super(SiriAnswerLine, self).to_plist()