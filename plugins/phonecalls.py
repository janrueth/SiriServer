#!/usr/bin/python
# -*- coding: utf-8 -*-

from plugin import *
from siriObjects.baseObjects import ObjectIsCommand, RequestCompleted
from siriObjects.contactObjects import PersonSearch, PersonSearchCompleted
from siriObjects.uiObjects import AddViews, DisambiguationList, ListItem, AssistantUtteranceView
from siriObjects.systemObjects import SendCommands, StartRequest, ResultCallback, Person, PersonAttribute
from siriObjects.phoneObjects import PhoneCall
import re

responses = {
'notFound': 
    {'de-DE': u"Entschuldigung, ich konnte niemanden in deinem Telefonbuch finden der so heißt",
     'en-US': u"Sorry, I did not find a match in your phone book"
    },
'devel':
    {'de-DE': u"Entschuldigung, aber diese Funktion befindet sich noch in der Entwicklungsphase",
     'en-US': u"Sorry this feature is still under development"
    },
 'select':
    {'de-DE': u"Wen genau?", 
     'en-US': u"Which one?"
    },
'selectNumber':
    {'de-DE': u"Welche Telefonnummer für {0}",
     'en-US': u"Which phone one for {0}"
    },
'callPersonSpeak':
    {'de-DE': u"Rufe {0}, {1} an.",
     'en-US': u"Calling {0}, {1}."
    },
'callPerson': 
    {'de-DE': u"Rufe {0}, {1} an: {2}",
     'en-US': u"Calling {0}, {1}: {2}"
    }
}

numberTypesLocalized= {
'_$!<Mobile>!$_': {'en-US': u"mobile", 'de-DE': u"Handynummer"},
'iPhone': {'en-US': u"iPhone", 'de-DE': u"iPhone-Nummer"},
'_$!<Home>!$_': {'en-US': u"home", 'de-DE': u"Privatnummer"},
'_$!<Work>!$_': {'en-US': u"work", 'de-DE': u"Geschäftsnummer"},
'_$!<Main>!$_': {'en-US': u"main", 'de-DE': u"Hauptnummer"},
'_$!<HomeFAX>!$_': {'en-US': u"home fax", 'de-DE': u'private Faxnummer'},
'_$!<WorkFAX>!$_': {'en-US': u"work fax", 'de-DE': u"geschäftliche Faxnummer"},
'_$!<OtherFAX>!$_': {'en-US': u"_$!<OtherFAX>!$_", 'de-DE': u"_$!<OtherFAX>!$_"},
'_$!<Pager>!$_': {'en-US': u"pager", 'de-DE': u"Pagernummer"},
'_$!<Other>!$_':{'en-US': u"other phone", 'de-DE': u"anderes Telefon"}
}

namesToNumberTypes = {
'de-DE': {'mobile': "_$!<Mobile>!$_", 'handy': "_$!<Mobile>!$_", 'zuhause': "_$!<Home>!$_", 'privat': "_$!<Home>!$_", 'arbeit': "_$!<Work>!$_"},
'en-US': {'work': "_$!<Work>!$_",'home': "_$!<Home>!$_", 'mobile': "_$!<Mobile>!$_"}
}

speakableDemitter={
'en-US': u", or ",
'de-DE': u', oder '}

errorNumberTypes= {
'de-DE': u"Ich habe dich nicht verstanden, versuch es bitte noch einmal.",
'en-US': u"Sorry, I did not understand, please try again."
}

errorNumberNotPresent= {
'de-DE': u"Ich habe diese {0} von {1} nicht, aber eine andere.",
'en-US': u"Sorry, I don't have a {0} number from {1}, but another."
}

