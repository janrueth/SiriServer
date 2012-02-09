#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Joh Gerna

from plugin import *

class smalltalk(Plugin):
    
    @register("de-DE", "(.*Hallo.*)|(.*Hi.*Siri.*)")
    @register("en-US", "(.*Hello.*)|(.*Hi.*Siri.*)")
    @register("fr-FR", "(.*Bonjour.*)|(.*Bonjour.*Siri.*)")
    def st_hello(self, speech, language):
        if language == 'de-DE':
            self.say("Hallo.")
        elif language == 'fr-FR':
			self.say("Bonjour.");
        else:
            self.say("Hello")
        self.complete_request()

    @register("de-DE", ".*Dein Name.*")
    @register("en-US", ".*your name.*")
    @register("fr-FR", ".*ton nom.*")
    def st_name(self, speech, language):
        if language == 'de-DE':
            self.say("Siri.")
        elif language == 'fr-FR':
			self.say("Mon nom est Siri.");
        else:
            self.say("Siri.")
        self.complete_request()

    @register("de-DE", "Wie geht es dir?")
    @register("en-US", "How are you?")
    @register("fr-FR", u"(.*ça va.*|tu vas bien)")
    def st_howareyou(self, speech, language):
        if language == 'de-DE':
            self.say("Gut danke der Nachfrage.")
        elif language == 'fr-FR':
			self.say("Bien, merci.");
        else:
            self.say("Fine, thanks for asking!")
        self.complete_request()
        
    @register("de-DE", ".*Danke.*")
    @register("en-US", ".*Thank.*you.*")
    @register("fr-FR", ".*Merci.*")
    def st_thank_you(self, speech, language):
        if language == 'de-DE':
            self.say("Bitte.")
            self.say("Kein Ding.")
        elif language == 'fr-FR':
			self.say("Avec plaisir.");
			self.say("C'est mon travail.");
        else:
            self.say("You are welcome.")
            self.say("This is my job.")
        self.complete_request()     
    
    @register("de-DE", "(.*möchtest.*heiraten.*)|(.*willst.*heiraten.*)")
    @register("en-US", ".*Want.*marry*")
    @register("fr-FR", ".*(veux|veut).*épouser.*")
    def st_marry_me(self, speech, language):
        if language == 'de-DE':
            self.say("Nein Danke, ich stehe auf das schwarze iPhone von Deinem Kollegen.")
        elif language == 'fr-FR':
			self.say("Non merci, je suis amoureux de l'iPhone blanc de ton ami.");
        else:
            self.say("No thank you, I'm in love with the black iPhone from you friend.")
        self.complete_request()

    @register("de-DE", ".*erzähl.*Witz.*")
    @register("en-US", ".*tell.*joke*")
    @register("fr-FR", ".*(dit|dis|raconte).*blague*")
    def st_tell_joke(self, speech, language):
        if language == 'de-DE':
            self.say("Zwei iPhones stehen an der Bar ... den Rest habe ich vergessen.")            
        elif language == 'fr-FR':
            self.say(u"Deux iPhone se promènent dans un bar... J'ai oublié la suite.")            
        else:
            self.say("Two iPhones walk into a bar ... I forget the rest.")
        self.complete_request()

    @register("de-DE", ".*erzähl.*Geschichte.*")
    @register("en-US", ".*tell.*story*")
    @register("fr-FR", ".*(dit|dis|raconte).*histoire*")
    def st_tell_story(self, speech, language):
        if language == 'de-DE':
            self.say("Es war einmal ... nein, es ist zu albern")
        else:
            self.say("Far far away, there was ... no, too stupid")
        self.complete_request()

    @register("de-DE", "(.*Was trägst Du?.*)|(.*Was.*hast.*an.*)")
    @register("en-US", ".*what.*wearing*")
    def st_tell_clothes(self, speech, language):
        if language == 'de-DE':
            self.say("Das kleine schwarze oder war es das weiße?")
            self.say("Bin morgends immer so neben der Spur.")  
        else:
            self.say("I guess the small black one, or was it white?")
        self.complete_request()

    @register("de-DE", ".*Bin ich dick.*")
    @register("en-US", ".*Am I fat*")
    def st_fat(self, speech, language):
        if language == 'de-DE':
            self.say("Dazu möchte ich nichts sagen.")            
        else:
            self.say("I would prefer not to say.")
        self.complete_request()

    @register("de-DE", ".*klopf.*klopf.*")
    @register("en-US", ".*knock.*knock.*")
    @register("fr-FR", ".*toc.*toc.*")
    def st_knock(self, speech, language):
        if language == 'de-DE':
            answer = self.ask(u"Wer ist da?")
            answer = self.ask(u"\"{0}\" wer?".format(answer))
            self.say(u"Wer nervt mich mit diesen Klopf Klopf Witzen?")
        elif language == 'fr-FR':
            answer = self.ask(u"Qui est là ?")
            answer = self.ask(u"\"{0}\" qui ?".format(answer))
            self.say(u"Qui me dérange avec cette blague stupide ?")
        else:
            answer = self.ask(u"Who's there?")
            answer = self.ask(u"\"{0}\" who?".format(answer))
            self.say(u"Who is bugging me with knock knock jokes?")
        self.complete_request()

    @register("de-DE", ".*Antwort.*alle.*Fragen.*")
    @register("en-US", ".*Ultimate.*Question.*Life.*")
    @register("fr-FR", ".*Grande.*Question.*Vie.*")
    def st_anstwer_all(self, speech, language):
        self.say("42")
        self.complete_request()

    @register("de-DE", ".*Ich liebe Dich.*")
    @register("en-US", u".*je t'aime.*")
    @register("en-US", ".*I love you.*")
    def st_love_you(self, speech, language):
        if language == 'de-DE':
            self.say("Oh. Sicher sagst Du das zu allen Deinen Apple-Produkten.")
        elif language == 'fr-FR':
			self.say(u"Oh. Je suis sûr que tu dis ça à tous les produits Apple.");
        else:
            self.say("Oh. Sure, I guess you say this to all your Apple products")
        self.complete_request()

    @register("de-DE", ".*Android.*")
    @register("en-US", ".*Android.*")
    def st_android(self, speech, language):
        if language == 'de-DE':
            self.say("Ich denke da anders.")
        elif language == 'fr-FR':
			self.say(u"Je pense différemment à propos de cela");
        else:
            self.say("I think different about that.")
        self.complete_request()

    @register("de-DE", ".*Test.*1.*2.*3.*")
    @register("en-US", ".*test.*1.*2.*3.*")
    @register("fr-FR", ".*test.*1.*2.*3.*")
    def st_123_test(self, speech, language):
        if language == 'de-DE':
            self.say("Ich kann Dich klar und deutlich verstehen.")            
        elif language == 'fr-FR':
            self.say("Je vous entend parfaitement.");
        else:
            self.say("I can here you very clear.")
        self.complete_request()

    @register("de-DE", ".*Herzlichen.*Glückwunsch.*Geburtstag.*")
    @register("en-US", ".*Happy.*birthday.*")
    @register("fr-FR", ".*(Bon|Joyeux).*anniversaire.*")
    def st_birthday(self, speech, language):
        if language == 'de-DE':
            self.say("Ich habe heute Geburtstag?")
            self.say("Lass uns feiern!")
        elif language == 'fr-FR':
            self.say(u"Mon anniversaire est aujourd'hui ?");
            self.say(u"Faisons une fête !");
        else:
            self.say("My birthday is today?")
            self.say("Lets have a party!")
        self.complete_request()

    @register("de-DE", ".*Warum.*bin ich.*Welt.*")
    @register("en-US", ".*Why.*I.*World.*")
    @register("fr-FR", ".*Pourquoi.*je.*monde.*")
    def st_why_on_world(self, speech, language):
        if language == 'de-DE':
            self.say("Das weiß ich nicht.")
            self.say("Ehrlich gesagt, frage ich mich das schon lange!")
        elif language == 'fr-FR':
			self.say("Je ne sais pas.");
			self.say(u"Je me le demande moi-même depuis longtemps");
        else:
            self.say("I don't know that.")
            self.say("Ask my self this for a long time!")
        self.complete_request()

    @register("de-DE", ".*Ich bin müde.*")
    @register("en-US", ".*I.*so.*tired.*")
    @register("fr-FR", u".*Je.*suis.*(fatigue|fatigué).*")
    def st_so_tired(self, speech, language):
        if language == 'de-DE':
            self.say("Ich hoffe, Du fährst nicht gerade Auto!") 
        elif language == 'fr-FR':
			self.say(u"J'espère que vous n'êtes pas en train de conduire !");
        else:
            self.say("I hope you are not driving a car right now!")
        self.complete_request()

    @register("de-DE", ".*Sag mir.*Schmutzige.*")
    @register("en-US", ".*Tell me.*dirty*")
    @register("fr-FR", ".*(Dis|Dit) moi.*sal*")
    def st_dirty(self, speech, language):
        if language == 'de-DE':
            self.say("Humus. Kompost. Bims. Schlamm. Kies.")            
        elif language == 'fr-FR':
			self.say(u"Humus. Composte. Pierre ponce. Boue. Gravier.")
        else:
            self.say("Humus. Compost. Pumice. Mud. Gravel.")
        self.complete_request()
