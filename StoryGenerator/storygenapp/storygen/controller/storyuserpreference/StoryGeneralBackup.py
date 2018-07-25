from storygenapp.storygen.SimpleNLG import SimpleNLG
import storygenapp.storygen.controller.storyuserpreference.StoryFoodie
from storygenapp.storygen.controller.storyuserpreference.UserPreferenceObject import UserPreferenceObject
from datetime import date
from datetime import datetime


class StoryGeneral:
    meals = ['breakfast', 'lunch', 'dinner', 'brunch', 'meal', 'snacks']

    def __init__(self):
        self.simplenlg = SimpleNLG()
        # self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()

    def activityphrase(self, assertions, userpref, pronoun):
        self.pronoun = pronoun
        self.sentences = []

        actions = self.getaction_activity(assertions=assertions, userpref=userpref)

        for action in actions:
            specific_actassertions = []
            s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
            s.setSubject(self.pronoun)
            s.setVerb(action[0])
            cpe = self.simplenlg.CoordinatedPhraseElement()

            if userpref == "The Foodie":
                action_name = "Action"
            else:
                action_name = "Activity"

            action_assertions = UserPreferenceObject.getAssertionBySpecificParamInAssertion(self=UserPreferenceObject,
                                                                                            param_name=action_name,
                                                                                            param_value=action,
                                                                                            assertions=assertions)

            for a in action_assertions:

                object = ""
                actionparam = ""
                organization = None

                if userpref == "The Foodie":
                    object = a.getspecificparameter("Food")
                    organization = a.getspecificparameter("Organization")
                    actionparam = a.getspecificparameter("Action")

                elif userpref == "The Fangirl/Fanboy":
                    object = a.getspecificparameter("Type")
                    actionparam = a.getspecificparameter("Activity")

                # elif(userpref == "The Sports Fanatic"):
                #     object = a.getspecificparameter("FanOf")

                elif userpref == "The Gamer":
                    object = a.getspecificparameter("Game")
                    actionparam = a.getspecificparameter("Activity")

                if actionparam is not None and actionparam.lower() == action[0].lower():

                    if actionparam in self.meals:
                        a.setspecificparam("Action", "eat")
                        a.setspecificparam("Food", actionparam)
                        s.setVerb("eat")

                    np = self.simplenlg.nlgfactory.createNounPhrase(object)

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

            self.sentences.append(self.simplenlg.nlgfactory.createSentence(s))
            self.specificactivityphrase(specific_actassertions, userpref)

        return self.sentences

    def specificactivityphrase(self, assertions, userpref):
        actions = self.getaction_activity(assertions, userpref)

        for action in actions:

            for a in assertions:
                s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
                s.setSubject(self.pronoun)
                s.setVerb(action[0])
                s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
                if userpref == "The Foodie":
                    actionparam = a.getspecificparameter("Action")
                else:
                    actionparam = a.getspecificparameter("Activity")

                if actionparam is not None and actionparam.lower() == action[0].lower():

                    object = ""
                    organization = None

                    if userpref == "The Foodie":
                        object = a.getspecificparameter("Food")
                        organization = a.getspecificparameter("Organization")

                    elif userpref == "The Fangirl/Fanboy":
                        object = a.getspecificparameter("Type")
                        # elif(userpref == "The Sports Fanatic"):
                        #     object = a.getspecificparameter("FanOf")
                    elif userpref == "The Gamer":
                        object = a.getspecificparameter("Game")

                    np = self.simplenlg.nlgfactory.createNounPhrase(object)

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

                self.sentences.append(self.simplenlg.nlgfactory.createSentence(s))

    def getaction_activity(self, assertions, userpref):
        actions = []

        for a in assertions:
            if userpref == "The Foodie":
                action = a.getspecificparameter("Action")
            else:
                action = a.getspecificparameter("Activity")

            if action != None:
                actions.append(action)

        actions = [[ft, actions.count(ft)] for ft in set(actions)]
        actions.sort(key=lambda k: (k[0], -k[1]), reverse=True)
        # print(actions)

        return actions

    def sentimentphrase(self, assertions, userpref):

        self.sentences = []

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

            object = ""
            if userpref == "The Foodie":
                object = a.getspecificparameter("Food")
            elif userpref == "The Fangirl/Fanboy":
                object = a.getspecificparameter("FanOf")
            elif userpref == "The Sports Fanatic":
                object = a.getspecificparameter("Sport")
            elif userpref == "The Gamer":
                object = a.getspecificparameter("Game")

            print("Object", object)

            pp1 = self.simplenlg.nlgfactory.createPrepositionPhrase()
            pp1.addComplement(object)
            pp1.setPreposition("on")
            s.addComplement(pp1)

            s2 = self.simplenlg.nlgfactory.createClause()
            s2.setSubject(self.pronoun)
            s2.setVerb("say")
            s2.setObject("\"" + a.getspecificparameter("Sentiment") + "\"")
            s2.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
            s2.setFeature(self.simplenlg.Feature.COMPLEMENTISER, "since")
            s.addComplement(s2)

            self.sentences.append(self.simplenlg.nlgfactory.createSentence(s))

        return self.sentences

    def eventphrase(self, assertions, userpref, pronoun):
        self.pronoun = pronoun
        self.sentences = []

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

            self.sentences.append(self.simplenlg.nlgfactory.createSentence(s))

        return self.sentences