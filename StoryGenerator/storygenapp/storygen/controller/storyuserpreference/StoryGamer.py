from storygenapp.storygen.SimpleNLG import SimpleNLG
from datetime import date
from datetime import datetime
from storygenapp.storygen.controller.storyuserpreference.StoryGeneral import StoryGeneral


class StoryGamer:
    userpref = "The Gamer"

    def __init__(self):
        self.simplenlg = SimpleNLG()
        self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()
        self.storygeneral = StoryGeneral()

    def generategamer(self, gamerobj, pronoun):
        self.pronoun = pronoun

        games = gamerobj.getSpecificParamType("Game")

        for g in games:
            assertiongamer = gamerobj.getAssertionsBySpecificParam("Game", g[0])

            play_assertions = gamerobj.getAssertionsByType(assertiongamer, "gamer_play")
            if len(play_assertions) != 0:
                self.documentlist.append(self.playphrase(g[0], play_assertions))

            activity_assertions = gamerobj.getAssertionsByType(assertiongamer, "gamer_activity")
            if len(activity_assertions) != 0:
                sentences = self.storygeneral.activityphrase(assertions=activity_assertions, userpref=self.userpref,
                                                             pronoun=self.pronoun)
                for s in sentences:
                    self.documentlist.append(s)

            achievement_assertions = gamerobj.getAssertionsByType(assertiongamer, "gamer_achievement")
            if len(achievement_assertions) != 0:
                self.documentlist.append(self.achievementphrase(achievement_assertions))

            event_assertions = gamerobj.getAssertionsByType(assertiongamer, "gamer_event")
            if len(event_assertions) != 0:
                sentences = self.storygeneral.eventphrase(assertions=event_assertions, userpref=self.userpref, pronoun=self.pronoun)
                for s in sentences:
                    self.documentlist.append(s)

            fanachievement_assertions = gamerobj.getAssertionsByType(assertiongamer, "gamer_fan_achievement")
            if len(fanachievement_assertions) != 0:
                self.fan_achievementphrase(fanachievement_assertions)

            sentiment_assertions = gamerobj.getAssertionsByType(assertiongamer, "gamer_sentiment")
            if len(sentiment_assertions) != 0:
                sentences = self.storygeneral.sentimentphrase(assertions=sentiment_assertions, userpref=self.userpref)
                for s in sentences:
                    self.documentlist.append(s)

        paragraph = self.simplenlg.nlgfactory.createParagraph(self.documentlist)

        story = self.simplenlg.realiser.realise(paragraph).getRealisation()
        print(story)

        return story

    def playphrase(self, game, play_assertions):
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("play")
        s.setObject(game)

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        p = self.simplenlg.nlgfactory.createClause()
        p.setVerb("is")
        p.addPreModifier("which")

        for pa in play_assertions:
            if pa.getspecificparameter("Game") == game:
                type = self.simplenlg.nlgfactory.createNounPhrase("a", pa.getspecificparameter("Type"))
                c.addCoordinate(type)

        p.setObject(c)
        s.addModifier(p)

        return self.simplenlg.nlgfactory.createSentence(s)

    def activityphrase(self, assertions):

        activities = self.getaction_activity(assertions)

        for activity in activities:
            s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
            s.setSubject(self.pronoun)
            s.setVerb(activity[0])
            cpe = self.simplenlg.CoordinatedPhraseElement()

            for a in assertions:
                actionparam = a.getspecificparameter("Activity")
                if actionparam is not None and actionparam.lower() == activity[0].lower():

                    np = self.simplenlg.nlgfactory.createNounPhrase(a.getspecificparameter("Game"))

                    location = a.getspecificparameter("Location")
                    tagged_friends = a.getspecificparameter("Tagged_Friends")

                    if location is None or tagged_friends is not None:
                        s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)

                    if a.getspecificparameter("Location") is not None:
                        pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                        pp1.addComplement(a.getspecificparameter("Location"))
                        pp1.setPreposition("at")
                        np.addModifier(pp1)

                    if a.getspecificparameter("Tagged_Friends") is not None:
                        pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                        pp2.addComplement(a.getspecificparameter("Tagged_Friends"))
                        pp2.setPreposition("with")
                        np.addModifier(pp2)

                    cpe.addCoordinate(np)

            s.setObject(cpe)

            self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))

    def getaction_activity(self, assertions):
        activities = []

        for a in assertions:
            activity = a.getspecificparameter("Activity")

            if activity != None:
                activities.append(activity)

        activities = [[ft, activities.count(ft)] for ft in set(activities)]
        activities.sort(key=lambda k: (k[0], -k[1]), reverse=True)
        # print(activities)

        return activities

    def achievementphrase(self, assertions):
        clause = self.simplenlg.nlgfactory.createClause()
        clause.setSubject(self.pronoun)
        clause.setVerb("win")
        clause.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
        clause.setFeature(self.simplenlg.Feature.CUE_PHRASE, "in fact,")

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()
        for a in assertions:
            np = self.simplenlg.nlgfactory.createNounPhrase(a.getspecificparameter("Achievement"))
            c.addCoordinate(np)

        clause.setObject(c)

        return self.simplenlg.nlgfactory.createSentence(clause)

    def fan_achievementphrase(self, assertions):

        for a in assertions:
            achievement = a.getspecificparameter("Achievement")
            if achievement != "null" and achievement is not None and achievement != "":
                s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
                s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "Other than that,")
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
            pp1.addComplement(a.getspecificparameter("Game"))
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

    def eventphrase(self, assertions):

        for a in assertions:
            s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
            s.setSubject(self.pronoun)
            s.setVerb(a.getspecificparameter("Activity"))
            s.setObject(a.getspecificparameter("Event"))

            if a.getspecificparameter("Location") is not None:
                pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                pp1.addComplement(a.getspecificparameter("Location"))
                pp1.setPreposition("at")
                s.addModifier(pp1)

            if a.getspecificparameter("Tagged_Friends") is not None:
                pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                pp2.addComplement(a.getspecificparameter("Tagged_Friends"))
                pp2.setPreposition("with")
                s.addModifier(pp2)

            eventdate = a.getspecificparameter("Date")
            if eventdate is not None:
                eventdateformat = datetime.strptime(eventdate, '%m/%d/%Y').date()
                eventdate = eventdateformat.strftime("%B %d %Y")

                pp3 = self.simplenlg.nlgfactory.createPrepositionPhrase()
                pp3.addComplement(eventdate)

                if eventdateformat < date.today():
                    pp3.setPreposition("last")
                    s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
                else:
                    pp3.setPreposition("on")
                    s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.FUTURE)
                s.addModifier(pp3)

            self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))
