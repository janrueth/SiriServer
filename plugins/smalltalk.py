#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Joh Gerna

from plugin import *

class smalltalk(Plugin):
    
    @register("de-DE", "(.*Hallo.*)|(.*Hi.*Siri.*)")
    @register("en-US", "(.*Hello.*)|(.*Hi.*Siri.*)")
    @register("fr-FR", "(.*Bonjour.*)|(.*Salut.*Siri.*)")
    def st_hello(self, speech, language):
        if language == 'de-DE':
            self.say("Hallo.")
        elif language == 'fr-FR':
            self.say("Bonjour.")
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
            self.say("Siri.")
        else:
            self.say("Siri.")
        self.complete_request()

    @register("de-DE", "Wie geht es dir?")
    @register("en-US", "How are you?")
<<<<<<< HEAD
    @register("fr-FR", u"(.*Comment vas-tu.*)|(.*Comment Áa va.*)")
=======
    @register("fr-FR", u"(.*Comment vas-tu.*)|(.*Comment √ßa va.*)")
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
    def st_howareyou(self, speech, language):
        if language == 'de-DE':
            self.say("Gut danke der Nachfrage.")
        elif language == 'fr-FR':
            self.say("Bien, merci de demander.")
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
            self.say("De rien.")
        else:
            self.say("You are welcome.")
            self.say("This is my job.")
        self.complete_request()     
    
    @register("de-DE", "(.*m√∂chtest.*heiraten.*)|(.*willst.*heiraten.*)")
    @register("en-US", ".*Want.*marry*")
<<<<<<< HEAD
    @register("fr-FR", u"(.*m'Èpouser.*)|(.*marier.*moi.*)")
=======
    @register("fr-FR", u"(.*m'√©pouser.*)|(.*marier.*moi.*)")
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
    def st_marry_me(self, speech, language):
        if language == 'de-DE':
            self.say("Nein Danke, ich stehe auf das schwarze iPhone von Deinem Kollegen.")   
        elif language == 'fr-FR':
<<<<<<< HEAD
            self.say(u"Non merci. Je suis amoureux d'un autre tÈlÈphone.")                  
=======
            self.say(u"Non merci. Je suis amoureux d'un autre t√©l√©phone.")         
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
        else:
            self.say("No thank you, I'm in love with the black iPhone from you friend.")
        self.complete_request()

    @register("de-DE", ".*erz√§hl.*Witz.*")
    @register("en-US", ".*tell.*joke*")
    @register("fr-FR", ".*raconte.*blague.*")
    def st_tell_joke(self, speech, language):
        if language == 'de-DE':
<<<<<<< HEAD
            self.say("Zwei iPhones stehen an der Bar ... den Rest habe ich vergessen.")   
        elif language == 'fr-FR':
            self.say(u"Deux iPhones entrent dans un bar ... j'ai oubliÈ la suite.")         
=======
            self.say("Zwei iPhones stehen an der Bar ... den Rest habe ich vergessen.")
        elif language == 'fr-FR':
            self.say(u"Deux iPhones entrent dans un bar ... j'ai oubli√© la suite.")
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
        else:
            self.say("Two iPhones walk into a bar ... I forget the rest.")
        self.complete_request()

    @register("de-DE", ".*erz√§hl.*Geschichte.*")
    @register("en-US", ".*tell.*story*")
    @register("fr-FR", ".*raconte.*histoire.*")
    def st_tell_story(self, speech, language):
        if language == 'de-DE':
<<<<<<< HEAD
            self.say("Es war einmal ... nein, es ist zu albern")            
        elif language == 'fr-FR':
            self.say(u"Il Ètait une fois ... non c'est trop stupide")
=======
            self.say("Es war einmal ... nein, es ist zu albern")
        elif language == 'fr-FR':
            self.say(u"Il √©tait une fois ... non c'est trop stupide")
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
        else:
            self.say("Far far away, there was ... no, too stupid")
        self.complete_request()

    @register("de-DE", "(.*Was tr√§gst Du?.*)|(.*Was.*hast.*an.*)")
    @register("en-US", ".*what.*wearing*")
    @register("fr-FR", "(.*que.*porte.*)|(.*qu'est-ce-que.*porte.*)")
    def st_tell_clothes(self, speech, language):
        if language == 'de-DE':
<<<<<<< HEAD
            self.say("Das kleine schwarze oder war es das weiﬂe?")
            self.say("Bin morgends immer so neben der Spur.")  
