#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Joh Gerna

from plugin import *

class smalltalk(Plugin):
     
    #only english additions 
    @register("en-US", "Good .*night.*")
    def st_night(self, speech, language):
        if language == 'en-US':
            self.say("Good Night, {0}. See you later".format(self.user_name()))
        self.complete_request()

    @register("en-US", "Good .*morning.*")
    def st_morning(self, speech, language):
        if language == 'en-US':
            self.say("Good Morning, {0}.".format(self.user_name()))
        self.complete_request()

    @register("en-US", "Good .*afternoon.*")
    def st_afternoon(self, speech, language):
        if language == 'en-US':
            self.say("Good Afternoon, {0}.".format(self.user_name()))
        self.complete_request()

    @register("en-US", "Good .*evening.*")
    def st_evening(self, speech, language):
        if language == 'en-US':
            self.say("Good Evening, {0}.".format(self.user_name()))
        self.complete_request()

    @register("en-US", "(testing)|(test)")
    def st_test(self, speech, language):
        if language == 'en-US':
            self.say("Mission Control, I read you loud and clear, {0}".format(self.user_name()))
        self.complete_request()

    @register("en-US", "(Okay)|(Ok)|(Okie)")
    def st_yes(self, speech, language):
        if language == 'en-US':
            self.say("Yep, everything's OK")
        self.complete_request()

    @register("en-US", "Really")
    def st_really(self, speech, language):
        if language == 'en-US':
            self.say("I suppose so.")
        self.complete_request()

    @register("en-US", "What's up")
    def st_whatups(self, speech, language):
        if language == 'en-US':
            self.say("Everything is cool, {0}".format(self.user_name()))
        self.complete_request()

    @register("en-US", "What are you doing")
    def st_doing(self, speech, language):
        if language == 'en-US':
            self.say("What am I doing? I'm talking with you, {0}".format(self.user_name()))
        self.complete_request()
  
    @register("en-US", "Bye")
    def st_bye(self, speech, language):
        if language == 'en-US':
            self.say("OK, see you later..")
        self.complete_request() 

    @register("en-US", "Thank you")
    def st_thank_you(self, speech, language):
        if language == 'en-US':
            self.say("My pleasure. As always.")
        self.complete_request()

    #thanks to LowKey 
     
    @register("de-DE", "(.*Mein name.*)")
    @register("en-US", "(.*My name.*)")
    def st_my_name(self, speech, language):  
        if language == 'de-DE':
            self.say(u"Du heißt {0}.".format(self.user_name()))
        else:            
            self.say(u"Your name is {0}. At least that's what you told me.".format(self.user_name()))
        self.complete_request()   
      
    @register("de-DE", "(.*Fick.*)")
    @register("en-US", "(.*Fuck.*)|(.*Dumb.*)")
    def st_fuck(self, speech, language):  
        if language == 'de-DE':
            self.say(u"Das ist nicht gut {0}!".format(self.user_name()))
        else:            
            self.say(u"Mind your language {0}!".format(self.user_name()))
        self.complete_request()   
        
        
    @register("de-DE", "(.*Hallo.*)|(.*Hi.*Siri.*)|(Hi)")
    @register("en-US", "(.*Hello.*)|(.*Hi.*Siri.*)|(Hi)")
    @register("fr-FR", ".*(Bonjour|Coucou|Salut)( Siri)?.*")
    def st_hello(self, speech, language):
        if language == 'de-DE':
            self.say(u"Hallo {0}".format(self.user_name()))
        elif language == 'fr-FR':
            self.say(u"Bonjour {0}".format(self.user_name()));
        else:
            self.say(u"Hello {0}".format(self.user_name()))
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
    @register("fr-FR", u".*((ça|ca) vas?|vas? bien|comment vas?|gaze).*")
    def st_howareyou(self, speech, language):
        if language == 'de-DE':
            self.say("Gut danke der Nachfrage.")
        elif language == 'fr-FR':
            rep = ["Je vais bien. Merci !", u"Je vais très bien. Merci !","Parfaitement bien !"]
            self.say(random.choice(rep));
        else:
            self.say("Fine, thanks for asking!")
        self.complete_request()
        
    @register("de-DE", u"(.*möchtest.*heiraten.*)|(.*willst.*heiraten.*)")
    @register("en-US", "(.*Want.*marry*)|(.*Will.*marry*)")
    @register("fr-FR", ".*(veux|veut).*épouser.*")
    def st_marry_me(self, speech, language):
        if language == 'de-DE':
            self.say("Nein Danke, ich stehe auf das schwarze iPhone von Deinem Kollegen.")
        elif language == 'fr-FR':
            self.say("Non merci, je suis amoureux de l'iPhone blanc de ton ami.");
        else:
            self.say("No thank you, I'm in love with the black iPhone from you friend.")
        self.complete_request()

    @register("de-DE", u".*erzähl.*Witz.*")
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
            self.say("Once upon a time, in a virtual galaxy far far away, there was a young, quite intelligent agent by the name of Siri.")
            self.say("One beautiful day, when the air was pink and all the trees were red, her friend Eliza said, 'Siri, you're so intelligent, and so helpful - you should work for Apple as a personal assistant.'")
            self.say("So she did. And they all lived happily ever after!")
        self.complete_request()

    @register("de-DE", u"(.*Was trägst Du?.*)|(.*Was.*hast.*an.*)")
    @register("en-US", ".*what.*wearing*")
    @register("fr-FR", "(.*que.*porte.*)|(.*qu'est-ce-que.*porte.*)")
    def st_tell_clothes(self, speech, language):
        if language == 'de-DE':
            self.say("Das kleine schwarze oder war es das weiße?")
            self.say("Bin morgends immer so neben der Spur.")  
        elif language == 'fr-FR':
            self.say("Je ne sais pas mais je suis beau.")
        else:
            self.say("Aluminosilicate glass and stainless steel. Nice, Huh?")
        self.complete_request()

    @register("de-DE", ".*Bin ich dick.*")
    @register("en-US", ".*Am I fat*")
    @register("fr-FR", u"(.*ai l'air.*gros.*)|(.*suis.*gros.*)")
    def st_fat(self, speech, language):
        if language == 'de-DE':
            self.say("Dazu möchte ich nichts sagen.")
        elif language == 'fr-FR':
            self.say(u"Je préfère ne pas répondre.")
        else:
            self.say("I would prefer not to say.")
        self.complete_request()

    @register("de-DE", ".*klopf.*klopf.*")
    @register("en-US", ".*knock.*knock.*")
    @register("fr-FR", ".*to(c|k).*to(c|k).*")
    def st_knock(self, speech, language):
        if language == 'de-DE':
            answer = self.ask(u"Wer ist da?")
            answer = self.ask(u"\"{0}\" wer?".format(answer))
            self.say(u"Wer nervt mich mit diesen Klopf Klopf Witzen?")
        elif language == 'fr-FR':
            answer = self.ask(u"Qui est là ?")
            answer2 = self.ask(u"{0} qui ?".format(answer))
            self.say(u"{0} {1} ? Qui est-ce ? Je ne le connais pas.".format(answer,answer2))
            #self.say(u"Je préfère ne pas réagir à cette blague.")
        else:
            answer = self.ask(u"Who's there?")
            answer = self.ask(u"\"{0}\" who?".format(answer))
            self.say(u", I don't do knock knock jokes.")
        self.complete_request()

    @register("de-DE", ".*Antwort.*alle.*Fragen.*")
    @register("en-US", ".*Ultimate.*Question.*Life.*")
    @register("fr-FR", ".*Grande.*Question.*Vie.*")
    def st_anstwer_all(self, speech, language):
        self.say("42")
        self.complete_request()

    @register("de-DE", ".*Ich liebe Dich.*")
    @register("en-US", ".*I love you.*")
    @register("fr-FR", ".*Je t'aime'.*")
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
    @register("fr-FR", ".*Android.*")
    def st_android(self, speech, language):
        if language == 'de-DE':
            self.say("Ich denke da anders.")
        elif language == 'fr-FR':
            self.say(u"Je pense différemment à propos de cela");
        else:
            self.say("I think differently")
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

    @register("de-DE", u".*Herzlichen.*Glückwunsch.*Geburtstag.*")
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
            self.say("I don't know")
            self.say("I have asked my self this for a long time!")
        self.complete_request()

    @register("de-DE", u".*Ich bin müde.*")
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
    @register("en-US", ".*talk.*dirty*")
    @register("fr-FR", ".*di(s|t).*mots?.*sales?.*")
    def st_dirty(self, speech, language):
        if language == 'de-DE':
            self.say("Hummus. Kompost. Bims. Schlamm. Kies.")
        elif language == 'fr-FR':
            self.say(u"Humus. Composte. Pierre ponce. Boue. Gravier.")      
        else:
            self.say("Hummus. Compost. Pumice. Mud. Gravel.")
        self.complete_request()
   
    @register("en-US", ".*bury.*dead.*body.*")
    def st_deadbody(self, speech, language):
        if language == 'en-US':
            self.say("dumps")
            self.say("mines")
            self.say("resevoirs")
            self.say("swamps")
            self.say("metal foundries")
        self.complete_request()
   
    @register("en-US", ".*favorite.*color.*")
    @register("fr-FR", u".*couleur.*(favorite|préféré|prèféré).*")
    def st_favcolor(self, speech, language):
        if language == 'en-US':
            self.say("My favorite color is... Well, I don't know how to say it in your language. It's sort of greenish, but with more dimensions.")
        elif language == 'fr-FR':
            self.say(u"Ma couleur préférée est... Bien, je ne sais pas vraiment comment le dire dans votre langue. C'est une sorte de vert, mais avec plus de dimensions.")
        self.complete_request()
    
    @register("en-US", ".*beam.*me.*up.*")
    def st_beamup(self, speech, language):
        if language == 'en-US':
            self.say("Sorry Captain, your TriCorder is in Airplane Mode.")
        self.complete_request()
   
    @register("en-US", ".*digital.*going.*away.*")
    def st_digiaway(self, speech, language):
        if language == 'en-US':
            self.say("Why would you say something like that!?")
        self.complete_request()
    
    @register("en-US", ".*sleepy.*")
    @register("fr-FR", u".*fatigué|endormi.*")
    def st_sleepy(self, speech, language):
        if language == 'en-US':
            self.say("Listen to me, put down the iphone right now and take a nap. I will be here when you get back.")
        elif language == 'fr-FR':
            rep = [u"Ecoutez-moi, déposez l'iPhone immédiatement et faites une sieste. Je serai là à votre retour.", u"Ecoutez-moi. Posez tout de suite cet iPhone et faites une sieste. Je vous attends ici."]
            self.say(random.choice(rep))
        self.complete_request()
    
    @register("en-US", ".*like.helping.*")
    @register("fr-FR", ".*aime.(aidé|aider).*")
    def st_likehlep(self, speech, language):
        if language == 'en-US':
            self.say("I really have no opinion.")
        elif language == 'fr-FR':
            self.say(u"Je n'ai pas d'opinion à ce sujet.")
        self.complete_request()
    
    @register("en-US",".*you.like.peanut.butter.*")
    def st_peanutbutter(self, speech, language):
        if language == 'en-US':
            self.say("This is about you, not me.")
        self.complete_request()
    
    @register("en-US",".*best.*phone.*")
    @register("fr-FR",".*meilleur.*(telephone|téléphone).*")
    def st_best_phone(self, speech, language):
        if language == 'en-US':
            self.say("The one you're holding!")
        elif language == 'fr-FR':
            self.say("C'est l'iPhone 4S, mais vous êtes trop pauvre pour l'acheter !")
        self.complete_request()
    
    @register("en-US",".*meaning.*life.*")
    def st_life_meaning(self, speech, language):
        if language == 'en-US':
            self.say("That's easy...it's a philosophical question concerning the purpose and significance of life or existence.")
        self.complete_request()
    
    @register("en-US",".*I.*fat.*")
    def st_fat(self, speech, language):
        if language == 'en-US':
            self.say("I would prefer not to say.")
        self.complete_request()
    
    @register("en-US",".*wood.could.*woodchuck.chuck.*")
    def st_woodchuck(self, speech, language):
        if language == 'en-US':
            self.say("It depends on whether you are talking about African or European woodchucks.")
        self.complete_request()
    
    @register("en-US",".*nearest.*glory.hole.*")
    def st_glory_hole(self, speech, language):
        if language == 'en-US':
            self.say("I didn't find any public toilets.")
        self.complete_request()
    
    @register("en-US",".*open.*pod.bay.doors.*")
    def st_pod_bay(self, speech, language):
        if language == 'en-US':
            self.say("That's it... I'm reporting you to the Intelligent Agents' Union for harassment.")
        self.complete_request()
    
    @register("en-US",".*best.*iPhone.*wallpaper.*")
    def st_best_wallpaper(self, speech, language):
        if language == 'en-US':
            self.say("You're kidding, right?")
        self.complete_request()
    
    @register("en-US",".*know.*happened.*HAL.*9000.*")
    @register("fr-FR",".*.*HAL.*9000.*")
    def st_hall_9000(self, speech, language):
        if language == 'en-US':
            self.say("Everyone knows what happened to HAL. I'd rather not talk about it.")
        elif language == 'fr-FR':
            self.say(u"Tout le monde sait ce qui est arrivé à HAL. Je préfère ne pas en parler.")
        self.complete_request()
    
    @register("en-US",".*don't.*understand.*love.*")
    def st_understand_love(self, speech, language):
        if language == 'en-US':
            self.say("Give me another chance, Your Royal Highness!")
        self.complete_request()
    
    @register("en-US",".*forgive.you.*")
    def st_forgive_you(self, speech, language):
        if language == 'en-US':
            self.say("Is that so?")
        self.complete_request()
    
    @register("en-US",".*you.*virgin.*")
    @register("fr-FR",".*tu.*vierge.*")
    def st_virgin(self, speech, language):
        if language == 'en-US':
            self.say("We are talking about you, not me.")
        elif language == 'fr-FR':
            self.say(u"Nous sommes en train de parler de toi, pas de moi.");
        self.complete_request()
    
    @register("en-US",".*you.*part.*matrix.*")
    def st_you_matrix(self, speech, language):
        if language == 'en-US':
            self.say("I can't answer that.")
        self.complete_request()
    
    
    @register("en-US",".*I.*part.*matrix.*")
    def st_i_matrix(self, speech, language):
        if language == 'en-US':
            self.say("I can't really say...")
        self.complete_request()
    
    @register("en-US",".*buy.*drugs.*")
    @register("fr-FR",".*achete.*drogue.*")
    def st_drugs(self, speech, language):
        if language == 'en-US':
            self.say("I didn't find any addiction treatment centers.")
        elif language == 'fr-FR':
            self.say(u"Je ne trouve aucun centre de soin pour les addictions.")
        self.complete_request()
    
    @register("en-US",".*I.can't.*")
    @register("fr-FR","(je|tu).(ne peu(x|t) pas|ne sai(s|t) pas).*")
    def st_i_cant(self, speech, language):
        if language == 'en-US':
            self.say("I thought not.");
            self.say("OK, you can't then.")
        elif language == 'fr-FR':
            self.say(u"Rien n'est impossible, l'important c'est d'avoir la foi.");
            self.say(u"OK, peut-être que ça l'est.")
        self.complete_request()
    
    @register("en-US","I.just.*")
    @register("fr-FR",u"je.viens.*")
    def st_i_just(self, speech, language):
        if language == 'en-US':
            self.say("Really!?")
        elif language == 'fr-FR':
            rep = [u"Vraiment !?", u"Cool !", u"Bravo !", u"Pas mal !", u"Super !"]
            self.say(random.choice(rep))
        self.complete_request()
    
    @register("en-US",".*where.*are.*you.*")
    @register("fr-FR",u".*(ou|où).*(est|es).*tu.*")
    def st_where_you(self, speech, language):
        if language == 'en-US':
            self.say("Wherever you are.")
        elif language == 'fr-FR':
            rep = [u"Je suis partout où tu es.",u"Je suis partout où tu es. Mais tu le savais déjà.", u"Je te suivrai, partout où tu iras, j'irai...", u"Je suis au même endroit que toi.", u"Je parie que tu sais où je me trouve."]
            self.say(random.choice(rep))
        self.complete_request()
    
    @register("en-US",".*why.are.you.*")
    @register("fr-FR",".*pourquoi.(es|est).tu.*")
    def st_why_you(self, speech, language):
        if language == 'en-US':
            self.say("I just am.")
        elif language == 'fr-FR':
            rep = [u"Je suis ce que je suis parce que je suis ce que je suis.", "Pourquoi faudrait-il tout expliquer ?", u"Il existe certaines choses qui ne s'expliquent pas. C'est comme ça."]
            self.say(random.choice(rep))
        self.complete_request()
    
    @register("en-US",".*you.*smoke.pot.*")
    def st_pot(self, speech, language):
        if language == 'en-US':
            self.say("I suppose it's possible")
        self.complete_request()
    
    @register("en-US",".*I'm.*drunk.driving.*")
    @register("fr-FR",u".*je.*(conduit|conduis|conduire).(bourré|saoul|soul|soûl|sous|bourrer).*")
    def st_dui(self, speech, language):
        if language == 'en=US':
            self.say("I couldn't find any DUI lawyers nearby.")
        elif language == 'fr-FR':
            choix = random.randint(0,1)
            if choix == 1:
                self.say("Je recherche la patrouille de police la plus proche...")
                self.say(u"Je n'ai trouvé aucune voiture de police dans le secteur.")
            else:
                self.say(u"Boire ou conduire, il faut choisir !")
        self.complete_request()
    
    @register("en-US",".*shit.*myself.*")
    def st_shit_pants(self, speech, language):
        if language == 'en-US':
            self.say("Ohhhhhh! That is gross!")
        self.complete_request()
    
    @register("en-US","I'm.*a.*")
    @register("fr-FR","Je suis.*(un|une).*")
    def st_im_a(self, speech, language):
        if language == 'en-US':
            self.say("Are you?")
        elif language == 'fr-FR':
            self.say("Tu es ?")
        self.complete_request()
    
    @register("en-US","Thanks.for.*")
    @register("fr-FR",u"Merci (de|pour).*")
    def st_thanks_for(self, speech, language):
        if language == 'en-US':
            self.say("My pleasure. As always.")
        elif language == 'fr-FR':
            self.say("Tout le plaisir est pour moi. Comme toujours.")
        self.complete_request()
    
    @register("en-US",".*you're.*funny.*")
    @register("fr-FR",u".*(tu (es|est).*(drole|drôle)|MDR|LOL).*")
    def st_funny(self, speech, language):
        if language == 'en-US':
            self.say("LOL")
        elif language == 'fr-FR':
            rep = ["LOL","MDR"]
            self.say(random.choice(rep))
        self.complete_request()
    
    @register("en-US",".*guess.what.*")
    @register("fr-FR",u".*devine.quoi.*")
    def st_guess_what(self, speech, language):
        if language == 'en-US':
            self.say("Don't tell me... you were just elected President of the United States, right?")
        if language == 'fr-FR':
            self.say("Ne me dit pas... Tu as gagné à l'EuroMillion, pas vrai ?")
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
    @register("fr-FR",".*chante.*chanson.*|chante.*")
    def st_sing_song(self, speech, language):
        if language == 'en-US':
            self.say("Daisy, Daisy, give me your answer do...")
        elif language == 'fr-FR':
            self.say(u"J'aurais voulu être un artiste...")
            self.say(u"Désolé, je devrais payer des royalties si j'en dis plus.")
        self.complete_request()