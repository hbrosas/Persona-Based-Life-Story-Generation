from storygenappv2.storygen.SimpleNLG import SimpleNLG
import random

class StorySportsFanatic:
    userpref = "The Sports Fanatic"

    def __init__(self):
        self.simplenlg = SimpleNLG()
        self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()

    def generatesportsfanatic(self, sportsfanaticobj, pronoun):
        """
        calls the methods needed to form the story for The Sports Fanatic
        and realizes the elements into one paragraph.

        :param sportsfanaticobj contains the different object needed by this method:
        :param pronoun contains the referring expression, prononun:
        :returns story a sports fanatic paragraph containing the story for "The Sports Fanatic":
        """

        self.pronoun = pronoun

        sports = sportsfanaticobj.getSpecificParamType("sport")
        sport_list = [sport[0] for sport in sports]
        print(sports)

        other_sports = []

        if len(sport_list) > 5:
            other_sports = sport_list[5:]
            sport_list = sport_list[:5]

        # get fave sport with the most number of assertions
        # self.favesport = sport_list[0]
        # self.documentlist.append(self.favesportphrase(self.favesport))

        for sport in sport_list:
            sport_assertion = sportsfanaticobj.getAssertionsBySpecificParam("Sport", sport)

            play_assertions = sportsfanaticobj.getAssertionsBySpecificType(sport_assertion, "play")
            if len(play_assertions) != 0:
                self.documentlist.append(self.introphrase(sport))
            else:
                self.documentlist.append(self.sportphrase(sport))

            # for each sport, get all Supports and FanOf assertions
            supports_assertions = sportsfanaticobj.getAssertionsBySpecificType(sport_assertion, "supports")
            fanof_assertions = sportsfanaticobj.getAssertionsBySpecificType(sport_assertion, "fanof")

            # "In basketball, he supports teams and ahtletes like ...."
            if len(supports_assertions) != 0 or len(fanof_assertions) != 0:
                self.documentlist.append(self.fanphrase(fanof_assertions, supports_assertions, sport))

            # "He also supports <sport> leagues specifically.."
            league_assertions = sportsfanaticobj.getAssertionsBySpecificType(sport_assertion, "league")
            leagues = sportsfanaticobj.getSpecificParamTypeWithAssertion('League', league_assertions)
            league_list = [league[0] for league in leagues]
            if len(league_list) != 0:
                self.documentlist.append(self.leaguephrase(league_list, sport))

            # "He usually talks about ... <shared_about subject> "
            shared_assertions = sportsfanaticobj.getAssertionsBySpecificType(sport_assertion, "shared_about")
            # topics = sportsfanaticobj.getSpecificParamTypeWithAssertion('Subject', shared_assertions)
            topics = []
            if len(shared_assertions) != 0:
                for sa in shared_assertions:
                    subject = sa.getspecificparameter('Subject')
                    frequency = sa.getspecificparameter('Frequency')
                    topic = [subject, frequency]
                    topics.append(topic)

                topics.sort(key=lambda k: -k[1])
                topic_list = [topic[0] for topic in topics]
                self.documentlist.append(self.sharedaboutphrase(topic_list, sport))

        if len(other_sports) != 0:
            self.documentlist.append(self.othersphrase(other_sports))

        paragraph = self.simplenlg.nlgfactory.createParagraph(self.documentlist)

        story = self.simplenlg.realiser.realise(paragraph).getRealisation()
        print(story)

        return story

    def introphrase(self, sport):
        """
        returns a DocumentElement with a sentence introductory about the specific sports that the user likes to play

        :param sport:
        :returns a sentence introductory about the sports that the user plays:
        """
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("like")

        clause = self.simplenlg.nlgfactory.createClause()
        clause.setVerb("play")
        clause.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.INFINITIVE)
        clause.setObject(sport)
        s.setObject(clause)

        return self.simplenlg.nlgfactory.createSentence(s)

    def sportphrase(self, sport):
        """
        returns a DocumentElement with a summary sentence about the specific sports that the user is interested in

        :param sport:
        :returns a summary sentence about the sports that the user is interested in:
        """
        cue_phrases = ['other than that', 'also', 'apart from that', 'additionally']
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("is interested")
        s.setFeature(self.simplenlg.Feature.CUE_PHRASE, random.choice(cue_phrases) + ",")

        pp = self.simplenlg.nlgfactory.createPrepositionPhrase()
        pp.addComplement(sport)
        pp.setPreposition("in")
        s.addModifier(pp)

        return self.simplenlg.nlgfactory.createSentence(s)

    # def favesportphrase(self, sport):
    #     s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
    #     s.setSubject(self.pronoun)
    #     s.setVerb("love")
    #     s.setObject(sport)
    #     s.addPostModifier("more")
    #
    #     return self.simplenlg.nlgfactory.createSentence(s)

    def othersphrase(self, sports):
        """
        returns a DocumentElement with a summary sentence about the other sports that the user is interested in

        :param sports list of sports:
        :returns a summary sentence about other sports the user is interested in:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("is also interested")
        s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "lastly,")

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for sport in sports:
            c.addCoordinate(sport)

        pp1 = self.simplenlg.nlgfactory.createPrepositionPhrase()
        pp1.addComplement("other sports")
        pp1.setPreposition("in")
        s.addModifier(pp1)

        pp2 = self.simplenlg.nlgfactory.createPrepositionPhrase()
        pp2.addComplement(c)
        pp2.setPreposition("like")
        s.addModifier(pp2)

        return self.simplenlg.nlgfactory.createSentence(s)

    def fanphrase(self, athlete_assertions, team_assertions, sport):
        """
        returns a DocumentElement with a summary sentence about the sports team and athletes that the user is supporting

        :param athlete_assertions assertions containing the specific atheletes that the user is a fan of:
        :param team_assertions assertions containing the specific teams that the user is a fan of:
        :param sport:
        :returns a summary sentence about the teams and athletes that the user support:
        """

        s1 = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s2 = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        if len(athlete_assertions) != 0:

            s1.setSubject(self.pronoun)
            s1.setVerb("is")

            np1 = self.simplenlg.nlgfactory.createNounPhrase("a", "fan")
            s1.setObject(np1)

            c1 = self.simplenlg.nlgfactory.createCoordinatedPhrase()

            for a in athlete_assertions:
                player = a.getspecificparameter("Athlete")
                c1.addCoordinate(player)

            pp = self.simplenlg.nlgfactory.createPrepositionPhrase()
            pp.addComplement(c1)
            pp.setPreposition("of")
            s1.addModifier(pp)

        if len(team_assertions) != 0:

            s2.setSubject(self.pronoun)
            s2.setVerb("support")

            np2 = self.simplenlg.nlgfactory.createNounPhrase(sport, "teams")
            s2.setObject(np2)

            c2 = self.simplenlg.nlgfactory.createCoordinatedPhrase()

            for a in team_assertions:
                player = a.getspecificparameter("Team")
                c2.addCoordinate(player)

            pp = self.simplenlg.nlgfactory.createPrepositionPhrase()
            pp.addComplement(c2)
            pp.setPreposition("like")
            s2.addModifier(pp)

        if len(team_assertions) != 0 and len(athlete_assertions) != 0:
            s = self.simplenlg.nlgfactory.createCoordinatedPhrase(s1, s2)
        elif len(team_assertions) == 0 and len(athlete_assertions) != 0:
            s = s1
        elif len(team_assertions) != 0 and len(athlete_assertions) == 0:
            s = s2

        s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "in fact,")

        return self.simplenlg.nlgfactory.createSentence(s)

    def leaguephrase(self, leagues, sport):
        """
        returns a DocumentElement with a summary sentence about the sport leagues that the user is following

        :param leagues list of sport leagues:
        :param sport:
        :returns a summary sentence about the sport leagues that the user follow:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        verb = self.simplenlg.nlgfactory.createVerbPhrase("is even updated")
        s.setVerb(verb)
        s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)

        np = self.simplenlg.nlgfactory.createNounPhrase(sport, "leagues")
        pp1 = self.simplenlg.nlgfactory.createPrepositionPhrase()
        pp1.addComplement(np)
        pp1.setPreposition("on")
        s.setObject(pp1)
        s.setSubject(self.pronoun)
        # s.setFeature(self.simplenlg.Feature.MODAL, "is")
        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for league in leagues:
            c.addCoordinate(league)

        pp2 = self.simplenlg.nlgfactory.createPrepositionPhrase()
        pp2.addComplement(c)
        pp2.setPreposition("specifically")
        s.addModifier(pp2)

        return self.simplenlg.nlgfactory.createSentence(s)

    def sharedaboutphrase(self, topics, sport):
        """
        returns a DocumentElement with a summary sentence about the topics that the user shared about

        :param topics list of topics about a specific sports:
        :param sport:
        :returns a summary sentence about the topics of a specific sport:
        """
        s1 = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s1.setSubject(self.pronoun)
        s1.setVerb("share")
        s1.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)

        pp = self.simplenlg.nlgfactory.createPrepositionPhrase()
        pp.addComplement(sport)
        pp.setPreposition("about")
        s1.addModifier(pp)

        s2 = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s2.setSubject(self.pronoun)
        s2.setVerb("talks")
        s2.addPreModifier("usually")

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        if len(topics) > 5:
            for t in range(0, 5):
                c.addCoordinate(topics[t])
        else:
            for topic in topics:
                c.addCoordinate(topic)

        pp = self.simplenlg.nlgfactory.createPrepositionPhrase()
        pp.addComplement(c)
        pp.setPreposition("about")
        s2.addModifier(pp)

        s = self.simplenlg.nlgfactory.createCoordinatedPhrase(s1, s2)
        s.setConjunction("where")

        return self.simplenlg.nlgfactory.createSentence(s)