errorOnCallResponse={'en-US':
                     [{'dialogIdentifier':u"PhoneCall#airplaneMode",
                       'text': u"Your phone is in airplane mode.",
                       'code': 1201},
                      {'dialogIdentifier': u"PhoneCall#networkUnavailable",
                       'text': u"Uh, I can't seem to find a good connection. Please try your phone call again when you have cellular access.",
                       'code': 1202},
                      {'dialogIdentifier': u"PhoneCall#invalidNumber",
                       'text': u"Sorry, I can't call this number.",
                       'code': 1203},
                      {'dialogIdentifier': u"PhoneCall#fatalResponse",
                       'text': u"Oh oh, I can't make your phone call.",
                       'code': -1}],
                     'de-DE':
                     [{'dialogIdentifier':u"PhoneCall#airplaneMode",
                       'text': u"Dein Telefon ist im Flugmodus.",
                       'code': 1201},
                      {'dialogIdentifier': u"PhoneCall#networkUnavailable",
                       'text': u"Oh je! Ich kann im Moment keine gute Verbindung bekommen. Versuch es noch einmal, wenn du wieder Funkempfang hast.",
                       'code': 1202},
                      {'dialogIdentifier': u"PhoneCall#invalidNumber",
                       'text': u"Ich kann diese Nummer leider nicht anrufen.",
                       'code': 1203},
                      {'dialogIdentifier': u"PhoneCall#fatalResponse",
                       'text': u"Tut mir leid, Ich, ich kann momentan keine Anrufe tätigen.",
                       'code': -1}]
}

