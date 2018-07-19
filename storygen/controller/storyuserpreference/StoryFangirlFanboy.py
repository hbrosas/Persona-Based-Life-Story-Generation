from SimpleNLG import SimpleNLG
from datetime import date
from datetime import datetime


class StoryFangirlFanboy:

    def __init__(self):
        self.simplenlg = SimpleNLG()
        self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()

    def generateFangirlFanboy(self, fangirlobj, pronoun):
        self.pronoun = pronoun
        fanoflist = fangirlobj.getSpecificParamType("FanOf")

        for f in fanoflist:
            assertionfan = fangirlobj.getAssertionsBySpecificParam("FanOf", f[0])

            self.documentlist.append(self.fanofphrase(f[0]))

            describe_assertions = fangirlobj.getAssertionsByType(assertionfan, "fan_describe")
            if len(describe_assertions) != 0:
                self.documentlist.append(self.describephrase(describe_assertions, f[0]))

            type = fangirlobj.getSpecificParamTypeWithAssertion("Type", assertionfan)

            for t in type:
                # print("TYPE ", t[0])
                assertiontype = fangirlobj.getAssertionBySpecificParamInAssertion("Type", t[0], assertionfan)

                activity_assertions = fangirlobj.getAssertionsByType(assertiontype, "fan_activity")
                if len(activity_assertions) != 0:
                    self.activityphrase(activity_assertions)

                event_assertions = fangirlobj.getAssertionsByType(assertiontype, "fan_event")
                if len(event_assertions) != 0:
                    self.eventphrase(event_assertions)

            sentiment_assertions = fangirlobj.getAssertionsByType(assertionfan, "fan_sentiment")
            if len(sentiment_assertions) != 0:
                self.sentimentphrase(sentiment_assertions)

        paragraph = self.simplenlg.nlgfactory.createParagraph(self.documentlist)

        story = self.simplenlg.realiser.realise(paragraph).getRealisation()
        print(story)

        return story

    def fanofphrase(self, fanof):
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        s.setSubject(self.pronoun)
        s.setVerb("is")

        object = self.simplenlg.nlgfactory.createNounPhrase("a", "fan")
        s.setObject(object)

        pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp.addComplement(fanof)
        pp.setPreposition("of")
        s.addModifier(pp)

        return self.simplenlg.nlgfactory.createSentence(s)

    def describephrase(self, assertions, fanof):
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        s.setSubject(self.pronoun)
        s.setVerb("describe")
        s.setObject(fanof)

        pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp.setPreposition("as")

        for a in assertions:
            description = a.getspecificparameter(param_name="Description")
            c.addCoordinate(self.simplenlg.nlgfactory.createNounPhrase(description))

        pp.addComplement(c)
        s.addModifier(pp)

        return self.simplenlg.nlgfactory.createSentence(s)

    def activityphrase(self, assertions):

        actions = self.getaction_activity(assertions)

        for action in actions:
            s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
            s.setSubject(self.pronoun)
            s.setVerb(action[0])
            s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
            cpe = self.simplenlg.CoordinatedPhraseElement()

            for a in assertions:
                actionparam = a.getspecificparameter("Activity")
                if actionparam is not None and actionparam.lower() == action[0].lower():

                    np = self.simplenlg.nlgfactory.createNounPhrase(a.getspecificparameter("Type"))

                    if a.getspecificparameter("FanOf") is not None:
                        pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                        pp1.addComplement(a.getspecificparameter("FanOf"))
                        pp1.setPreposition("of")
                        np.addModifier(pp1)

                    if a.getspecificparameter("Location") is not None:
                        pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                        pp2.addComplement(a.getspecificparameter("Location"))
                        pp2.setPreposition("at")
                        np.addModifier(pp2)

                    if a.getspecificparameter("Tagged_Friends") is not None:
                        pp3 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                        pp3.addComplement(a.getspecificparameter("Tagged_Friends"))
                        pp3.setPreposition("with")
                        np.addModifier(pp3)

                    cpe.addCoordinate(np)

            s.setObject(cpe)

            self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))

    def getaction_activity(self, assertions):
        actions = []

        for a in assertions:
            action = a.getspecificparameter("Activity")

            if action != None:
                actions.append(action)

        actions = [[ft, actions.count(ft)] for ft in set(actions)]
        actions.sort(key=lambda k: (k[0], -k[1]), reverse=True)
        # print(actions)

        return actions

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
            pp1.addComplement(a.getspecificparameter("FanOf"))
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
