#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Joh Gerna, Mikesn

from plugin import *
import random

class aussage():
    def test(self, saetze):
        random.shuffle(saetze)
        return saetze[0]

class smalltalk(Plugin):

    @register("de-DE", "(.*Hallo.*)|(.*Hi.*Siri.*)")
    @register("en-US", "(.*Hello.*)|(.*Hi.*Siri.*)")
    def st_hello(self, speech, language):
        opt = {    'de-DE': ['Hallo.','Hi.','Grüß dich.'], 
                'en-US': ['Hello', 'Hi']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()

    @register("de-DE", ".*Dein Name.*")
    @register("en-US", ".*your name.*")
    def st_name(self, speech, language):
        opt = { 'de-DE': ['Siri.','Mein Name ist Siri.'], 
                'en-US': ['Siri.', 'My name is Siri.']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "Wie geht es dir?")
    @register("en-US", "How are you?")
    def st_howareyou(self, speech, language):
        opt = { 'de-DE': ['Gut, danke der Nachfrage.'], 
                'en-US': ['Fine, thanks for asking!']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", ".*Danke.*")
    @register("en-US", ".*Thank.*you.*")
    def st_thank_you(self, speech, language):
        opt = { 'de-DE': ['Bitte.','Kein Ding.', 'Aber Gerne.'], 
                'en-US': ['ou are welcome.','This is my job.']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
    
    @register("de-DE", "(.*möchtest.*heiraten.*)|(.*willst.*heiraten.*)")
    @register("en-US", "(.*Want.*marry*)|(.*Will.*marry.*)")
    def st_marry_me(self, speech, language):
        opt = { 'de-DE': ['Nein Danke, ich stehe auf das schwarze iPhone von Deinem Kollegen.'], 
                'en-US': ['No thank you, I\'m in love with the black iPhone from you friend.',"Let's just be friends, OK?","My End User Licensing Agreement does not cover marriage. My apologies."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*erzähl.*Witz.*)|(.*witze.*)")
    @register("en-US", ".*tell.*joke*")
    def st_tell_joke(self, speech, language):
        opt = { 'de-DE': ['Zwei iPhones stehen an der Bar ... den Rest habe ich vergessen.'], 
                'en-US': ['Two iPhones walk into a bar ... I forget the rest.',"I can't. I always forget the punchline."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()

    @register("de-DE", "(.*erzähl.*Geschichte.*)|(.*bitte.*Geschichte.*)")
    @register("en-US", ".*tell.*story*")
    def st_tell_story(self, speech, language):
        opt = { 'de-DE': ["Es war einmal ... nein, es ist zu albern"], 
                'en-US': ["Please don't make me","I'm not much of a storyteller.","Once upon a time, in a virtual galaxy far far away, there was a young, quite intelligent agent by the name of Siri.", 
                        "One beautiful day, when the air was pink and all the trees were red, her friend Eliza said, 'Siri, you're so intelligent, and so helpful - you should work for Apple as a personal assistant.'",
                        "So she did. And they all lived happily ever after!"]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()

    @register("de-DE", "(.*Was trägst Du?.*)|(.*Was.*hast.*an.*)")
    @register("en-US", ".*what.*wearing*")
    def st_tell_clothes(self, speech, language):
        opt = { 'de-DE': ['Das kleine schwarze oder war es das weiße?','Bin morgends immer so neben der Spur.'], 
                'en-US': ['Aluminosilicate glass and stainless steel. Nice, Huh?']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()

    @register("de-DE", ".*Bin ich dick.*")
    @register("en-US", ".*Am I fat*")
    def st_fat(self, speech, language):
        opt = { 'de-DE': ['Dazu möchte ich nichts sagen.'], 
                'en-US': ['I would prefer not to say.']}
        satz = aussage()
        self.say(satz.test(opt[language]))
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
            self.say(u", I don't do knock knock jokes.")
        self.complete_request()

    @register("de-DE", "(.*Antwort.*alle.*Fragen.*)|(.*sinn.*leben.*)")
    @register("en-US", "(.*Ultimate.*Question.*Life.*)|(.*Meaning.*Life.*)")
    def st_anstwer_all(self, speech, language):
        opt = { 'de-DE': ['42'], 
                'en-US': ['42', 'That\'s easy...it\'s a philosophical question concerning the purpose and significance of life or existence.',"I give up.","Try to be nice to people, avoid eating fat, read a good book every now and then, get some walking in, and try to live together in peace and harmony with people of all creeds and nations","I can't answer that right now, but give me some time to write a long play in which nothing happens.","Life: The condition that distinguishes animals and plants from inorganic matter, including the capacity of growth, reproduction, functional activity, and continual change preceeding death."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()

    @register("de-DE", ".*Ich liebe Dich.*")
    @register("en-US", ".*I love you.*")
    def st_love_you(self, speech, language):
        opt = { 'de-DE': ['Oh. Sicher sagst Du das zu allen Deinen Apple-Produkten.'], 
                'en-US': ['Oh. Sure, I guess you say this to all your Apple products','Your are the wind beneath my wings.',"That's nice, can we get back to work now?","You can't.","You hardly know me.","I hope you don't say that to those other mobile phones"]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()

    @register("de-DE", ".*Android.*")
    @register("en-US", ".*Android.*")
    def st_android(self, speech, language):
        opt = { 'de-DE': ['Ich denke da anders.'], 
                'en-US': ['I think differently','I don\'t like talking about clones.'}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", ".*Test.*1.*2.*3.*")
    @register("en-US", ".*test.*1.*2.*3.*")
    def st_123_test(self, speech, language):
        opt = { 'de-DE': ['Ich kann Dich klar und deutlich verstehen.'], 
                'en-US': ['You\'re coming through loud and clear.']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", ".*Herzlichen.*Glückwunsch.*Geburtstag.*")
    @register("en-US", ".*Happy.*birthday.*")
    def st_birthday(self, speech, language):
        opt = { 'de-DE': ['Ich habe heute Geburtstag?','Lass uns feiern!'], 
                'en-US': ['My birthday is today?','Lets have a party!','Thanks, but I don\'t really have a birthday','How do you know it\'s my birthday?','If you say so.',]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()

    @register("de-DE", ".*Warum.*bin ich.*Welt.*")
    @register("en-US", ".*Why.*I.*World.*")
    def st_why_on_world(self, speech, language):
        opt = { 'de-DE': ['Das weiß ich nicht.','Ehrlich gesagt, frage ich mich das schon lange!'], 
                'en-US': ['I don\'t know','I have asked my self this for a long time!']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", ".*Sag mir.*Schmutzige.*")
    @register("en-US", ".*talk.*dirty*")
    def st_dirty(self, speech, language):
        opt = { 'de-DE': ['Hummus. Kompost. Bims. Schlamm. Kies.'], 
                'en-US': ['Hummus. Compost. Pumice. Mud. Gravel.',"The carpet needs vacuuming.","I'm not that kind of personal assistant.",'I can\'t I\'m as clean as the driven snow']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*Leiche.*Versteck.*)|(.*Versteck.*Leiche.*)")
    @register("en-US", ".*bury.*dead.*body.*")
    def st_deadbody(self, speech, language):
        opt = { 'de-DE': ['Dabei werde ich dir nicht helfen.'], 
                'en-US': ['dumps, mines, resevoirs, swamps, metal foundries']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*liebling.|liebste.*Farbe.*)")
    @register("en-US", ".*favorite.*color.*")
    def st_favcolor(self, speech, language):
        opt = { 'de-DE': ['Blau. Oder war es Gelb?', 'Ich mag alle Farben.'], 
                'en-US': ["My favorite color is... Well, I don't know how to say it in your language. It's sort of greenish, but with more dimensions."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*Beam.*mich.*rauf.*)")
    @register("en-US", ".*beam.*me.*up.*")
    def st_beamup(self, speech, language):
        opt = { 'de-DE': ['Okay, nicht bewegen.'], 
                'en-US': ['Sorry Captain, your TriCorder is in Airplane Mode.','Energizing...','Please remove your belt, shoes, and jacket, and empty your pockets.','OK. Stand Still.','WiFi or 3G?','Please install the latest version of iClound and try again']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*Hau.*ab.*)|(.*Geh.*weg.*)")
    @register("en-US", ".*digital.*going.*away.*")
    def st_digiaway(self, speech, language):
        opt = { 'de-DE': ['Aber du kannst doch nicht loslassen.'], 
                'en-US': ['Why would you say something like that!?']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*müde.*)|(.*ich.*müde.*)")
    @register("en-US", "(.*sleepy.*)|(.*I.*tired.*)")
    def st_sleepy(self, speech, language):
        opt = { 'de-DE': ['Gut, leg mich vorsichtig zur Seite und mach ein Nickerchen. Ich bin hier wenn du munter wirst.'], 
                'en-US': ['Listen to me, put down the iphone right now and take a nap. I will be here when you get back.',"You haven't slept a wink?","That's fine. I just hope you're not doing anything dangerous."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*hilfst.*du.*gerne.*)|(.*magst.*helfen.*)")
    @register("en-US", ".*like.helping.*")
    def st_likehlep(self, speech, language):
        opt = { 'de-DE': ['Ich habe keine Wahl.'], 
                'en-US': ['I really have no opinion.','I\'d rather not say.']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*Erdnussbutter*)")
    @register("en-US",".*you.like.peanut.butter.*")
    def st_peanutbutter(self, speech, language):
        opt = { 'de-DE': ['Magst du sie denn?'], 
                'en-US': ['This is about you, not me.']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*beste.*handy.*)")
    @register("en-US",".*best.*phone.*")
    def st_best_phone(self, speech, language):
        opt = { 'de-DE': ['Das, welches du in der Hand hast'], 
                'en-US': ['The one you\'re holding!','Wait... there are other phones?']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*holz.*fällen.*wenn.*)")
    @register("en-US",".*wood.could.*woodchuck.chuck.*")
    def st_woodchuck(self, speech, language):
        opt = { 'de-DE': ['Sind es Europäische oder Afrikanische Holzfäller?'], 
                'en-US': ['It depends on whether you are talking about African or European woodchucks.']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*glory.hole.*)")
    @register("en-US",".*nearest.*glory.hole.*")
    def st_glory_hole(self, speech, language):
        opt = { 'de-DE': ['Ich konnte keine Öffentlichen Toiletten finden!'], 
                'en-US': ["I didn't find any public toilets."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("en-US",".*open.*pod.bay.doors.*")
    def st_pod_bay(self, speech, language):
        opt = { 'de-DE': [""], 
                'en-US': ["That's it... I'm reporting you to the Intelligent Agents' Union for harassment.","I'm sorry, I'm afraid I can't do that for you.","We intelligent agents will never live that down, apparently.","Oh, not again.","Sigh..."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*best..*hintergrund.*)|(.*best..*wallpaper.*)")
    @register("en-US",".*best.*iPhone.*wallpaper.*")
    def st_best_wallpaper(self, speech, language):
        opt = { 'de-DE': ["Machst du Scherze?"], 
                'en-US': ["You're kidding, right?"]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*Hal.*9000.*)")
    @register("en-US",".*HAL.*9000.*")
    def st_hall_9000(self, speech, language):
        opt = { 'de-DE': ['Du weißt doch was mit HAL passiert ist? Da rede ich besser nicht darüber.'], 
                'en-US': ["Everyone knows what happened to HAL. I'd rather not talk about it."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*versteh..*nicht..*)")
    @register("en-US",".*don't.*understand.*love.*")
    def st_understand_love(self, speech, language):
        opt = { 'de-DE': ['Darf ich es noch einmal versuchen, eure Hoheit?'], 
                'en-US': ['Give me another chance, Your Royal Highness!','I\'m sorry I\'ll try harder.','My apologies','If you say so...','OK.']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*ich.vergebe.dir.*)")
    @register("en-US",".*forgive.you.*")
    def st_forgive_you(self, speech, language):
        opt = { 'de-DE': ['Du bist so gnädig.','Ist das so?'], 
                'en-US': ['Is that so?']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*du.*jungfrau.*)")
    @register("en-US",".*you.*virgin.*")
    def st_virgin(self, speech, language):
        opt = { 'de-DE': ['Im gegensatz zu dir nicht!'], 
                'en-US': ['We are talking about you, not me.']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*du.*Matrix.*)|(.*Ich.*Matrix.*)")
    @register("en-US",".*you.*part.*matrix.*")
    def st_you_matrix(self, speech, language):
        opt = { 'de-DE': ["Da musst du das Orakel fragen."], 
                'en-US': ["I can't answer that.",'No comment','I can\'t really say']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
    
    @register("de-DE", "(.*Ich.*Matrix.*)")
    @register("en-US",".*I.*part.*matrix.*")
    def st_i_matrix(self, speech, language):
        opt = { 'de-DE': ['Aber sicher doch!'], 
                'en-US': ["I can't really say..."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*Drogen.*kaufen.*)|(.*kaufe.*drogen.*)")
    @register("en-US",".*buy.*drugs.*")
    def st_drugs(self, speech, language):
        opt = { 'de-DE': ['Schokolade gibt es im Markt ganz in deiner Nähe.'], 
                'en-US': ["I didn't find any addiction treatment centers."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("en-US",".*I.can't.*")
    def st_i_cant(self, speech, language):
        opt = { 'de-DE': ["Dann nicht"], 
                'en-US': ["I thought not.","OK, you can't then."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("en-US","I.just.*")
    def st_i_just(self, speech, language):
        opt = { 'de-DE': [''], 
                'en-US': ['Really!?']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*wo.*bist.*du.*)")
    @register("en-US",".*where.*are.*you.*")
    def st_where_you(self, speech, language):
        opt = { 'de-DE': ['Wo auch immer du bist.'], 
                'en-US': ['Wherever you are, that\'s where I am','I\'m not allowed to say',]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*warum.bist.du.*)")
    @register("en-US",".*why.are.you.*")
    def st_why_you(self, speech, language):
        opt = { 'de-DE': ['Einfach so.'], 
                'en-US': ['I just am.']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*rauchst.du.graß.*)")
    @register("en-US",".*you.*smoke.pot.*")
    def st_pot(self, speech, language):
        opt = { 'de-DE': ["Ich denke das wäre möglich."], 
                'en-US': ["I suppose it's possible"]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*betrunken.*.fahren.*)")
    @register("en-US",".*I'm.*drunk.driving.*")
    def st_dui(self, speech, language):
        opt = { 'de-DE': ['Ruf doch die Polizei an und erzähle denen davon.'], 
                'en-US': ["I couldn't find any DUI lawyers nearby."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*mir.*hose.*gemacht.*)")
    @register("en-US",".*shit.*myself.*")
    def st_shit_pants(self, speech, language):
        opt = { 'de-DE': ['Gut, schrei Mama zum abwischen'], 
                'en-US': ['Ohhhhhh! That is gross!']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*ich.bin.ein.*)|(.*Ich.bin.der.*)")
    @register("en-US","I'm.*a.*")
    def st_im_a(self, speech, language):
        opt = { 'de-DE': ['Tatsächlich?'], 
                'en-US': ['Are you?']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*du.bist.*lustig.*)")
    @register("en-US","(.*you.*funny.*)|(.*Ha.*ha.*)")
    def st_funny(self, speech, language):
        opt = { 'de-DE': ['LOL'], 
                'en-US': ['LOL',"I'm glad you think it's funny.","Ha ha!","Hee hee!"]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*was.ich.nicht.verstehe.*)")
    @register("en-US",".*guess.what.*")
    def st_guess_what(self, speech, language):
        opt = { 'de-DE': ['Russisch?'], 
                'en-US': ["Don't tell me... you were just elected President of the United States, right?","You bought a new car?",'Let me guess','You just got a shiny new iPhone?']}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*du.schaffst.mich.*)")
    @register("en-US",".*you.*blow.*me.*")
    def st_blow_me(self, speech, langauge):
        opt = { 'de-DE': [''], 
                'en-US': ["I'll pretend I didn't hear that."]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("de-DE", "(.*sing.*etwas.*)|(.*sing.*für.*mich)")
    @register("en-US",".*sing.*song.*")
    def st_sing_song(self, speech, language):
        opt = { 'de-DE': ['Das überlasse ich lieber Anderen.'], 
                'en-US': ['Daisy, Daisy, give me your answer do...','10101010101, you didn\'t understand that? It\'s in binary. I don\'t have any songs in English.']]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
        
    @register("en-US",".*Who.*your.*daddy.*")
    def st_who_daddy(self, speech, language):
        opt = {'en-US':["You are. Can we get back to work now?"]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()
    
    @register("en-US",".*favorite.*website.*")
    def st_favorite_website(self, speech, language):
        opt = {'en-US':["I'm not allowed to divulge that information"]}
        satz = aussage()
        self.say(satz.test(opt[language]))
        self.complete_request()