class phonecallPlugin(Plugin):

    def searchUserByName(self, personToLookup):
        search = PersonSearch(self.refId)
        search.scope = PersonSearch.ScopeLocalValue
        search.name = personToLookup
        answerObj = self.getResponseForRequest(search)
        if ObjectIsCommand(answerObj, PersonSearchCompleted):
            answer = PersonSearchCompleted(answerObj)
            return answer.results if answer.results != None else []
        else:
            raise StopPluginExecution("Unknown response: {0}".format(answerObj))
        return []
           
    def getNumberTypeForName(self, name, language):
        # q&d
        if name != None:
            if name.lower() in namesToNumberTypes[language]:
                return namesToNumberTypes[language][name.lower()]
            else:
                for key in numberTypesLocalized.keys():
                    if numberTypesLocalized[key][language].lower() == name.lower():
                        return numberTypesLocalized[key][language]
        return None
    
    def findPhoneForNumberType(self, person, numberType, language):         
        # first check if a specific number was already requested
        phoneToCall = None
        if numberType != None:
            # try to find the phone that fits the numberType
            phoneToCall = filter(lambda x: x.label == numberType, person.phones)
        else:
            favPhones = filter(lambda y: y.favoriteVoice if hasattr(y, "favoriteVoice") else False, person.phones)
            if len(favPhones) == 1:
                phoneToCall = favPhones[0]
        if phoneToCall == None:
            # lets check if there is more than one number
            if len(person.phones) == 1:
                if numberType != None:
                    self.say(errorNumberNotPresent.format(numberTypesLocalized[numberType][language], person.fullName))
                phoneToCall = person.phones[0]
            else:
                # damn we need to ask the user which one he wants...
                while(phoneToCall == None):
                    rootView = AddViews(self.refId, temporary=False, dialogPhase="Clarification", scrollToTop=False, views=[])
                    sayit = responses['selectNumber'][language].format(person.fullName)
                    rootView.views.append(AssistantUtteranceView(text=sayit, speakableText=sayit, listenAfterSpeaking=True,dialogIdentifier="ContactDataResolutionDucs#foundAmbiguousPhoneNumberForContact"))
                    lst = DisambiguationList(items=[], speakableSelectionResponse="OK...", listenAfterSpeaking=True, speakableText="", speakableFinalDemitter=speakableDemitter[language], speakableDemitter=", ",selectionResponse="OK...")
                    rootView.views.append(lst)
                    for phone in person.phones:
                        numberType = phone.label
                        item = ListItem()
                        item.title = ""
                        item.text = u"{0}: {1}".format(numberTypesLocalized[numberType][language], phone.number)
                        item.selectionText = item.text
                        item.speakableText = u"{0}  ".format(numberTypesLocalized[numberType][language])
                        item.object = phone
                        item.commands.append(SendCommands(commands=[StartRequest(handsFree=False, utterance=numberTypesLocalized[numberType][language])]))
                        lst.items.append(item)
                    answer = self.getResponseForRequest(rootView)
                    numberType = self.getNumberTypeForName(answer, language)
                    if numberType != None:
                        matches = filter(lambda x: x.label == numberType, person.phones)
                        if len(matches) == 1:
                            phoneToCall = matches[0]
                        else:
                            self.say(errorNumberTypes[language])
                    else:
                        self.say(errorNumberTypes[language])
        return phoneToCall
             
    
    def call(self, phone, person, language):
        root = ResultCallback(commands=[])
        rootView = AddViews("", temporary=False, dialogPhase="Completion", views=[])
        root.commands.append(rootView)
        rootView.views.append(AssistantUtteranceView(text=responses['callPerson'][language].format(person.fullName, numberTypesLocalized[phone.label][language], phone.number), speakableText=responses['callPersonSpeak'][language].format(person.fullName, numberTypesLocalized[phone.label][language]), dialogIdentifier="PhoneCall#initiatePhoneCall", listenAfterSpeaking=False))
        rootView.callbacks = []
        
        # create some infos of the target
        personAttribute=PersonAttribute(data=phone.number, displayText=person.fullName, obj=Person())
        personAttribute.object.identifer = person.identifier
        call = PhoneCall("", recipient=phone.number, faceTime=False, callRecipient=personAttribute)
        
        rootView.callbacks.append(ResultCallback(commands=[call]))
        
        call.callbacks = []
        # now fill in error messages (airplanemode, no service, invalidNumber, fatal)
        for i in range(4):
            errorRoot = AddViews(None, temporary=False, dialogPhase="Completion", scrollToTop=False, views=[])
            errorRoot.views.append(AssistantUtteranceView(text=errorOnCallResponse[language][i]['text'], speakableText=errorOnCallResponse[language][i]['text'], dialogIdentifier=errorOnCallResponse[language][i]['dialogIdentifier'], listenAfterSpeaking=False))
            call.callbacks.append(ResultCallback(commands=[errorRoot], code=errorOnCallResponse[language][i]['code']))
            
        self.complete_request([root])

    def presentPossibleUsers(self, persons, language):
        root = AddViews(self.refId, False, False, "Clarification", [], [])
        root.views.append(AssistantUtteranceView(responses['select'][language], responses['select'][language], "ContactDataResolutionDucs#disambiguateContact", True))
        lst = DisambiguationList([], "OK!", True, "OK!", speakableDemitter[language], ", ", "OK!")
        root.views.append(lst)
        for person in persons:
            item = ListItem(person.fullName, person.fullName, [], person.fullName, person)
            item.commands.append(SendCommands([StartRequest(False, "^phoneCallContactId^=^urn:ace:{0}".format(person.identifier))]))
            lst.items.append(item)
        return root
    
    @register("de-DE", "ruf. (?P<name>[\w ]+).*(?P<type>arbeit|zuhause|privat|mobil|handy.*|iPhone.*|pager)? an")
    @register("en-US", "(make a )?call (to )?(?P<name>[\w ]+).*(?P<type>work|home|mobile|main|iPhone|pager)?")
    def makeCall(self, speech, language, regex):
        personToCall = regex.group('name')
        numberType = str.lower(regex.group('type')) if type in regex.groupdict() else None
        numberType = self.getNumberTypeForName(numberType, language)
        persons = self.searchUserByName(personToCall)
        personToCall = None
        if len(persons) > 0:
            if len(persons) == 1:
                personToCall = persons[0]
            else:
                identifierRegex = re.compile("\^phoneCallContactId\^=\^urn:ace:(?P<identifier>.*)")
                #  multiple users, ask user to select
                while(personToCall == None):
                    strUserToCall = self.getResponseForRequest(self.presentPossibleUsers(persons, language))
                    self.logger.debug(strUserToCall)
                    # maybe the user clicked...
                    identifier = identifierRegex.match(strUserToCall)
                    if identifier:
                        strUserToCall = identifier.group('identifier')
                        self.logger.debug(strUserToCall)
                    for person in persons:
                        if person.fullName == strUserToCall or person.identifier == strUserToCall:
                            personToCall = person
                    if personToCall == None:
                        # we obviously did not understand him.. but probably he refined his request... call again...
                        self.say(errorNumberTypes[language])
                    
            if personToCall != None:
                self.call(self.findPhoneForNumberType(personToCall, numberType, language), personToCall, language)
                return # complete_request is done there
        self.say(responses['notFound'][language])                         
        self.complete_request()
    
