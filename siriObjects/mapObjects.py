#!/usr/bin/python
# -*- coding: utf-8 -*-

from siriObjects.baseObjects import AceObject, ClientBoundCommand

class SiriMapItemSnippet(AceObject):
    def __init__(self, userCurrentLocation=True, items=None):
        super(SiriMapItemSnippet, self).__init__("MapItemSnippet", "com.apple.ace.localsearch")
        self.userCurrentLocation = userCurrentLocation
        self.items = items
    
    def to_plist(self):
        self.add_property('userCurrentLocation')
        self.add_property('items')
        return super(SiriMapItemSnippet, self).to_plist()

class SiriLocation(AceObject):
    def __init__(self, label="", street="", city="", stateCode="", countryCode="", postalCode="", latitude="", longitude=""):
        super(SiriLocation, self).__init__("Location", "com.apple.ace.system")
        self.label = label
        self.street = street
        self.city = city
        self.stateCode = stateCode
        self.countryCode = countryCode
        self.postalCode = postalCode
        self.latitude = latitude
        self.longitude = longitude
    
    def to_plist(self):
        self.add_property('label')
        self.add_property('street')
        self.add_property('city')
        self.add_property('stateCode')
        self.add_property('countryCode')
        self.add_property('postalCode')
        self.add_property('latitude')
        self.add_property('longitude')
        return super(SiriLocation, self).to_plist()

class SiriMapItem(AceObject):
    def __init__(self, label="", location=None, detailType="BUSINESS_ITEM"):
        super(SiriMapItem, self).__init__("MapItem", "com.apple.ace.localsearch")
        self.label = label
        self.detailType = detailType
        self.location = location if location != None else SiriLocation()
    
    def to_plist(self):
        self.add_property('label')
        self.add_property('detailType')
        self.add_property('location')
        return super(SiriMapItem, self).to_plist()