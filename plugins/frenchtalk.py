#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Cédric Boverie

from plugin import *

class frenchtalk(Plugin):

    @register("fr-FR", u"(.*J'ai.*faim.*)|(J'ai.*soif.*)")
    def ft_faim(self, speech, language):
        self.say(u"Si tu m'invites, je te montrerai peut-être le chemin.");
        self.complete_request()

    @register("fr-FR", "(.*Youtube.*)|(.*Dailymotion.*)")
    def ft_youtube(self, speech, language):
        self.say(u"Je ne peux pas encore te montrer de vidéos, désolé.");
        self.complete_request()

    @register("fr-FR", "(.*Qui.*es.*tu.*)|(Comment.*appelle.*)")
    def ft_quiestu(self, speech, language):
        self.say(u"Je suis Siri.");
        self.complete_request()

    @register("fr-FR", "Coucou.*")
    def ft_aimer(self, speech, language):
        self.say(u"Bonjour.");
        self.complete_request()
		
    @register("fr-FR", u"(Au revoir.*)|((A|à) bientôt.*)")
    def ft_aurevoir(self, speech, language):
        self.say(u"A bientôt.");
        self.complete_request()
	
    @register("fr-FR", ".*Je.*travail.*")
    def ft_travaille(self, speech, language):
        self.say(u"D'accord, je vous laisse travailler.");
        self.complete_request()
		
    @register("fr-FR", "((Veux|Veut).*tu.*)|(.*tu.*(veux|veut).*)|(as.*tu besoin d.*)")
    def ft_besoin(self, speech, language):
        self.say(u"Merci, mais j'ai déjà tout ce dont j'ai besoin dans le nuage.");
        self.complete_request()
		
    @register("fr-FR", "Je.*aime")
    def ft_aime(self, speech, language):
        self.say(u"Désolé, un assistant virtuel ne peut pas éprouver de sentiment.");
        self.say(u"Voilà, c'est dit.");
        self.complete_request()
		
    @register("fr-FR", u"J'aime.*")
    def ft_aimer(self, speech, language):
        self.say(u"Moi aussi.");
        self.complete_request()

    @register("fr-FR", u"(Je déteste.*)|(J'ai horreur.*)|(Je n'aime pas.*)")
    def ft_aimer(self, speech, language):
        self.say(u"Chaqu'un ses goûts.");
        self.say(u"Heureusement, nous n'avons pas forcément les-mêmes.");
        self.complete_request()
		
    @register("fr-FR", "Hello")
    def ft_frenglish(self, speech, language):
        self.say(u"Oh Oh, tu essayes de parler anglais, c'est bien.");
        self.say(u"Mais ça ne marchera pas, tu as configuré Siri en français.");
        self.complete_request()
		
    @register("fr-FR", u"(.*connard.*)|(.*idiot.*)|(.*crétin.*)|(.*pétasse.*)|(.*connasse.*)|(.*salope.*)|(.*putain.*)|(.*merde.*)|(.*débile.*)|(.* con .*)")
    def ft_insultes(self, speech, language):
        self.say(u"Oh Oh, tu parles un langage bien châtié, il me semble.");
        self.say(u"Repose-moi ta question poliment.");
        self.complete_request()
		
    @register("fr-FR", u"j.*envie.*")
    def ft_envies(self, speech, language):
        self.say(u"Moi pas.");
        self.say(u"Heureusement, nous n'avons pas les mêmes envies.");
        self.complete_request()		

    @register("fr-FR", u"tu.*(est|es).*(genie|genial|génie|génial)")
    def ft_genie(self, speech, language):
        self.say(u"Cela nous fait un point commun.");
        self.say(u"Nous savons tout les 2 que je suis génial.");
        self.complete_request()

    @register("fr-FR", u".*couleur.*cheval.*napoléon")
    def ft_napoleon(self, speech, language):
        self.say(u"Le cheval de Napoléon est blanc.");
        self.complete_request()

    @register("fr-FR", u".*fai(s|t).*(tu|quoi).*")
    def ft_faitquoi(self, speech, language):
        self.say(u"Je suis en train de te parler.");
        self.complete_request()
