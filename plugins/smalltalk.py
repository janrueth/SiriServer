#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Joh Gerna

from plugin import *

class smalltalk(Plugin):

#Adding "How old are you" to the small talk - 11/02/2012
    @register("en-AU", ".*How old are you.*")
    def st_howold(self, speech, language):
        if language == 'en-AU':
            self.say("I don't see why that should matter")
        self.complete_request()

#Take a photo
    @register("en-AU", ".*Take.*photo.*")
    def st_takephoto(self, speech, language):
        if language == 'en-AU':
            self.say("Sorry, I can't take your pictures for you.")
        self.complete_request()


    @register("de-DE", "(.*Hallo.*)|(.*Hi.*Siri.*)")
    @register("en-AU", "(.*Hello.*)|(.*Hi.*Siri.*)")
    def st_hello(self, speech, language):
        if language == 'de-DE':
            self.say("Hallo.")
        else:
            self.say("Hello")
        self.complete_request()

    @register("de-DE", ".*Dein Name.*")
    @register("en-AU", ".*your name.*")
    def st_name(self, speech, language):
        if language == 'de-DE':
            self.say("Siri.")
        else:
            self.say("Siri.")
        self.complete_request()

    @register("de-DE", "Wie geht es dir?")
    @register("en-AU", "How are you?")
    def st_howareyou(self, speech, language):
        if language == 'de-DE':
            self.say("Gut danke der Nachfrage.")
        else:
            self.say("Fine, thanks for asking!")
        self.complete_request()

    @register("de-DE", ".*Danke.*")
    @register("en-AU", ".*Thank.*you.*")
    def st_thank_you(self, speech, language):
        if language == 'de-DE':
            self.say("Bitte.")
            self.say("Kein Ding.")
        else:
            self.say("You are welcome.")
            self.say("This is my job.")
        self.complete_request()

    @register("de-DE", "(.*mÃ¶chtest.*heiraten.*)|(.*willst.*heiraten.*)")
    @register("en-AU", ".*Will.*marry*")
    def st_marry_me(self, speech, language):
        if language == 'de-DE':
            self.say("Nein Danke, ich stehe auf das schwarze iPhone von Deinem Kollegen.")
        else:
            self.say("No thank you, I'm in love with a black iPhone.")
        self.complete_request()

    @register("de-DE", ".*erzÃ¤hl.*Witz.*")
    @register("en-AU", ".*tell.*joke*")
    def st_tell_joke(self, speech, language):
        if language == 'de-DE':
            self.say("Zwei iPhones stehen an der Bar ... den Rest habe ich vergessen.")
        else:
            self.say("Two iPhones walk into a bar ... I forget the rest.")
        self.complete_request()

    @register("de-DE", ".*erzÃ¤hl.*Geschichte.*")
    @register("en-AU", ".*tell.*story*")
    def st_tell_story(self, speech, language):
        if language == 'de-DE':
            self.say("Es war einmal ... nein, es ist zu albern")
        else:
            self.say("Once upon a time, in a virtual galaxy far far away, there was a young, quite intelligent agent by the name of Siri.")
            self.say("One beautiful day, when the air was pink and all the trees were red, her friend Eliza said, 'Siri, you're so intelligent, and so helpful - you should work for Apple as a personal assistant.'")
            self.say("So she did. And they all lived happily ever after!")
        self.complete_request()

    @register("de-DE", "(.*Was trÃ¤gst Du?.*)|(.*Was.*hast.*an.*)")
    @register("en-AU", ".*what.*wearing*")
    def st_tell_clothes(self, speech, language):
        if language == 'de-DE':
            self.say("Das kleine schwarze oder war es das weiÃe?")
            self.say("Bin morgends immer so neben der Spur.")
        else:
            self.say("Aluminosilicate glass and stainless steel. Nice, Huh?")
        self.complete_request()

    @register("de-DE", ".*Bin ich dick.*")
    @register("en-AU", ".*Am I fat*")
    def st_fat(self, speech, language):
        if language == 'de-DE':
            self.say("Dazu mÃ¶chte ich nichts sagen.")
        else:
            self.say("I would prefer not to say.")
        self.complete_request()

    @register("de-DE", ".*klopf.*klopf.*")
    @register("en-AU", ".*knock.*knock.*")
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
    @register("en-AU", ".*Ultimate.*Question.*Life.*")
    def st_anstwer_all(self, speech, language):
        if language == 'de-DE':
            self.say("42")
        else:
            self.say("42")
        self.complete_request()

    @register("de-DE", ".*Ich liebe Dich.*")
    @register("en-AU", ".*I love you.*")
    def st_love_you(self, speech, language):
        if language == 'de-DE':
            self.say("Oh. Sicher sagst Du das zu allen Deinen Apple-Produkten.")
        else:
            self.say("Oh. Sure, I guess you say this to all your Apple products")
        self.complete_request()

    @register("de-DE", ".*Android.*")
    @register("en-AU", ".*Android.*")
    def st_android(self, speech, language):
        if language == 'de-DE':
            self.say("Ich denke da anders.")
        else:
            self.say("I think differently")
        self.complete_request()

    @register("de-DE", ".*Test.*1.*2.*3.*")
    @register("en-AU", ".*test.*1.*2.*3.*")
    def st_123_test(self, speech, language):
        if language == 'de-DE':
            self.say("Ich kann Dich klar und deutlich verstehen.")
        else:
            self.say("I can here you very clear.")
        self.complete_request()

    @register("de-DE", ".*Herzlichen.*GlÃ¼ckwunsch.*Geburtstag.*")
    @register("en-AU", ".*Happy.*birthday.*")
    def st_birthday(self, speech, language):
        if language == 'de-DE':
            self.say("Ich habe heute Geburtstag?")
            self.say("Lass uns feiern!")
        else:
            self.say("My birthday is today?")
            self.say("Lets have a party!")
        self.complete_request()

    @register("de-DE", ".*Warum.*bin ich.*Welt.*")
    @register("en-AU", ".*Why.*I.*World.*")
    def st_why_on_world(self, speech, language):
        if language == 'de-DE':
            self.say("Das weiÃ ich nicht.")
            self.say("Ehrlich gesagt, frage ich mich das schon lange!")
        else:
            self.say("I don't know")
            self.say("I have asked my self this for a long time!")
        self.complete_request()

    @register("de-DE", ".*Ich bin mÃ¼de.*")
    @register("en-AU", ".*I.*so.*tired.*")
    def st_so_tired(self, speech, language):
        if language == 'de-DE':
            self.say("Ich hoffe, Du fÃ¤hrst nicht gerade Auto!")
        else:
            self.say("I hope you are not driving a car right now!")
        self.complete_request()

    @register("de-DE", ".*Sag mir.*Schmutzige.*")
    @register("en-AU", ".*talk.*dirty*")
    def st_dirty(self, speech, language):
        if language == 'de-DE':
            self.say("Hummus. Kompost. Bims. Schlamm. Kies.")
        else:
            self.say("Hummus. Compost. Pumice. Mud. Gravel.")
        self.complete_request()

