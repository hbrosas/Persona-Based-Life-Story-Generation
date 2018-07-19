from SimpleNLG import SimpleNLG
from datetime import datetime


class StorySportsFanatic:

    def __init__(self):
        self.simplenlg = SimpleNLG()
        self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()

    def generatesportsfanatic(self, sportsfanaticobj, pronoun):
        self.pronoun = pronoun

        sports = sportsfanaticobj.getSpecificParamType("sport")

        for s in sports:
            assertionsport = sportsfanaticobj.getAssertionsBySpecificParam("Sport", s[0])

            play_assertions = sportsfanaticobj.getAssertionsByType(assertionsport, "sport_play")

            if s[1] > 1:
                self.documentlist.append(self.introphrase(s[0], play_assertions))

            # sport_partof : when the person is part of a sports team/speaks about his/her own team
            partof_assertions = sportsfanaticobj.getAssertionsByType(assertionsport, "sport_partof")
            if len(partof_assertions) != 0:
                self.documentlist.append(self.partofphrase(partof_assertions))

            # sport_play : when the person is doing a certain sport at a certain location with his/her friends
            if len(play_assertions) != 0:
                self.documentlist.append(self.playphrase(s[0], play_assertions))

            # sport_achievement: when the person has gained an achievement on his/her sport
            achievement_assertions = sportsfanaticobj.getAssertionsByType(assertionsport, "sport_achievement")
            if len(achievement_assertions) != 0:
                self.documentlist.append(self.achievementphrase(achievement_assertions))

            # sport_fan_achievement: when the sports team that person idolizes gained an achievement
            fan_assertions = sportsfanaticobj.getAssertionsByType(assertionsport, "sport_fan_achievement")
            if len(fan_assertions) != 0:
                self.documentlist.append(self.fanofphrase(fan_assertions))
                self.fanof_achievementphrase(fan_assertions)

            # sport_fan_activity: when the person is doing an activity for the sports team that he idolizes
            fanactivity_assertions = sportsfanaticobj.getAssertionsByType(assertionsport, "sport_fan_activity")
            if len(fanactivity_assertions) != 0:
                self.fanactivity_phrase(fanactivity_assertions)

            # sport_sentiment: when the person posts sentiments about a sport
            sentiment_assertions = sportsfanaticobj.getAssertionsByType(assertionsport, "sport_sentiment")
            if len(sentiment_assertions) != 0:
                self.sentimentphrase(sentiment_assertions)
 
        paragraph = self.simplenlg.nlgfactory.createParagraph(self.documentlist)

        story = self.simplenlg.realiser.realise(paragraph).getRealisation()
        print(story)

        return story

    def introphrase(self, sport, play_assertions):
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        s.setSubject(self.pronoun)
        s.setVerb("like")

        isfound = False

        for pa in play_assertions:
            if pa.getspecificparameter("Sport") == sport:
                isfound = True

        if isfound:
            clause = self.simplenlg.nlgfactory.createClause()
            clause.setVerb("play")
            clause.setObject(sport)
            clause.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.INFINITIVE)
            s.setObject(clause)
        else:
            s.setObject(sport)

        return self.simplenlg.nlgfactory.createSentence(s)

    def partofphrase(self, partof_assertions):
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("is")
        s.setObject("part")

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()
        for poa in partof_assertions:
            np = self.simplenlg.nlgfactory.createNounPhrase(poa.getspecificparameter("Team"))
            c.addCoordinate(np)

        pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp.addComplement(c)
        pp.setPreposition("of")
        s.addModifier(pp)

        return self.simplenlg.nlgfactory.createSentence(s)

    def playphrase(self, sport, play_assertions):
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("play")
        s.setObject(sport)

        cpe = self.simplenlg.CoordinatedPhraseElement()

        for pa in play_assertions:
            clause = self.simplenlg.nlgfactory.createClause()

            location = pa.getspecificparameter("Location")
            tagged_friends = pa.getspecificparameter("Tagged_Friends")

            if location is None or tagged_friends is not None:
                s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)

            if location is not None:
                pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                pp1.addComplement(location)
                pp1.setPreposition("at")
                clause.addModifier(pp1)

            if tagged_friends is not None:
                pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                pp2.addComplement(tagged_friends)
                pp2.setPreposition("with")
                clause.addModifier(pp2)

            cpe.addCoordinate(clause)

        s.addModifier(cpe)

        return self.simplenlg.nlgfactory.createSentence(s)

    def achievementphrase(self, assertions):
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("win")
        s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()
        for a in assertions:
            np = self.simplenlg.nlgfactory.createNounPhrase(a.getspecificparameter("Achievement"))
            c.addCoordinate(np)

        s.setObject(c)

        return self.simplenlg.nlgfactory.createSentence(s)

    def fanofphrase(self, assertions):
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("is")

        np = self.simplenlg.nlgfactory.createNounPhrase("a", "fan")
        s.setObject(np)

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for a in assertions:
            achievement = a.getspecificparameter("Achievement")
            if achievement == "null" or achievement is None or achievement == "":
                c.addCoordinate(a.getspecificparameter("FanOf"))

        pp = self.simplenlg.nlgfactory.createPrepositionPhrase()
        pp.addComplement(c)
        pp.setPreposition("of")
        s.addModifier(pp)

        return self.simplenlg.nlgfactory.createSentence(s)

    def fanof_achievementphrase(self, assertions):

        for a in assertions:
            achievement = a.getspecificparameter("Achievement")
            if achievement != "null" and achievement is not None and achievement != "":
                s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
                s.setSubject(self.pronoun)

                verb = self.simplenlg.nlgfactory.createVerbPhrase("is")
                s.setVerbPhrase(verb)

                np1 = self.simplenlg.nlgfactory.createNounPhrase("a", "fan")
                s.setObject(np1)
                pp = self.simplenlg.nlgfactory.createPrepositionPhrase()
                pp.addComplement(a.getspecificparameter("FanOf"))
                pp.setPreposition("of")
                s.addModifier(pp)

                clause = self.simplenlg.nlgfactory.createClause()
                clause.setSubject("who")
                clause.setVerb("win")
                clause.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
                clause.setObject(achievement)

                s.addModifier(clause)

                self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))

    def fanactivity_phrase(self, assertions):

        for a in assertions:
            s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
            s.setSubject(self.pronoun)
            s.setVerb("watch")
            s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
            s.setObject(a.getspecificparameter("FanOf"))

            event = a.getspecificparameter("Event")
            if event is not None:
                pp1 = self.simplenlg.nlgfactory.createPrepositionPhrase()
                pp1.addComplement(event)
                pp1.setPreposition("at")
                s.addModifier(pp1)

            date = a.getspecificparameter("Date")
            if date is not None:
                dateformat = datetime.strptime(date, '%m/%d/%Y').date()
                date = dateformat.strftime("%B %d %Y")

                pp2 = self.simplenlg.nlgfactory.createPrepositionPhrase()
                pp2.addComplement(date)
                pp2.setPreposition("last")
                s.addModifier(pp2)

            self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))

    def sentimentphrase(self, assertions):

        for a in assertions:
            s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
            s.setSubject(self.pronoun)
            s.setVerb("gives")
            s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
            sentiment = a.getspecificparameter("Sentiment_Class")
            if sentiment is not None and sentiment != "null" and sentiment != "":
                s.setObject(sentiment + " sentiment")
            else:
                s.setObject("Sentiment")

            pp1 = self.simplenlg.nlgfactory.createPrepositionPhrase()
            pp1.addComplement(a.getspecificparameter("Sport"))
            pp1.setPreposition("on")
            s.addComplement(pp1)

            s2 = self.simplenlg.nlgfactory.createClause()
            s2.setSubject(self.pronoun)
            s2.setVerb("say")
            s2.setObject("\"" + a.getspecificparameter("Sentiment") + "\"")
            s2.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
            s2.setFeature(self.simplenlg.Feature.COMPLEMENTISER, "since")
            s.addComplement(s2)

            self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))