from storygenappv2.storygen.SimpleNLG import SimpleNLG


class StoryLikedPagesAndEvents:

    def __init__(self):
        self.simplenlg = SimpleNLG()
        self.likes_documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()
        self.events_documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()

    def generatesummary(self, likeseventsobj, pronoun, user_pref):
        """
        calls the methods needed to form the paragraph for Liked Pages and Events
        and realizes the elements into one paragraph.

        :param likeseventsobj LikedPagesEventsObject containing the objects needed by this method:
        :param pronoun contains the referring expression, prononun:
        :param user_pref user preference of the user:
        :returns story contains a paragraph of the user's liked pages and events:
        """
        self.pronoun = pronoun

        likes_assertions = likeseventsobj.getSpecificAssertions("likes", user_pref)
        if len(likes_assertions) != 0:
            self.likes_documentlist.append(self.likesphrase(likes_assertions))

        likes_paragraph = self.simplenlg.nlgfactory.createParagraph(self.likes_documentlist)

        likes_story = self.simplenlg.realiser.realise(likes_paragraph).getRealisation()
        print(likes_story)

        events_assertions = likeseventsobj.getSpecificAssertions("events", user_pref)
        interested_assertions = likeseventsobj.getAssertionsBySpecificParam("RSVP", "unsure", events_assertions)
        if len(interested_assertions) != 0:
            self.events_documentlist.append(self.interested_eventsphrase(interested_assertions))

        attended_assertions = likeseventsobj.getAssertionsBySpecificParam("RSVP", "attending", events_assertions)
        if len(attended_assertions) != 0:
            self.events_documentlist.append(self.attended_eventsphrase(attended_assertions))

        events_paragraph = self.simplenlg.nlgfactory.createParagraph(self.events_documentlist)

        events_story = self.simplenlg.realiser.realise(events_paragraph).getRealisation()
        print(events_story)

        story = likes_story + "\n" + events_story

        return story

    def likesphrase(self, likes_assertions):
        """
        returns a DocumentElement with the gathered information of the user's liked pages
        on a specific user preference

        includes listing the name of the liked pages in the given assertions

        :param likes_assertions assertions containing all the liked pages of the user:
        :returns DocumentElement extension of NLG comprises of the paragraph listing the names of the liked pages in each assertion:
        """
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("like")

        object = self.simplenlg.nlgfactory.createNounPhrase("page")
        object.setPlural(True)
        s.setObject(object)

        cpe = self.simplenlg.CoordinatedPhraseElement()

        if len(likes_assertions) > 15:
            likes_assertions = likes_assertions[:15]

        for la in likes_assertions:
            np = self.simplenlg.nlgfactory.createNounPhrase(la.getspecificparameter("PAGE"))
            cpe.addCoordinate(np)

        pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp.addComplement(cpe)
        pp.setPreposition("such as")
        s.addModifier(pp)

        return self.simplenlg.nlgfactory.createSentence(s)

    def interested_eventsphrase(self, events_assertions):
        """
        returns a DocumentElement with the gathered information of the events that the user is interested in

        includes listing the name of the events that the user

        :param events_assertions assertions containing all the events that the user is interested in:
        :returns DocumentElement extension of NLG comprises of the paragraph listing the names of the events in each assertion:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("is")

        ap = self.simplenlg.nlgfactory.createAdjectivePhrase("interested")
        s.setObject(ap)

        pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp1.addComplement("events")
        pp1.setPreposition("in")
        s.addModifier(pp1)

        cpe = self.simplenlg.CoordinatedPhraseElement()

        if len(events_assertions) > 10:
            events_assertions = events_assertions[:10]

        for ea in events_assertions:
            np = self.simplenlg.nlgfactory.createNounPhrase(ea.getspecificparameter("EVENT"))
            cpe.addCoordinate(np)

        pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp2.addComplement(cpe)
        pp2.setPreposition("such as")
        s.addModifier(pp2)

        return self.simplenlg.nlgfactory.createSentence(s)

    def attended_eventsphrase(self, events_assertions):
        """
        returns a DocumentElement with the gathered information of the attended events of the user

        includes listing the name of the attended events that the user

        :param events_assertions assertions containing all the attended events of the user:
        :returns DocumentElement extension of NLG comprises of the paragraph listing the names of the events in each assertion:
        """
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("attend")
        s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
        s.setObject("events")

        cpe = self.simplenlg.CoordinatedPhraseElement()

        if len(events_assertions) > 10:
            events_assertions = events_assertions[:10]

        for ea in events_assertions:
            np = self.simplenlg.nlgfactory.createNounPhrase(ea.getspecificparameter("EVENT"))
            cpe.addCoordinate(np)

        pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp.addComplement(cpe)
        pp.setPreposition("such as")
        s.addModifier(pp)

        return self.simplenlg.nlgfactory.createSentence(s)