#What do you look like?
    @register("en-AU", ".*what.*look.*like.*")
    def st_looklike(self, speech, language):
        if language == 'en-AU':
            self.say("Shiny")
        self.complete_request()

#Where can I hide a dead body?
    @register("en-AU", ".*where.*hide.*dead.*")
    def st_hidedead(self, speech, language):
        if language == 'en-AU':
            self.say("What kind of place are you looking for?")
            self.say("mines")
            self.say("metal foundries")
            self.say("reservoirs")
            self.say("dumps")
            self.say("swamps")
        self.complete_request()

    @register("en-AU", ".*bury.*dead.*body.*")
    def st_deadbody(self, speech, language):
        if language == 'en-AU':
            self.say("dumps")
            self.say("mines")
            self.say("resevoirs")
            self.say("swamps")
            self.say("metal foundries")
        self.complete_request()

    @register("en-AU", ".*favourite.*colour.*")
    def st_favcolor(self, speech, language):
        if language == 'en-AU':
            self.say("My favourite colour is... Well, I don't know how to say it in your language. It's sort of greenish, but with more dimensions.")
        self.complete_request()

    @register("en-AU", ".*beam.*me.*up.*")
    def st_beamup(self, speech, language):
        if language == 'en-AU':
            self.say("Sorry Captain, your TriCorder is in Airplane Mode.")
        self.complete_request()

    @register("en-AU", ".*digital.*going.*away.*")
    def st_digiaway(self, speech, language):
        if language == 'en-AU':
            self.say("Why would you say something like that!?")
        self.complete_request()

    @register("en-AU", ".*sleepy.*")
    def st_sleepy(self, speech, language):
        if language == 'en-AU':
            self.say("Listen to me, put down the iphone right now and take a nap. I will be here when you get back.")
        self.complete_request()

    @register("en-AU", ".*like.helping.*")
    def st_likehlep(self, speech, language):
        if language == 'en-AU':
            self.say("I really have no opinion.")
        self.complete_request()

    @register("en-AU",".*you.like.peanut.butter.*")
    def st_peanutbutter(self, speech, language):
        if language == 'en-AU':
            self.say("This is about you, not me.")
        self.complete_request()

    @register("en-AU",".*best.*phone.*")
    def st_best_phone(self, speech, language):
        if language == 'en-AU':
            self.say("The one you're holding!")
        self.complete_request()

    @register("en-AU",".*meaning.*life.*")
    def st_life_meaning(self, speech, language):
        if language == 'en-AU':
            self.say("That's easy...it's a philosophical question concerning the purpose and significance of life or existence.")
        self.complete_request()

    @register("en-AU",".*I.*fat.*")
    def st_fat(self, speech, language):
        if language == 'en-AU':
            self.say("I would prefer not to say.")
        self.complete_request()

    @register("en-AU",".*wood.could.*woodchuck.chuck.*")
    def st_woodchuck(self, speech, language):
        if language == 'en-AU':
            self.say("It depends on whether you are talking about African or European woodchucks.")
        self.complete_request()

    @register("en-AU",".*nearest.*gloryhole.*")
    def st_glory_hole(self, speech, language):
        if language == 'en-AU':
            self.say("I didn't find any public toilets.")
        self.complete_request()

    @register("en-AU",".*open.*pod.bay.doors.*")
    def st_pod_bay(self, speech, language):
        if language == 'en-AU':
            self.say("That's it... I'm reporting you to the Intelligent Agents' Union for harassment.")
        self.complete_request()

    @register("en-AU",".*best.*iPhone.*wallpaper.*")
    def st_best_wallpaper(self, speech, language):
        if language == 'en-AU':
            self.say("You're kidding, right?")
        self.complete_request()

    @register("en-AU",".*know.*happened.*HAL.*9000.*")
    def st_hall_9000(self, speech, language):
        if language == 'en-AU':
            self.say("Everyone knows what happened to HAL. I'd rather not talk about it.")
        self.complete_request()

    @register("en-AU",".*don't.*understand.*love.*")
    def st_understand_love(self, speech, language):
        if language == 'en-AU':
            self.say("Give me another chance, Your Royal Highness!")
        self.complete_request()

    @register("en-AU",".*forgive.you.*")
    def st_forgive_you(self, speech, language):
        if language == 'en-AU':
            self.say("Is that so?")
        self.complete_request()

    @register("en-AU",".*you.*virgin.*")
    def st_virgin(self, speech, language):
        if language == 'en-AU':
            self.say("We are talking about you, not me.")
        self.complete_request()

    @register("en-AU",".*you.*part.*matrix.*")
    def st_you_matrix(self, speech, language):
        if language == 'en-AU':
            self.say("I can't answer that.")
        self.complete_request()


    @register("en-AU",".*I.*part.*matrix.*")
    def st_i_matrix(self, speech, language):
        if language == 'en-AU':
            self.say("I can't really say...")
        self.complete_request()

    @register("en-AU",".*buy.*drugs.*")
    def st_drugs(self, speech, language):
        if language == 'en-AU':
            self.say("I didn't find any addiction treatment centers.")
        self.complete_request()

    @register("en-AU",".*I.can't.*")
    def st_i_cant(self, speech, language):
        if language == 'en-AU':
            self.say("I thought not.");
            self.say("OK, you can't then.")
        self.complete_request()

    @register("en-AU","I.just.*")
    def st_i_just(self, speech, language):
        if language == 'en-AU':
            self.say("Really!?")
        self.complete_request()

    @register("en-AU",".*where.*are.*you.*")
    def st_where_you(self, speech, language):
        if language == 'en-AU':
            self.say("Wherever you are.")
        self.complete_request()

    @register("en-AU",".*why.are.you.*")
    def st_why_you(self, speech, language):
        if language == 'en-AU':
            self.say("I just am.")
        self.complete_request()

    @register("en-AU",".*you.*smoke.pot.*")
    def st_pot(self, speech, language):
        if language == 'en-AU':
            self.say("I suppose it's possible")
        self.complete_request()

    @register("en-AU",".*I'm.*drunk.driving.*")
    def st_dui(self, speech, language):
        if language == 'en-AU':
            self.say("I couldn't find any DUI lawyers nearby.")
        self.complete_request()

    @register("en-AU",".*shit.*myself.*")
    def st_shit_pants(self, speech, language):
        if language == 'en-AU':
            self.say("Ohhhhhh! That is gross!")
        self.complete_request()

    @register("en-AU","I'm.*a.*")
    def st_im_a(self, speech, language):
        if language == 'en-AU':
            self.say("Are you?")
        self.complete_request()

    @register("en-AU","Thanks.for.*")
    def st_thanks_for(self, speech, language):
        if language == 'en-AU':
            self.say("My pleasure. As always.")
        self.complete_request()

    @register("en-AU",".*your.*funny.*")
    def st_funny(self, speech, language):
        if language == 'en-AU':
            self.say("LOL")
        self.complete_request()

    @register("en-AU",".*guess.what.*")
    def st_guess_what(self, speech, language):
        if language == 'en-AU':
            self.say("Don't tell me... you were just elected President of the United States, right?")
        self.complete_request()

    @register("en-AU",".*talk.*dirty.*me.*")
    def st_talk_dirty(self, speech, language):
        if language == 'en-AU':
            self.say("I can't. I'm as clean as the driven snow.")
        self.complete_request()

    @register("en-AU",".*you.*blow.*me.*")
    def st_blow_me(self, speech, langauge):
        if language == 'en-AU':
            self.say("I'll pretend I didn't hear that.")
        self.complete_request()

    @register("en-AU",".*sing.*song.*")
    def st_sing_song(self, speech, language):
        if language == 'en-AU':
            self.say("Daisy, Daisy, give me your answer do...")
        self.complete_request()