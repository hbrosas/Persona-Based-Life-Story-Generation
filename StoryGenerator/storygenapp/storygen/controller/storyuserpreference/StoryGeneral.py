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

            if userpref == "The Foodie":
                action_name = "Action"
            else:
                action_name = "Activity"

            action_assertions = UserPreferenceObject.getAssertionBySpecificParamInAssertion(self=UserPreferenceObject, param_name=action_name, param_value=action[0], assertions=assertions)

            if len(action_assertions) == 1:
                self.specificactivityphrase(action_assertions, userpref, action[0])

            else:

                s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
                s.setSubject(self.pronoun)
                s.setVerb(action[0])
                cpe = self.simplenlg.CoordinatedPhraseElement()


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

                    if actionparam is not None:

                        if actionparam in self.meals:
                            a.setspecificparam("Action", "eat")
                            a.setspecificparam("Food", actionparam)
                            s.setVerb("eat")

                        np = self.simplenlg.nlgfactory.createNounPhrase(object)


                        location = a.getspecificparameter("Location")
                        tagged_friends = a.getspecificparameter("Tagged_Friends")

                        if len(location) > 0 or len(tagged_friends) > 0:
                            specific_actassertions.append(a)

                        else:
                            if len(organization) > 0:
                                pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                                pp1.addComplement(organization[0])
                                pp1.setPreposition("in")
                                np.addModifier(pp1)

                        cpe.addCoordinate(np)

                s.setObject(cpe)

                self.sentences.append(self.simplenlg.nlgfactory.createSentence(s))
                self.specificactivityphrase(specific_actassertions, userpref, action[0])

        return self.sentences

    def specificactivityphrase(self, assertions, userpref, action):

        sorted_assertions = self.getassertionsbydate(assertions)

        for a in sorted_assertions:
            s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
            s.setSubject(self.pronoun)
            s.setVerb(action)
            s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
            if userpref == "The Foodie":
                actionparam = a.getspecificparameter("Action")
            else:
                actionparam = a.getspecificparameter("Activity")

            if actionparam is not None:

                object = ""
                organization = None

                if userpref == "The Foodie":

                    if actionparam in self.meals:
                        a.setspecificparam("Action", "eat")
                        a.setspecificparam("Food", actionparam)
                        s.setVerb("eat")

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
                date = a.getspecificparameter("Date")

                if len(organization) > 0:
                    pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                    pp1.addComplement(organization[0])
                    pp1.setPreposition("in")
                    np.addModifier(pp1)

                if len(location) > 0:
                    pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                    pp2.addComplement(location[0])
                    pp2.setPreposition("at")
                    np.addModifier(pp2)

                if len(tagged_friends) > 0:
                    # tagged_friends = [x.strip() for x in tagged_friends.split(',')]
                    taggedfriends_pp = self.simplenlg.nlgfactory.createCoordinatedPhrase()

                    for friend in tagged_friends:
                        friend_np = self.simplenlg.nlgfactory.createNounPhrase(friend)
                        taggedfriends_pp.addCoordinate(friend_np)

                    pp3 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                    pp3.addComplement(taggedfriends_pp)
                    pp3.setPreposition("with")
                    np.addModifier(pp3)

                if date is not None:
                    pp4 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                    pp4.addComplement(date)
                    pp4.setPreposition("last")
                    np.addModifier(pp4)

                s.setObject(np)

            self.sentences.append(self.simplenlg.nlgfactory.createSentence(s))


    def getassertionsbydate(self, assertions):
        dates = self.getdate_activity(assertions)
        sorted_assertions = []
        for d in dates:
            for a in assertions:
                date = a.getspecificparameter("Date")
                if date == d:
                    sorted_assertions.append(a)

        return sorted_assertions

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

    def getdate_activity(self, assertions):
        dates = []

        for a in assertions:
            date = a.getspecificparameter("Date")
            if date != None:
                dates.append(date)

        datesorted = sorted(dates, key=lambda d: datetime.strptime(d, '%B %d, %Y'))

        return datesorted

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

            # print("Object", object)

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

            location = a.getspecificparameter("Location")
            tagged_friends = a.getspecificparameter("Tagged_Friends")

            if len(location) > 0:
                pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                pp1.addComplement(location[0])
                pp1.setPreposition("at")
                s.addModifier(pp1)

            if len(tagged_friends) > 0:
                taggedfriends_pp = self.simplenlg.nlgfactory.createCoordinatedPhrase()

                for friend in tagged_friends:
                    friend_np = self.simplenlg.nlgfactory.createNounPhrase(friend)
                    taggedfriends_pp.addCoordinate(friend_np)

                pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                pp2.addComplement(taggedfriends_pp)
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