from storygenapp.storygen.SimpleNLG import SimpleNLG
from storygenapp.storygen.controller.storyuserpreference.StoryGeneral import StoryGeneral

class StoryFoodie:
    meals = ['breakfast', 'lunch', 'dinner', 'brunch', 'meal', 'snacks']
    userpref = "The Foodie"

    def __init__(self):
        self.simplenlg = SimpleNLG()
        self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()
        self.storygeneral = StoryGeneral()

    def generatefoodie(self, foodieobj, pronoun):
        self.pronoun = pronoun
        foodtypes = foodieobj.getSpecificParamType("Type")

        for ft in foodtypes:
            assertionft = foodieobj.getAssertionsBySpecificParam("Type", ft[0])

            if ft[1] > 1:
                self.documentlist.append(self.introphrase(ft[0]))

            describe_assertions = foodieobj.getAssertionsByType(assertionft, "food_describe")
            if len(describe_assertions) != 0:
                self.documentlist.append(self.describephrase(describe_assertions))

            activity_assertions = foodieobj.getAssertionsByType(assertionft, "food_activity")
            if len(activity_assertions) != 0:
                sentences = self.storygeneral.activityphrase(assertions=activity_assertions, userpref=self.userpref, pronoun=self.pronoun)

                for s in sentences:
                    self.documentlist.append(s)
                # self.activityphrase(activity_assertions)

            sentiment_assertions = foodieobj.getAssertionsByType(assertionft, "food_sentiment")
            if len(sentiment_assertions) != 0:
                sentences = self.storygeneral.sentimentphrase(assertions=sentiment_assertions, userpref=self.userpref)
                for s in sentences:
                    self.documentlist.append(s)
                # self.sentimentphrase(sentiment_assertions)

        assertion_noft = foodieobj.getAssertionsNoType("Type")

        describe_assertionsnoft = foodieobj.getAssertionsByType(assertion_noft, "food_describe")
        if len(describe_assertionsnoft) != 0:
            self.documentlist.append(self.describephrase(describe_assertionsnoft))

        activity_assertionsnoft = foodieobj.getAssertionsByType(assertion_noft, "food_activity")
        if len(activity_assertionsnoft) != 0:
            sentences = self.storygeneral.activityphrase(activity_assertionsnoft, self.userpref, self.pronoun)
            for s in sentences:
                self.documentlist.append(s)
            # self.activityphrase(activity_assertionsnoft)
            # self.specificactivityphrase(activity_assertionsnoft)

        sentiment_assertionsnoft = foodieobj.getAssertionsByType(assertion_noft, "food_sentiment")
        if len(sentiment_assertionsnoft) != 0:
            sentences = self.storygeneral.sentimentphrase(sentiment_assertionsnoft, self.userpref)
            for s in sentences:
                self.documentlist.append(s)
            # self.sentimentphrase(sentiment_assertionsnoft)

        paragraph = self.simplenlg.nlgfactory.createParagraph(self.documentlist)

        story = self.simplenlg.realiser.realise(paragraph).getRealisation()
        print(story)

        return story

    def introphrase(self, foodtype):
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        s.setSubject(self.pronoun)
        s.setVerb("is")

        object = self.simplenlg.nlgfactory.createNounPhrase("a", "lover")
        object.addPreModifier(foodtype)
        s.setObject(object)

        return self.simplenlg.nlgfactory.createSentence(s)

    def describephrase(self, assertions):
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        s.setSubject(self.pronoun)
        s.setVerb("describe")

        for a in assertions:
            clause = self.simplenlg.nlgfactory.createClause()
            clause.setSubject(a.getspecificparameter(param_name="Food"))

            food_org = a.getspecificparameter("Organization")
            description = a.getspecificparameter(param_name="Description")

            if food_org is not None:
                pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                pp1.addComplement(food_org)
                pp1.setPreposition("in")
                clause.addModifier(pp1)

            pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp2.setPreposition("is")

            adjp = self.simplenlg.AdjPhraseSpec(self.simplenlg.nlgfactory)
            adjp.setAdjective(description)

            pp2.addComplement(adjp)
            clause.addModifier(pp2)

            c.addCoordinate(clause)

        s.setObject(c)

        return self.simplenlg.nlgfactory.createSentence(s)

    def activityphrase(self, assertions):

        actions = self.getaction_activity(assertions)

        for action in actions:
            specific_actassertions = []
            s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
            s.setSubject(self.pronoun)
            s.setVerb(action[0])
            cpe = self.simplenlg.CoordinatedPhraseElement()

            for a in assertions:
                actionparam = a.getspecificparameter("Action")
                if actionparam is not None and actionparam.lower() == action[0].lower():

                    if actionparam in self.meals:
                        a.setspecificparam("Action", "eat")
                        a.setspecificparam("Food", actionparam)
                        s.setVerb("eat")

                    np = self.simplenlg.nlgfactory.createNounPhrase(a.getspecificparameter("Food"))

                    organization = a.getspecificparameter("Organization")
                    location = a.getspecificparameter("Location")
                    tagged_friends = a.getspecificparameter("Tagged_Friends")

                    if location is not None or tagged_friends is not None:
                        specific_actassertions.append(a)

                    else:
                        if organization is not None:
                            pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                            pp1.addComplement(organization)
                            pp1.setPreposition("in")
                            np.addModifier(pp1)

                    cpe.addCoordinate(np)

            s.setObject(cpe)

            self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))
            self.specificactivityphrase(specific_actassertions)

    def specificactivityphrase(self, assertions):
        actions = self.getaction_activity(assertions)

        for action in actions:

            for a in assertions:
                s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
                s.setSubject(self.pronoun)
                s.setVerb(action[0])
                s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
                actionparam = a.getspecificparameter("Action")
                if actionparam is not None and actionparam.lower() == action[0].lower():

                    np = self.simplenlg.nlgfactory.createNounPhrase(a.getspecificparameter("Food"))

                    organization = a.getspecificparameter("Organization")
                    location = a.getspecificparameter("Location")
                    tagged_friends = a.getspecificparameter("Tagged_Friends")

                    if organization is not None:
                        pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                        pp1.addComplement(organization)
                        pp1.setPreposition("in")
                        np.addModifier(pp1)

                    if location is not None:
                        pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                        pp2.addComplement(location)
                        pp2.setPreposition("at")
                        np.addModifier(pp2)

                    if tagged_friends is not None:
                        pp3 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                        pp3.addComplement(tagged_friends)
                        pp3.setPreposition("with")
                        np.addModifier(pp3)

                    s.setObject(np)

                self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))

    def getaction_activity(self, assertions):
        actions = []

        for a in assertions:
            action = a.getspecificparameter("Action")

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
            pp1.addComplement(a.getspecificparameter("Food"))
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
