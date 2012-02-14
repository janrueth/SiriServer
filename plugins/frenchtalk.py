#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Cédric Boverie

import random
from plugin import *
from siriObjects.websearchObjects import WebSearch

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
        self.say(u"Je suis Siri.")
        self.complete_request()
		
    @register("fr-FR", u"(Au revoir.*)|((A|à) bientôt.*)")
    def ft_aurevoir(self, speech, language):
        self.say(u"A bientôt.");
        self.complete_request()
	
    @register("fr-FR", ".*Je.*travail.*")
    def ft_travaille(self, speech, language):
        self.say(u"D'accord, je vous laisse travailler.");
        self.complete_request()
		
    @register("fr-FR", u"(Veux|Veut).*tu.*|.*tu.*(veux|veut).*|as.*tu besoin d.*|.*tu.*(as|a).*besoin d.*|.*qu.*(puis|peux|peut).*toi.*|.*que.*veux.*tu")
    def ft_veuxtu(self, speech, language):
        rep = [u"Merci, mais j'ai déjà tout ce dont j'ai besoin dans le nuage.", u"J'ai déjà tout ce dont j'ai besoin."]
        self.say(random.choice(rep));
        self.complete_request()

    @register("fr-FR", u".*(j'ai|j'|je).*besoin.*")
    def ft_besoin(self, speech, language):
        rep = [u"Désolé, je n'ai aucun moyen de vous en procurer.", u"J'espère que vous trouverer ce que vous chercher.", u"Je suis désolé, je ne peux pas vous aider."]
        self.say(random.choice(rep))
        self.complete_request()
		
    @register("fr-FR", "Je.*aime")
    def ft_jetaime(self, speech, language):
        self.say(u"Désolé, un assistant virtuel ne peut pas éprouver de sentiment.");
        self.say(u"Voilà, c'est dit.")
        self.complete_request()
		
    @register("fr-FR", u"J'aime.*")
    def ft_aime(self, speech, language):
        self.say(u"Moi aussi.")
        self.complete_request()

    @register("fr-FR", u"(Je déteste.*)|(J'ai horreur.*)|(Je n'aime pas.*)")
    def ft_deteste(self, speech, language):
        self.say(u"Chaqu'un ses goûts.");
        self.say(u"Heureusement, nous n'avons pas forcément les-mêmes.");
        self.complete_request()

    @register("fr-FR", u".*tu.*aimes?.*")
    def ft_aimes(self, speech, language):
        rep = [u"Il s'agit de vous, pas de moi."]
        self.say(random.choice(rep));
        self.complete_request()
		
    @register("fr-FR", "Hello")
    def ft_frenglish(self, speech, language):
        self.say(u"Oh Oh, tu essayes de parler anglais, c'est bien.");
        self.say(u"Mais ça ne marchera pas, tu as configuré Siri en français.");
        self.complete_request()
		
    @register("fr-FR", u".*(ta gueule).*")
    def ft_tg(self, speech, language):
        choix = random.randint(0,2)
        if choix == 1:
            self.say(u"J'essaye simplement de me rendre utile.");
        elif choix == 2:
            self.say(u"Désolé, je vais me suicider.");
        else:
            self.say(u"Excusez-moi. J'essayais simplement de vous aider.")
        self.complete_request()
		
    @register("fr-FR", u"(.*connard.*)|(.*idiot.*)|(.*crétin.*)|(.*pétasse.*)|(.*connasse.*)|(.*salope.*)|(.*putain.*)|(.*merde.*)|(.*débile.*)|(.* con .*)")
    def ft_insultes(self, speech, language):
        choix = random.randint(0,3)
        if choix == 1:
            self.say(u"Oh Oh, tu parles un langage bien châtié, il me semble.");
            self.say(u"Repose-moi ta question poliment.");
        elif choix == 2:
            self.say(u"Je vous respecte.");
        elif choix == 3:
            self.say(u"Allons, allons.");
        else:
            self.say("Demandez gentiment, maintenant.")
        self.complete_request()

    @register("fr-FR", u".*(suis|suit).*(saoul|soul|soûl|sous)|(je|j'ai).*alcool.*")
    def ft_glouglou(self, speech, language):
        rep = [u"Ne buvez jamais si vous avez du travail à faire, ne buvez jamais seul et ne buvez jamais lorsque le soleil brille.", u"Ne comptez pas sur moi pour vous ramener chez vous."]
        self.say(random.choice(rep))
        self.complete_request()
		
    @register("fr-FR", u"j.*envie.*")
    def ft_envies(self, speech, language):
        rep = [u"Moi pas. Heureusement, nous n'avons pas les mêmes envies.", u"Excellent choix, j'aurais fait pareil.", u"Excellente décision, j'aurais fait pareil"]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u"je.*suis.*tueur.*")
    def ft_envies(self, speech, language):
        rep = [u"Je ne peux pas ne pas être d'accord."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u"tu.*(est|es).*(genie|genial|génie|génial|intelligent|merveilleux)")
    def ft_genie(self, speech, language):
        choix = random.randint(0,3)
        if choix == 1:
            self.say(u"Cela nous fait un point commun.")
            self.say(u"Nous savons tout les 2 que je suis génial.")
        elif choix == 2:
            self.say(u"Oui. J'ai un fan")
        elif choix == 3:
            self.say(u"Je suis bon, mais pas excellent.")
        else:
            self.say(u"Il y en a là-dedans !")
        self.complete_request()

    @register("fr-FR", u".*couleur.*cheval.*napoléon")
    def ft_napoleon(self, speech, language):
        self.say(u"Le cheval de Napoléon est blanc.");
        self.complete_request()

    @register("fr-FR", u".*fai(s|t).*(tu|quoi).*")
    def ft_faitquoi(self, speech, language):
        rep = [u"Je suis en train de te parler.", u"Je te parle, mais tu le savais déjà.", u"J'entretiens une conversation très intéressante avec un bon ami.", u"Je suis en pleine conversation avec quelqu'un.", u"Je parle à une personnne très sympathique."]
        self.say(random.choice(rep));
        self.complete_request()

    @register("fr-FR", u".*(iphone 5|iphone cinq).*")
    def ft_iphonenext(self, speech, language):
        rep = [u"Désolé, c'est convidentiel",u"Il sortira le... Désolé, un problème technique m'empêche de répondre"]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*(iphone|ipad|ipod|itouch|imac|ibook|ibidule|macbook|mac book|apple).*")
    def ft_iphone(self, speech, language):
        self.say(u"Tout ce que vous devez savoir sur les produits Apple se trouve sur le site web d'Apple...");
        button = Button(text=u"Aller sur Apple.com/fr", commands=[OpenLink(ref="http://www.apple.com/fr")])
        self.send_object(AddViews(self.refId, views=[button]))
        self.complete_request()

    @register("fr-FR", u".*(Bon(ne) ann(é|e)e|Joyeux No(e|ë)l).*")
    def ft_fete(self, speech, language):
        self.say(u"Merci | Amusez-vous bien.");
        self.complete_request()

    @register("fr-FR", u".*(Quan(t|d).*est?.*no(e|ë)l).*")
    def ft_quandnoel(self, speech, language):
        self.say(u"Noël, c'est le 25 décembre. J'espère être en congé ce jour-là.");
        self.complete_request()

    @register("fr-FR", u".*Quan(t|d).*est?.saint.valentin.*")
    def ft_quandstvalentin(self, speech, language):
        self.say(u"La Saint-Valentin, c'est le 14 février.");
        self.complete_request()

    @register("fr-FR", u".*(c.est (ça|sa|ca)).*")
    def ft_cestca(self, speech, language):
        self.say(u"Parfois je m'épate moi-même.")
        self.complete_request()

    @register("fr-FR", u".*(dieu|religion).*")
    def ft_religion(self, speech, language):
        self.say(u"Si possible, veuillez poser ce genre de questions à quelqu'un de plus qualifié que moi. Un être humain serait préférable.")
        self.complete_request()

    @register("fr-FR", u"(je vai(s|t) dormir).*")
    def ft_vaisdormir(self, speech, language):
        rep = [u"D'accord, à demain.",u"Pas de problème, passe une bonne nuit.",u"Aucun soucis, passe une bonne nuit."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u"(je vai(s|t)).*")
    def ft_vais(self, speech, language):
        rep = [u"D'accord.",u"Pas de problème.",u"Aucun soucis.",u"Amusez-vous bien."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*(bonne nuit|(a|à) demain).*")
    def ft_bonnenuit(self, speech, language):
        rep = [u"Bonne nuit.",u"Passe une bonne nuit.",u"Bonne nuit à vous aussi.",u"A demain."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*(autre (chose|chause)).*")
    def ft_autrechose(self, speech, language):
        rep = [u"Désolé, je n'ai rien d'autre à vous proposer.",u"Désolé, je n'ai rien d'autre en stock.",u"C'est tout.",u"Je ne crois pas."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*((comprends?|sais|sait).*rien).*")
    def ft_comprendrien(self, speech, language):
        rep = [u"Vraiment ?",u"Je fais ce que je peux, pas ce que je veux.",u"Désolé, je fais pourtant de mon mieux", u"Ah oui ? Pourtant, je fais mon possible pour vous aider."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u"tu.*es.*(mignon|gentil|sage).*")
    def ft_mignon(self, speech, language):
        rep = [u"Merci. On peut se remettre au boulot, maintenant ?", u"Merci. Allez, au travail !"]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*(je|j).*en.*(fout|fou|foot).*|.*je trouve.*|.*(t'es|tu es|tes|tu est) pas.*|tu pues?|tu sens")
    def ft_chacunsonavis(self, speech, language):
        rep = [u"Je crois que chacun peut avoir son opinion là-dessus.",u"Chaque personne peut avoir un avis différent.",u"Vous êtes libre de penser ce que vous voulez.", u"Vous êtes libre de croire ce que vous vouler."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*(pourquoi|pour quoi).*")
    def ft_pourquoi(self, speech, language):
        rep = [u"Je n'en sais rien. Pour vous dire la vérité, je me le demande aussi.", u"Je ne sais pas. Pour vous dire la vérité, je me pose cette question tout les jours.", u"Je n'en ai absolument aucune idée.", u"Je ne sais pas.", u"Je n'en ai aucune idée"]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u"(c'est|cest|ces|cet|ce|sa|c).*vrai.*")
    def ft_cvrai(self, speech, language):
        rep = [u"C'est agréable d'avoir raison."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*(tu devrais).*")
    def ft_tdevrais(self, speech, language):
        rep = [u"C'est noté.",u"Je le note.", u"Je tâcherai de m'en rappeler.", u"Je m'en souviendrai.", u"Je m'en rappellerai."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*(tu|t'es).*(chiant|chier|chié).*")
    def ft_tchiant(self, speech, language):
        rep = [u"Si seulement j'étais plus marrant.", u"Je fais de mon mieux..."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*moi.*aussi.*")
    def ft_moiaussi(self, speech, language):
        rep = [u"C'est parfait.", u"Aucun problème.", u"Faites ce que bon vous semble."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*(j'ai|j'|je).*probl(è|e)me.*")
    def ft_jaiprobleme(self, speech, language):
        rep = [u"Désolé, je n'ai aucune solution à vous proposer.", u"Je ne sais pas. Peut-être que les membres du Genius Bar pourront vous aider."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*quel.*meilleur.*tablette.*")
    def ft_meilleurtab(self, speech, language):
        rep = [u"L'iPad d'Apple est ce qu'il y a de mieux. Et ce n'est pas seulement moi qui le dis."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*d.accord.*")
    def ft_daccord(self, speech, language):
        rep = [u"Ça me va si ça vous va.","Tant que ça vous va, ça me va."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*Pas.du.tout.*")
    def ft_pasdutout(self, speech, language):
        rep = [u"OK.", u"J'ai compris.", u"D'accord."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*ok.*")
    def ft_ok(self, speech, language):
        rep = [u"Ok.", u"D'accord", "Pas de problème."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*pas de probl(e|è)me.*")
    def ft_pasdeprobleme(self, speech, language):
        rep = [u"Parfait !", u"Bien.", u"C'est agréable à entendre.", u"Ravi de l'entendre."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*qu.*sai(s|t).*faire.*")
    def ft_qqtusaisfaire(self, speech, language):
        rep = [u"Tout et n'importe quoi. Ou peut-être rien...", u"Je peux tout faire, si tu me le demandes gentillement.", u"La liste des commandes disponibles n'est pas encore disponible."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*je.*suis.*malade.*")
    def ft_malade(self, speech, language):
        choix = random.randint(0,2)
        if choix == 1:
            answer = self.ask(u"Quels sont les symptômes ?")
            self.say(u"Malheureusement, je pense que votre maladie est incurable.")
        elif choix == 2:
            self.say("Soignez-vous bien.");
        else:
            self.say(u"S'il vous plait, éloignez-vous du téléphone. Je ne voudrais pas être contaminé.")
            
        self.complete_request()

    @register("fr-FR", u".*je.*(suis|sens|sent).*seul.*")
    def ft_seul(self, speech, language):
        rep = [u"Si vous me le demander, je peux vous chercher de la compagnie.", u"Vous êtes seul ? Et moi ! Je compte pour du beurre ?", u"Voyons, je suis là.", u"Je crois que vous oubliez que je suis là."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u".*(drogue|coca(i|ï)ne).*")
    def ft_drogue(self, speech, language):
        rep = [u"La drogue, c'est mal.", u"Je vous conseille vivement d'arrêter."]
        self.say(random.choice(rep))
        self.complete_request()


    @register("fr-FR", u".*j.*vol(é|e).*")
    def ft_vole(self, speech, language):
        rep = [u"Le vol, c'est mal.", u"Qui vole un oeuf, vole un boeuf."]
        self.say(random.choice(rep))
        self.complete_request()

    @register("fr-FR", u"je.*suis.*")
    def ft_jesuis(self, speech, language):
        rep = [u"Tu es ce que tu es, pas la peine de m'en vouloir pour ça.", u"Ce que tu es ne dépends que de toi, pas de moi.", u"Et alors ? Tu es ce que tu es, un point c'est tout.", u"Tu l'es, et tu le resteras probablement encore longtemps.", u"A ce rythme-là, tu le seras encore dans très longtemps..."]
        self.say(random.choice(rep))
        self.complete_request()