=======
            self.say("Das kleine schwarze oder war es das wei√üe?")
            self.say("Bin morgends immer so neben der Spur.")
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
        elif language == 'fr-FR':
            self.say("Je ne sais pas mais je suis beau.")
        else:
            self.say("I guess the small black one, or was it white?")
        self.complete_request()

    @register("de-DE", ".*Bin ich dick.*")
    @register("en-US", ".*Am I fat*")
    @register("fr-FR", u"(.*ai l'air.*gros.*)|(.*suis.*gros.*)")
    def st_fat(self, speech, language):
        if language == 'de-DE':
<<<<<<< HEAD
            self.say("Dazu mˆchte ich nichts sagen.")
        elif language == 'fr-FR':
            self.say(u"Je prÈfËre ne pas rÈpondre.")
=======
            self.say("Dazu m√∂chte ich nichts sagen.")
        elif language == 'fr-FR':
            self.say(u"Je pr√©f√®re ne pas r√©pondre.")
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
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
        else:
            answer = self.ask(u"Who's there?")
            answer = self.ask(u"\"{0}\" who?".format(answer))
            self.say(u"Who is bugging me with knock knock jokes?")
        self.complete_request()

    @register("de-DE", ".*Antwort.*alle.*Fragen.*")
    @register("en-US", ".*Ultimate.*Question.*Life.*")
    @register("fr-FR", ".*question.*ultime.*vie.*")
    def st_anstwer_all(self, speech, language):
        if language == 'de-DE':
            self.say("42")            
        else:
            self.say("42")
        self.complete_request()

    @register("de-DE", ".*Ich liebe Dich.*")
    @register("en-US", ".*I love you.*")
    @register("fr-FR", ".*Je t'aime'.*")
    def st_love_you(self, speech, language):
        if language == 'de-DE':
            self.say("Oh. Sicher sagst Du das zu allen Deinen Apple-Produkten.")            
        else:
            self.say("Oh. Sure, I guess you say this to all your Apple products")
        self.complete_request()

    @register("de-DE", ".*Android.*")
    @register("en-US", ".*Android.*")
    @register("fr-FR", ".*Android.*")
    def st_android(self, speech, language):
        if language == 'de-DE':
            self.say("Ich denke da anders.")            
        else:
            self.say("I think different about that.")
        self.complete_request()

    @register("de-DE", ".*Test.*1.*2.*3.*")
    @register("en-US", ".*test.*1.*2.*3.*")
    @register("fr-FR", ".*test.*1.*2.*3.*")
    def st_123_test(self, speech, language):
        if language == 'de-DE':
            self.say("Ich kann Dich klar und deutlich verstehen.")            
        else:
            self.say("I can here you very clear.")
        self.complete_request()

    @register("de-DE", ".*Herzlichen.*Gl√ºckwunsch.*Geburtstag.*")
    @register("en-US", ".*Happy.*birthday.*")
    @register("fr-FR", "(.*Joyeux.*anniversaire.*)|(.*Bon.*anniversaire.*)")
    def st_birthday(self, speech, language):
        if language == 'de-DE':
            self.say("Ich habe heute Geburtstag?")
            self.say("Lass uns feiern!")       
        else:
            self.say("My birthday is today?")
            self.say("Lets make a party!")
        self.complete_request()

    @register("de-DE", ".*Warum.*bin ich.*Welt.*")
    @register("en-US", ".*Why.*I.*World.*")
    def st_why_on_world(self, speech, language):
        if language == 'de-DE':
            self.say("Das wei√ü ich nicht.")
            self.say("Ehrlich gesagt, frage ich mich das schon lange!")       
        else:
            self.say("I don't know that.")
            self.say("Ask my self this for a long time!")
        self.complete_request()

    @register("de-DE", ".*Ich bin m√ºde.*")
    @register("en-US", ".*I.*so.*tired.*")
<<<<<<< HEAD
    @register("fr-FR", u".*Je.*fatiguÈ.*")
=======
    @register("fr-FR", u".*Je.*fatigu√©.*")
>>>>>>> 5194b777e300be9728d1d71016f49e7e55b5252e
    def st_so_tired(self, speech, language):
        if language == 'de-DE':
            self.say("Ich hoffe, Du f√§hrst nicht gerade Auto!")            
        else:
            self.say("I hope you are not driving a car right now!")
        self.complete_request()

    @register("de-DE", ".*Sag mir.*Schmutzige.*")
    @register("en-US", ".*Tell me.*dirty*")
    @register("fr-FR", ".*parle.*salement")
    def st_dirty(self, speech, language):
        if language == 'de-DE':
            self.say("Humus. Kompost. Bims. Schlamm. Kies.")            
        else:
            self.say("Humus. Compost. Pumice. Mud. Gravel.")
        self.complete_request()
