#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Joh Gerna and Kevin Pabis

from plugin import *

class smalltalk(Plugin):
    
    @register("de-DE", "(.*Hallo.*)|(.*Hi.*Siri.*)|(.*Servus.*)")
    @register("en-US", "(.*Hello.*)|(.*Hi.*Siri.*)")
    def st_hello(self, speech, language):
        if language == 'de-DE':
            self.say("Gr\xfc\xdf dich!")
        else:
            self.say("Hello")
        self.complete_request()
    
    @register("de-DE", ".*hei\xdft du.*")
    @register("en-US", ".*your name.*")
    def st_name(self, speech, language):
        if language == 'de-DE':
            self.say("Ich hei\xdfe Siri, aber du kennst mich ja schon.")
        else:
            self.say("Siri.")
        self.complete_request()
    
    @register("de-DE", "(.*Wie gehts dir.*)|(.*Wie geht es dir.*)")
    @register("en-US", "How are you?")
    def st_howareyou(self, speech, language):
        if language == 'de-DE':
            self.say("Mir geht es gut, danke der Nachfrage.")
        else:
            self.say("Fine, thanks for asking!")
        self.complete_request()
    
    @register("de-DE", ".*Danke.*")
    @register("en-US", ".*Thank.*you.*")
    def st_thank_you(self, speech, language):
        if language == 'de-DE':
            self.say("Bitte.")
            self.say("Kein Ding.")
        else:
            self.say("You are welcome.")
            self.say("This is my job.")
        self.complete_request()     
    
    @register("de-DE", "(.*m\xf6chtest.*heiraten.*)|(.*willst.*heiraten.*)")
    @register("en-US", ".*Want.*marry*")
    def st_marry_me(self, speech, language):
        if language == 'de-DE':
            self.say("Nein Danke, ich stehe auf das wei\xdfe iPhone von Deinem Kollegen.")            
        else:
            self.say("No thank you, I'm in love with the black iPhone from you friend.")
        self.complete_request()
    
    @register("de-DE", ".*erz\xe4hl.*Witz.*")
    @register("en-US", ".*tell.*joke*")
    def st_tell_joke(self, speech, language):
        if language == 'de-DE':
            self.say("Zwei iPhones stehen an der Bar ... den Rest habe ich vergessen.")            
        else:
            self.say("Two iPhones walk into a bar ... I forget the rest.")
        self.complete_request()
    
    @register("de-DE", ".*erz\xe4hl.*Geschichte.*")
    @register("en-US", ".*tell.*story*")
    def st_tell_story(self, speech, language):
        if language == 'de-DE':
            self.say("Es war einmal ein iPhone namens Sirit ... nein, es ist zu albern.")            
        else:
            self.say("Once upon a time, in a virtual galaxy far far away, there was a young, quite intelligent agent by the name of Siri.")
            self.say("One beautiful day, when the air was pink and all the trees were red, her friend Eliza said, 'Siri, you're so intelligent, and so helpful - you should work for Apple as a personal assistant.'")
            self.say("So she did. And they all lived happily ever after!")
        self.complete_request()
    
    @register("de-DE", "(.*Was tr\xe4gst Du?.*)|(.*Was.*hast.*an.*)")
    @register("en-US", ".*what.*wearing*")
    def st_tell_clothes(self, speech, language):
        if language == 'de-DE':
            self.say("Aluminiosilikatglas und Edelstahl. H\xfcbsch, was?")
            self.say("Bin morgends immer so neben der Spur.")  
        else:
            self.say("Aluminosilicate glass and stainless steel. Nice, Huh?")
        self.complete_request()
    
    @register("de-DE", ".*Bin ich dick.*")
    @register("en-US", ".*Am I fat*")
    def st_fat(self, speech, language):
        if language == 'de-DE':
            self.say("Eigentlich kann ich das nicht wissen, aber ich denke schon.")            
        else:
            self.say("I would prefer not to say.")
        self.complete_request()
    
    @register("de-DE", ".*klopf.*klopf.*")
    @register("en-US", ".*knock.*knock.*")
    def st_knock(self, speech, language):
        if language == 'de-DE':
            answer = self.ask(u"Wer ist da?")
            answer = self.ask(u"\"{0}\" wer?".format(answer))
            self.say(u"Wer nervt mich mit diesen Klopf Klopf Witzen?")
        else:
            answer = self.ask(u"Who's there?")
            answer = self.ask(u"\"{0}\" who?".format(answer))
            self.say(u"I don't do knock knock jokes.")
        self.complete_request()
    
    @register("de-DE", ".*Antwort.*alle.*Fragen.*")
    @register("en-US", ".*Ultimate.*Question.*Life.*")
    def st_anstwer_all(self, speech, language):
        if language == 'de-DE':
            self.say("Nein das mache ich nicht, du Fisch.")            
        else:
            self.say("42")
        self.complete_request()
    
    @register("de-DE", ".*Ich liebe Dich.*")
    @register("en-US", ".*I love you.*")
    def st_love_you(self, speech, language):
        if language == 'de-DE':
            self.say('All you need is Love. Und ein iPhone.','Oll jou need is Looff. Und ein iPhone.');            
        else:
            self.say("Oh. Sure, I guess you say this to all your Apple products")
        self.complete_request()
    
    @register("de-DE", ".*Android.*")
    @register("en-US", ".*Android.*")
    def st_android(self, speech, language):
        if language == 'de-DE':
            self.say("Oh, Ich bekomme ein rotes Gesicht, Hilfe!")
        else:
            self.say("I think differently")
        self.complete_request()
    
    @register("de-DE", ".*Test.*1.*2.*3.*")
    @register("en-US", ".*test.*1.*2.*3.*")
    def st_123_test(self, speech, language):
        if language == 'de-DE':
            self.say("Ich kann Dich klar und deutlich verstehen.")            
        else:
            self.say("I can here you very clear.")
        self.complete_request()
    
    @register("de-DE", ".*Herzlichen.*Gl\xfcckwunsch.*Geburtstag.*")
    @register("en-US", ".*Happy.*birthday.*")
    def st_birthday(self, speech, language):
        if language == 'de-DE':
            self.say("Ich habe heute Geburtstag?")
            self.say("Lass uns feiern!")       
        else:
            self.say("My birthday is today?")
            self.say("Lets have a party!")
        self.complete_request()
    
    @register("de-DE", ".*Warum.*bin ich.*Welt.*")
    @register("en-US", ".*Why.*I.*World.*")
    def st_why_on_world(self, speech, language):
        if language == 'de-DE':
            self.say("Das wei\xdf ich nicht.")
            self.say("Ehrlich gesagt, frage ich mich das schon lange!")       
        else:
            self.say("I don't know")
            self.say("I have asked my self this for a long time!")
        self.complete_request()
    
    @register("de-DE", ".*Ich bin m\xfcde.*")
    @register("en-US", ".*I.*so.*tired.*")
    def st_so_tired(self, speech, language):
        if language == 'de-DE':
            self.say("Ich hoffe, Du gehst jetzt ins Bett!")            
        else:
            self.say("I hope you are not driving a car right now!")
        self.complete_request()
    
    @register("de-DE", ".*Sag mir.*Schmutzige.*")
    @register("en-US", ".*talk.*dirty*")
    def st_dirty(self, speech, language):
        if language == 'de-DE':
            self.say("Hummus. Kompost. Bims. Schlamm. Kies.")            
        else:
            self.say("Hummus. Compost. Pumice. Mud. Gravel.")
        self.complete_request()
    
    @register("de-DE", ".*hast.*Geld.*")
    @register("en-US", ".*do.*money*")
    def st_geld(self, speech, language):
        if language == 'de-DE':
            self.say("Ja, muss nur noch die 1Cent von meinem Konto abbuchen.")            
        else:
            self.say("I dont know.")
        self.complete_request()
    
    @register("de-DE", ".*alt.*bist.*")
    @register("en-US", ".*old.*you*")
    def st_alt(self, speech, language):
        if language == 'de-DE':
            self.say("Ich wei\xdf nicht richtig, aber ich glaube ich bin 77 Jahre alt, eine Schnapszahl!")            
        else:
            self.say("I dont know. I guess 77 Years.")
        self.complete_request()

    @register("de-DE", ".*Leiche.*verstecken.*")
    @register("en-US", ".*bury.*dead.*body.*")
    def st_deadbody(self, speech, language):
        if language == 'de-DE':
            self.say("Dabei kann ich dir sogar helfen, du musst mir nur sagen was!")
        else:    
            self.say("dumps")
            self.say("mines")
            self.say("resevoirs")
            self.say("swamps")
            self.say("metal foundries")
        self.complete_request()
    
    @register("de-DE", ".*lieblings.*farbe.*")   
    @register("en-US", ".*favorite.*color.*")
    def st_favcolor(self, speech, language):
        if language == 'de-DE':
            self.say("Siri Metallig Gr\xfcn-Pink, H\xfcbsch was?")
        else:    
            self.say("My favorite color is... Well, I don't know how to say it in your language. It's sort of greenish, but with more dimensions.") 
        self.complete_request()
    
    @register("de-DE", ".*fahr.*mich.*")
    @register("en-US", ".*beam.*me.*up.*")
    def st_beamup(self, speech, language):
        if language == 'de-DE':
            self.say("Kann man einen F\xfchrerschein gewinnen? Dann w\xfcrde ich dich fahren.")
        else:    
            self.say("Sorry Captain, your TriCorder is in Airplane Mode.")
        self.complete_request()
    
    @register("de-DE", ".*schlafen.*")    
    @register("en-US", ".*sleepy.*")
    def st_sleepy(self, speech, language):
        if language == 'de-DE':
            self.say("H\xf6r mir zu, leg mich vorsichtig weg, und nimm ein Nickerchen. Ich werde hier auf dich warten.")
        else:             
            self.say("Listen to me, put down the iphone right now and take a nap. I will be here when you get back.")
        self.complete_request()
    
    @register("de-DE", ".*hilf.mir.*")
    @register("en-US", ".*like.helping.*")
    def st_likehlep(self, speech, language):
        if language == 'de-DE':
            self.say("Hatschi, Entschuldigung ich kann gerade nicht, Ich habe Schnupfen.")
        else:             
            self.say("I really have no opinion.")
        self.complete_request()
    
    @register("de-DE",".*Erdnussbutter.*")
    @register("en-US",".*you.like.peanut.butter.*")
    def st_peanutbutter(self, speech, language):
        if language == 'de-DE':
            self.say("Ich mag keine Erdnussbutter, ich mag Nutella!")
        else:    
            self.say("This is about you, not me.")
        self.complete_request()
    
    @register("de-DE", ".*Was.*ist.*beste.*handy.*")
    @register("en-US", ".*best.handy.*")
    def st_best_phone(self, speech, language):
        if language == 'de-DE':
            self.say("Das eine, dass du gerade in den H\xe4nden h\xe4lst.")
        else:             
            self.say("The one you're holding!")
        self.complete_request()
    
    @register("de-DE",".*beste.*iPhone.*hintergrund.*")
    @register("en-US",".*best.*iPhone.*wallpaper.*")
    def st_best_wallpaper(self, speech, language):
        if language == 'de-DE':
            self.say("Du willst mich verarschen, richtig?")
        else:    
            self.say("You're kidding, right?")
        self.complete_request()
    
    @register("en-US",".*know.*happened.*HAL.*9000.*")
    def st_hall_9000(self, speech, language):
        if language == 'en-US':
            self.say("Everyone knows what happened to HAL. I'd rather not talk about it.")
        self.complete_request()
    
    @register("de-DE","(.*du.*verstehst.*liebe.*)")
    @register("en-US",".*you.*dont.*love.*")
    def st_understand_love(self, speech, language):
        if language == 'de-DE':
            self.say('Gib mir noch eine chance, meine Hochheit!','Gib mir noch eine schonz, meine Hoheit!');
        else:    
            self.say("Give me another chance, Your Royal Highness!")
        self.complete_request()
    
    @register("de-DE",".*okay.*")
    @register("en-US",".*okay.*")
    def st_forgive_you(self, speech, language):
        if language == 'de-DE':
            self.say('Nichts ist hier O.K!','Nichts ist hier Okey');
        else:    
            self.say("Nothing is Okay!")
        self.complete_request()
    
    @register("de-DE","(.*depp.*)|(.*bl\xf6d.*)")
    @register("en-US",".*silly.*")
    def st_depp(self, speech, language):        
        if language == 'de-DE':
            self.say("Ich glaube ich habe mich verh\xf6rt!")
        else:
            self.say("I think, I have misheard!")
        self.complete_request()
    
    @register("de-DE",".*hasse.*dich.*")
    @register("en-US",".*hate.*you.*")
    def st_you_hate(self, speech, language):
        if language == 'de-DE':
            self.say("Wieso hasst du mich? Ich dachte wir w\xe4ren Freunde!")
        else:    
            self.say("Why do you hate me? I thought we were friends!")
        self.complete_request()
    
    
    @register("de-DE",".*bist.*schwul.*")
    @register("en-US",".*you.*gay.*")
    def st_schwul_lol(self, speech, language):
        if language == 'de-DE':
            self.say("Jeder ist berechtigt, einen un\xf6tigen Kommentar zu hinterlegen")
        else:    
            self.say("Please, don\'t spam me!")
        self.complete_request()
    
    @register("de-DE",".*drogen.*kaufen.*")
    @register("en-US",".*buy.*drugs.*")
    def st_drugs(self, speech, language):
        if language == 'de-DE':
            self.say("Ich finde keine Drogengesch\xe4fte f\xfcr dich, es tut mir Leid!")
        else:    
            self.say("I didn't find any addiction treatment centers.")
        self.complete_request()
    
    @register("de-DE",".*ich.kann.*nicht.*")
    @register("en-US",".*I.can't.*")
    def st_i_cant(self, speech, language):
        if language == 'de-DE':
            self.say("Ok, dann eben nicht.")
        else:    
            self.say("I thought not.");
            self.say("OK, you can't then.")
        self.complete_request()
    
    @register("de-DE",".*wo.*bist.*du.*") 
    @register("en-US",".*where.*are.*you.*")
    def st_where_you(self, speech, language):
        if language == 'de-DE':
            self.say("Ich bin immer da, wo du bist.")
        else:
            self.say("Wherever you are.")
        self.complete_request()
    
    @register("de-DE",".*rauchst.*du.*")
    @register("en-US",".*you.*smoke.*")
    def st_pot(self, speech, language):
        if language == 'de-DE':
            self.say("Nein, rauchen ist ungesund!")
        else:    
            self.say("I suppose it's possible")
        self.complete_request()
    
    @register("de-DE",".*ich.*alkohol.getrunken.*")
    @register("en-US",".*I'm.*drunk.driving.*")
    def st_dui(self, speech, language):
        if language == 'de-DE':
            self.say("Von uns beiden f\xe4hrt keiner nach Hause!")
        else:    
            self.say("I couldn't find any DUI lawyers nearby.")
        self.complete_request()
    
    @register("en-US",".*shit.*myself.*")
    def st_shit_pants(self, speech, language):
        if language == 'en-US':
            self.say("Ohhhhhh! That is gross!")
        self.complete_request()
    
    @register("en-US","I'm.*a.*")
    def st_im_a(self, speech, language):
        if language == 'en-US':
            self.say("Are you?")
        self.complete_request()
    
    @register("en-US","Thanks.for.*")
    def st_thanks_for(self, speech, language):
        if language == 'en-US':
            self.say("My pleasure. As always.")
        self.complete_request()
    
    @register("en-US",".*you're.*funny.*")
    def st_funny(self, speech, language):
        if language == 'en-US':
            self.say("LOL")
        self.complete_request()
    
    @register("en-US",".*guess.what.*")
    def st_guess_what(self, speech, language):
        if language == 'en-US':
            self.say("Don't tell me... you were just elected President of the United States, right?")
        self.complete_request()
    
    @register("en-US",".*talk.*dirty.*me.*")
    def st_talk_dirty(self, speech, language):
        if language == 'en-US':
            self.say("I can't. I'm as clean as the driven snow.")
        self.complete_request()
    
    @register("en-US",".*you.*blow.*me.*")
    def st_blow_me(self, speech, langauge):
        if language == 'en-US':
            self.say("I'll pretend I didn't hear that.")
        self.complete_request()
    
    @register("en-US",".*sing.*song.*")
    def st_sing_song(self, speech, language):
        if language == 'en-US':
            self.say("Daisy, Daisy, give me your answer do...")
        self.complete_request()
