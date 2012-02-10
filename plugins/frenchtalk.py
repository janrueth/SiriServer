#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Cédric Boverie

from plugin import *

class frenchtalk(Plugin):

    @register("fr-FR", u"(.*J'ai.*faim.*)|(J'ai.*soif.*)")
    def st_faim(self, speech, language):
        self.say(u"Si tu m'invites, je te montrerai peut-être le chemin.");
        self.complete_request()

    @register("fr-FR", "(.*Youtube.*)|(.*Dailymotion.*)")
    def st_youtube(self, speech, language):
        self.say(u"Je ne peux pas encore te montrer de vidéos, désolé.");
        self.complete_request()

    @register("fr-FR", "(.*Qui.*es.*tu.*)|(Comment.*appelle.*)")
    def st_quiestu(self, speech, language):
        self.say(u"Je suis Siri.");
        self.complete_request()

    @register("fr-FR", "(Coucou.*)")
    def st_aimer(self, speech, language):
        self.say(u"Bonjour.");
        self.complete_request()
		
    @register("fr-FR", u"(Au revoir.*)|((A|à) bientôt.*)")
    def st_aurevoir(self, speech, language):
        self.say(u"A bientôt.");
        self.complete_request()
	
    @register("fr-FR", "(.*Je.*travail.*)")
    def st_travaille(self, speech, language):
        self.say(u"D'accord, je vous laisse travailler.");
        self.complete_request()
		
    @register("fr-FR", "((Veux|Veut).*tu.*)|(.*tu.*(veux|veut).*)|(as.*tu besoin d.*)")
    def st_besoin(self, speech, language):
        self.say(u"Merci, mais j'ai déjà tout ce dont j'ai besoin dans le nuage.");
        self.complete_request()
		
    @register("fr-FR", "(Je.*aime)")
    def st_aime(self, speech, language):
        self.say(u"Désolé, un assistant virtuel ne peut pas éprouver de sentiment.");
        self.say(u"Voilà, c'est dit.");
        self.complete_request()
		
    @register("fr-FR", u"(J'aime.*)")
    def st_aimer(self, speech, language):
        self.say(u"Moi aussi.");
        self.complete_request()

    @register("fr-FR", u"(Je déteste.*)|(J'ai horreur.*)|(Je n'aime pas.*)")
    def st_aimer(self, speech, language):
        self.say(u"Chaqu'un ses goûts.");
        self.say(u"Heureusement, nous n'avons pas forcément les-mêmes.");
        self.complete_request()
		
    @register("fr-FR", "(Hello)")
    def st_frenglish(self, speech, language):
        self.say(u"Oh Oh, tu essayes de parler anglais, c'est bien.");
        self.say(u"Mais ça ne marchera pas, tu as configuré Siri en français.");
        self.complete_request()
		
    @register("fr-FR", u"(.*connard.*)|(.*idiot.*)|(.*crétin.*)|(.*pétasse.*)|(.*connasse.*)|(.*salope.*)|(.*putain.*)|(.*merde.*)|(.*débile.*)|(.* con.*)")
    def st_insultes(self, speech, language):
        self.say(u"Oh Oh, tu parles un langage bien châtié, il me semble.");
        self.say(u"Repose-moi ta question poliment.");
        self.complete_request()
		
    @register("fr-FR", u"(j.*envie.*)")
    def st_envies(self, speech, language):
        self.say(u"Moi pas.");
        self.say(u"Heureusement, nous n'avons pas les mêmes envies.");
        self.complete_request()