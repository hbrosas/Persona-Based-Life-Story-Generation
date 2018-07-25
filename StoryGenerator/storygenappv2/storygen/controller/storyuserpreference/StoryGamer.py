from storygenappv2.storygen.SimpleNLG import SimpleNLG


class StoryGamer:

    def __init__(self):
        self.simplenlg = SimpleNLG()
        self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()
        self.userpref = "The Gamer"

    def generategamer(self, gamerobj, pronoun):
        """
        calls the methods needed to form the story for The Gamer
        and realizes the elements into one paragraph.

        :param gamerobj contains the different object needed by this method:
        :param pronoun contains the referring expression, prononun:
        :returns story a gamer paragraph containing the story for "The Gamer":
        """

        self.pronoun = pronoun

        play_assertions = gamerobj.getAssertionsByType("Play")
        activity_assertions = gamerobj.getAssertionsByType("Activity")

        gametypes = gamerobj.getSpecificParamTypeWithAssertion("Type", play_assertions)
        gametype_list = [gametype[0] for gametype in gametypes]
        print(gametypes)
        if len(gametype_list) != 0:
            self.documentlist.append(self.introphrase(gametype_list))

        for gt in gametype_list:
            # get all the games of specific game type
            specplay_assertions = gamerobj.getAssertionBySpecificParamInAssertion('Type', gt, play_assertions)
            games = gamerobj.getSpecificParamTypeWithAssertion('Game', specplay_assertions)
            game_list = [game[0] for game in games]
            # create intro phrase for the specific game type (play)
            self.documentlist.append(self.playphrase(game_list, gt))

            giveaway_assertions = []
            livestream_assertions = []

            for game in game_list:
                # get activity assertions for each game
                specific_assertions = gamerobj.getAssertionBySpecificParamInAssertion('Game', game, activity_assertions)
                # giveaway and livestream
                giveaway = gamerobj.getAssertionBySpecificParamInAssertion('Activity', 'giveaway', specific_assertions)
                if len(giveaway) != 0:
                    giveaway_assertions.append(giveaway[0])
                livestream = gamerobj.getAssertionBySpecificParamInAssertion('Activity', 'livestream', specific_assertions)
                if len(livestream) != 0:
                    livestream_assertions.append(livestream[0])

            if len(giveaway_assertions) != 0:
                self.documentlist.append(self.activityphrase(giveaway_assertions, 'giveaway', gt))
            if len(livestream_assertions) != 0:
                self.documentlist.append(self.activityphrase(livestream_assertions, 'livestream', gt))

        support_assertions = gamerobj.getAssertionsByType("Supports")
        countries = gamerobj.getSpecificParamTypeWithAssertion("Country", support_assertions)
        country_list = [country[0] for country in countries]
        if len(support_assertions) != 0:
            self.documentlist.append(self.teamphrase(support_assertions, country_list))

        # if len(country_list) != 0:
        #     self.documentlist.append(self.supportphrase(country_list))
        #
        # for country in country_list:
        #     team_assertions = gamerobj.getAssertionBySpecificParamInAssertion('Country', country, support_assertions)
        #     teams = gamerobj.getSpecificParamTypeWithAssertion("Team", team_assertions)
        #     team_list = [team[0] for team in teams]
        #     if len(team_list) != 0:
        #         self.documentlist.append(self.teamphrase(team_list, country))

        paragraph = self.simplenlg.nlgfactory.createParagraph(self.documentlist)

        story = self.simplenlg.realiser.realise(paragraph).getRealisation()
        print(story)

        return story

    def introphrase(self, gametypes):
        """
        returns a DocumentElement with the sentence introductory about the types of games that the user usually play

        :param gametypes main category of the games:
        :returns a sentence introductory about the types of games that the user usually play:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("is interested")

        pp1 = self.simplenlg.nlgfactory.createPrepositionPhrase()
        pp1.addComplement("different types of games")
        pp1.setPreposition("in")
        s.addModifier(pp1)

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()
        for gametype in gametypes:
            c.addCoordinate(gametype)

        pp2 = self.simplenlg.nlgfactory.createPrepositionPhrase()
        pp2.addComplement(c)
        pp2.setPreposition("such as")
        s.addModifier(pp2)

        return self.simplenlg.nlgfactory.createSentence(s)

    def playphrase(self, games, gametype):
        """
        returns a DocumentElement with a summary sentence about the specific games
        that the user usually play for a specific type of game

        :param games list of games that the user play:
        :param gametype type of game:
        :returns a summary sentence about the games that the user usually play for the given game type:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        if "game" not in gametype and "games" not in gametype:
            gametype += " games"
        s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "In " + gametype + ",")
        s.setSubject(self.pronoun)
        s.setVerb("play")

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()
        for game in games:
            c.addCoordinate(game)
        if len(games) != 0:
            s.addModifier(c)
    
        return self.simplenlg.nlgfactory.createSentence(s)

    def activityphrase(self, assertions, activity, gametype):
        """
        returns a DocumentElement with a summary sentence about the activities that the user
        do for a specific game type.

        :param assertions specifically activity assertions:
        :param activity specific activity that the user does:
        :param gametype:
        :returns a summmary sentence about the user's activities for a given type of game:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        ga = self.simplenlg.nlgfactory.createCoordinatedPhrase()
        ls = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for a in assertions:
            # check activity
            game = a.getspecificparameter("Game")
            if activity == 'giveaway':
                ga.addCoordinate(game)
            elif activity == 'livestream':
                ls.addCoordinate(game)

        if activity == 'livestream':
            s.setSubject(self.pronoun)
            # s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "In fact,")
            s.setVerb("watch")
            s.setPreModifier("usually")
            s.setObject(activity)

            pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp1.addComplement(gametype)
            pp1.setPreposition("of")
            s.addModifier("pp1")

            pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp2.addComplement(ls)
            pp2.setPreposition("specifically")
            s.addModifier(pp2)
        elif activity == 'giveaway':
            s.setSubject(self.pronoun)
            # s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "Other than that,")
            s.setVerb("join")
            s.setPreModifier("also")
            s.setObject(activity)

            pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp2.addComplement(ga)
            pp2.setPreposition("in")
            s.addModifier(pp2)

        return self.simplenlg.nlgfactory.createSentence(s)

    # def supportphrase(self, countries):
    #     """
    #     returns a DocumentElement with a summary sentence about the countries that the user supports
    #     when it comes to games
    #
    #     :param countries list of countries that the user supports for a game:
    #     :returns a summary sentence about the countries that the user suppports for a specific game:
    #     """
    #
    #     s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
    #     s.setSubject(self.pronoun)
    #     s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "As a gamer,")
    #     s.setVerb("supports")
    #     s.setObject("different teams")
    #
    #     c = self.simplenlg.nlgfactory.createCoordinatedPhrase()
    #     for country in countries:
    #         c.addCoordinate(country)
    #
    #     pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
    #     pp.addComplement(c)
    #     pp.setPreposition("from")
    #     s.addModifier(pp)
    #
    #     return self.simplenlg.nlgfactory.createSentence(s)

    def teamphrase(self, assertions, countries):
        """
        returns a DocumentElement with a summary sentence about the teams per country
        that the user supports in general

        :param assertions that contains the 'Support' assertions:
        :param countries:
        :returns a summary sentence about the teams that the user supports for each country:
        """
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "As a gamer,")
        s.setSubject(self.pronoun)
        s.setVerb("supports")

        list = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for country in countries:
            c = self.simplenlg.nlgfactory.createCoordinatedPhrase()
            for a in assertions:
                if a.containsspecificparam('Country', country):
                    team = a.getspecificparameter('Team')
                    c.addCoordinate(team)
            clause = self.simplenlg.nlgfactory.createClause()
            clause.setObject(c)

            pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp.addComplement(country)
            pp.setPreposition("from")
            clause.addModifier(pp)

            list.addCoordinate(clause)

        s.addModifier(list)

        return self.simplenlg.nlgfactory.createSentence(s)