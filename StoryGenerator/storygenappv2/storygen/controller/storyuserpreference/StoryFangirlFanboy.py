from storygenappv2.storygen.SimpleNLG import SimpleNLG
from datetime import date
from datetime import datetime
import random


class StoryFangirlFanboy:

    def __init__(self):
        self.userpref = "The Fangirl/Fanboy"
        self.simplenlg = SimpleNLG()
        self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()

    def generateFangirlFanboy(self, fangirlobj, pronoun):
        """
        calls the methods needed to form the story for The Fangirl/Fanboy
        and realizes the elements into one paragraph.

        :param fangirlobj contains the different object needed by this method:
        :param pronoun contains the referring expression, prononun:
        :returns story a fangirl/fanboy paragraph containing the story for "The Fangirl/Fanboy":
        """

        self.pronoun = pronoun

        # get assertions with category
        categ_assertions = fangirlobj.getAssertionsWithCategory(self.userpref)

        # get level1 categories
        categories = fangirlobj.getCategoryOfAssertions('level1', categ_assertions)
        print(categories)

        artist_assertions = fangirlobj.getAssertionsByCategory(categ_assertions, 'artist', 'level1')

        for c in categories:
            # get assertions with specific category
            specific_assertions = fangirlobj.getAssertionsByCategory(categ_assertions, c[0], 'level1')

            if c[0] == 'books and literature':
                self.documentlist.append(self.introphrase(c[0]))

                genres = fangirlobj.getCategoryOfAssertions('level2', specific_assertions)
                for g in genres:
                    # intro phrase for the book genre
                    self.documentlist.append(self.genrephrase(c[0], g[0]))
                    # get specific books - parameter FanOF
                    book_assertions = fangirlobj.getAssertionsByCategory(specific_assertions, g[0], 'level2')

                    if len(book_assertions) != 0:
                        books = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', book_assertions)
                        book_list = [book[0] for book in books]
                        self.specific_fanphrase(c[0], book_assertions, book_list)
                    # "She already read <books>"

                # get artists related to books and literature
                bookartist_assertions = fangirlobj.getAssertionsByCategory(artist_assertions, 'author and writer', 'level2')
                specific_artists = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', bookartist_assertions)
                artist_list = [specific_artist[0] for specific_artist in specific_artists]
                if len(artist_list) != 0:
                    self.fanofphrase('book authors', bookartist_assertions, artist_list)

                # Getting all fandom assertions for each musical artist category
                fandom_assertions = fangirlobj.getAssertionsBySpecificType(bookartist_assertions, 'fandom')
                fandom_artists = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', fandom_assertions)

                # Getting the fandoms of each artist
                for fa in fandom_artists:
                    specific_assertions = fangirlobj.getAssertionBySpecificParamInAssertion('FanOf', fa[0], fandom_assertions)
                    fandoms = fangirlobj.getSpecificParamTypeWithAssertion('Fandom', specific_assertions)
                    fandom_list = [fandom[0] for fandom in fandoms]
                    if len(fandom_list) != 0:
                        self.documentlist.append(self.fandomphrase(fandom_list, fa[0]))

            elif c[0] == 'music':
                self.documentlist.append(self.introphrase(c[0]))

                genre_assertions = fangirlobj.getAssertionsByCategory(specific_assertions, 'music genres', 'level2')
                genres = fangirlobj.getCategoryOfAssertions('level3', genre_assertions)
                genre_list = [genre[0] for genre in genres]
                if len(genre_list) != 0:
                    self.documentlist.append(self.genrephrase(c[0], genre_list))
                songs = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', genre_assertions)
                song_list = [song[0] for song in songs]
                if len(song_list) != 0:
                    self.specific_fanphrase('music genres', genre_assertions, song_list)

                # get artists related to books and literature
                musicartist_assertions = fangirlobj.getAssertionsByCategory(artist_assertions, 'musical artist',
                                                                           'level2')
                specific_artists = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', musicartist_assertions)
                artist_list = [specific_artist[0] for specific_artist in specific_artists]
                if len(artist_list) != 0:
                    self.fanofphrase('musical artists', musicartist_assertions, artist_list)

                # Getting all fandom assertions for each musical artist category
                fandom_assertions = fangirlobj.getAssertionsBySpecificType(musicartist_assertions, 'fandom')
                fandom_artists = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', fandom_assertions)

                # Getting the fandoms of each artist
                for fa in fandom_artists:
                    specific_assertions = fangirlobj.getAssertionBySpecificParamInAssertion('FanOf', fa[0],
                                                                                            fandom_assertions)
                    fandoms = fangirlobj.getSpecificParamTypeWithAssertion('Fandom', specific_assertions)
                    fandom_list = [fandom[0] for fandom in fandoms]
                    if len(fandom_list) != 0:
                        self.documentlist.append(self.fandomphrase(fandom_list, fa[0]))

            elif c[0] == 'movies and tv':
                self.documentlist.append(self.introphrase(c[0]))

                genres = fangirlobj.getCategoryOfAssertions('level2', specific_assertions)
                for g in genres:
                    # intro phrase for the book genre
                    self.documentlist.append(self.genrephrase(c[0], g[0]))
                    # get specific books - parameter FanOF
                    movie_assertions = fangirlobj.getAssertionsByCategory(specific_assertions, g[0], 'level2')
                    movies = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', movie_assertions)
                    movie_list = [movie[0] for movie in movies]
                    if len(movie_list) != 0:
                        self.specific_fanphrase(c[0], movie_assertions, movie_list)

                # get artists related to books and literature
                movieartist_assertions = fangirlobj.getAssertionsByCategory(artist_assertions, 'movie and tv',
                                                                            'level2')
                specific_artists = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', movieartist_assertions)
                artist_list = [specific_artist[0] for specific_artist in specific_artists]
                if len(artist_list) != 0:
                    self.fanofphrase('actors', movieartist_assertions, artist_list)

                # Getting all fandom assertions for each musical artist category
                fandom_assertions = fangirlobj.getAssertionsBySpecificType(movieartist_assertions, 'fandom')
                fandom_artists = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', fandom_assertions)

                # Getting the fandoms of each artist
                for fa in fandom_artists:
                    specific_assertions = fangirlobj.getAssertionBySpecificParamInAssertion('FanOf', fa[0],
                                                                                                fandom_assertions)
                    fandoms = fangirlobj.getSpecificParamTypeWithAssertion('Fandom', specific_assertions)
                    fandom_list = [fandom[0] for fandom in fandoms]
                    if len(fandom_list) != 0:
                        self.documentlist.append(self.fandomphrase(fandom_list, fa[0]))

            elif c[0] == 'comics and animation':
                self.documentlist.append(self.introphrase(c[0]))

                genres = fangirlobj.getCategoryOfAssertions('level2', specific_assertions)
                for g in genres:
                    # get specific comics and animation - parameter FanOF
                    comics_assertions = fangirlobj.getAssertionsByCategory(specific_assertions, g[0], 'level2')
                    comics = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', comics_assertions)
                    comic_list = [comic[0] for comic in comics]
                    self.specific_fanphrase(c[0], comics_assertions, comic_list)

                # get artists related to books and literature
                comicartist_assertions = fangirlobj.getAssertionsByCategory(artist_assertions, 'comics and animation',
                                                                            'level2')
                specific_comicartists = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', comicartist_assertions)
                comicartist_list = [specific_comicartist[0] for specific_comicartist in specific_comicartists]
                if len(comicartist_list) != 0:
                    self.fanofphrase('comics creators', comicartist_assertions, comicartist_list)

                # Getting all fandom assertions for each musical artist category
                fandom_assertions = fangirlobj.getAssertionsBySpecificType(comicartist_assertions, 'fandom')
                fandom_artists = fangirlobj.getSpecificParamTypeWithAssertion('FanOf', fandom_assertions)

                # Getting the fandoms of each artist
                for fa in fandom_artists:
                    specific_assertions = fangirlobj.getAssertionBySpecificParamInAssertion('FanOf', fa[0],
                                                                                            fandom_assertions)
                    fandoms = fangirlobj.getSpecificParamTypeWithAssertion('Fandom', specific_assertions)
                    fandom_list = [fandom[0] for fandom in fandoms]
                    if len(fandom_list) != 0:
                        self.documentlist.append(self.fandomphrase(fandom_list, fa[0]))

        paragraph = self.simplenlg.nlgfactory.createParagraph(self.documentlist)

        story = self.simplenlg.realiser.realise(paragraph).getRealisation()
        print(story)

        return story

    def introphrase(self, category):
        """
        returns a DocumentElement with the sentence introductory about the user's fan of.

        :param category main category which the user is a fan of:
        :returns a sentence introductory about the category that the user is a fan of:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)

        if category == 'artist':
            object = self.simplenlg.nlgfactory.createNounPhrase("a", "fan")
            s.setObject(object)

            pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp.addComplement("different types of artists")
            pp.setPreposition("of")
            s.addModifier(pp)

        elif category == 'books and literature':
            s.setVerb("is")
            object = self.simplenlg.nlgfactory.createNounPhrase("a", "lover")
            object.addPreModifier("book")
            s.setObject(object)

        elif category == 'music':
            s.setVerb("is")
            object = self.simplenlg.nlgfactory.createNounPhrase("a", "fan")
            s.setObject(object)

            pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp.addComplement(category)
            pp.setPreposition("of")
            s.addModifier(pp)

        elif category == 'movies and tv':
            s.setVerb("is")
            object = self.simplenlg.nlgfactory.createNounPhrase("a", "fan")
            s.setObject(object)

            pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp.addComplement("movies and films")
            pp.setPreposition("of")
            s.addModifier(pp)

        elif category == 'comics and animation':
            s.setVerb("love")
            s.setObject("comics and anime")

        return self.simplenlg.nlgfactory.createSentence(s)

    def genrephrase(self, category, genre):
        """
        returns a DocumentElement with a summary sentence about the user's favorite genre on a specific category.
        
        :param category main category which the user is a fan of: 
        :param genre favorite genre category of the user: 
        :returns a summary sentence about the user's favorite genre:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("like")

        if category == 'books and literature':
            clause = self.simplenlg.nlgfactory.createClause()
            clause.setVerb("read")
            clause.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.INFINITIVE)
            clause.setObject(genre)
            s.setObject(clause)

        elif category == 'movies and tv':
            clause = self.simplenlg.nlgfactory.createClause()
            clause.setVerb("watch")
            clause.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.INFINITIVE)
            clause.setObject(genre)
            s.setObject(clause)

        elif category == 'music':
            clause = self.simplenlg.nlgfactory.createClause()
            clause.setVerb("listen")
            clause.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.INFINITIVE)

            c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

            for g in genre:
                c.addCoordinate(g)

            pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp.addComplement(c)
            pp.setPreposition("to")
            clause.setObject(pp)
            s.setObject(clause)


        return self.simplenlg.nlgfactory.createSentence(s)

    def fanofphrase(self, category, assertions, artists):
        """
        generates a DocumentElement with a summary sentence about the artists that the user supports on a specific category

        calls the describephrase method

        :param category type of artist:
        :param assertions contains the specific assertions about the artists:
        :param artists list of artists that the user supports:
        """

        cue_phrases = ['in fact', 'additionally', 'moreover', 'furthermore']
        verbs = ['admire', 'like', 'love', 'support']
        describe_assertions = []
        describe_artists = []

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb(random.choice(verbs))
        s.setObject(category)
        s.setFeature(self.simplenlg.Feature.CUE_PHRASE, random.choice(cue_phrases) + ",")

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for a in assertions:
            if a.getspecificparameter('Sentiment') != 'negative':
                artist = a.getspecificparameter('FanOf')
                if artist is not None and artist in artists:
                    artists.remove(artist)
                    c.addCoordinate(artist)
            elif a.getspecificparameter('Sentiment') == 'negative':
                artist = a.getspecificparameter('FanOf')
                artists.remove(artist)
            if a.assertion_type == 'describes':
                describe_artists.append(a.getspecificparameter('FanOf'))
                describe_assertions.append(a)
            # if a.assertion_type == 'fandom':
            #     fandom_artists.append(a.getspecificparameter('FanOf'))
            #     fandom_assertions.append(a)

        pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp.addComplement(c)
        pp.setPreposition("specifically")
        s.addModifier(pp)

        self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))
        # if len(fandom_assertions) != 0:
        #     self.fandomphrase(fandom_assertions, fandom_artists)
        if len(describe_assertions) != 0:
            self.describephrase(describe_assertions, describe_artists)

    def specific_fanphrase(self, category, assertions, objects):
        """
        generates a DocumentElement with a summary sentence about the objects that the user loves about a specific category

        :param category main category of the objects that the user is a fan of:
        :param assertions contains the specific assertions about the objects:
        :param objects list of objects that the user is a fan of:
        """
        describe_assertions = []
        ctrobject = 0
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        if len(objects) > 1:
            s.setPlural(True)

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()
        for a in assertions:
            if a.getspecificparameter('Sentiment') != 'negative':
                object = a.getspecificparameter('FanOf')
                if type(object) is list:
                    object = object[0]
                if object is not None and object in objects:
                    ctrobject+=1
                    c.addCoordinate(object)
                    objects.remove(object)
            elif a.getspecificparameter('Sentiment') == 'negative':
                object = a.getspecificparameter('FanOf')
                objects.remove(object)
            if a.assertion_type == 'describes':
                describe_assertions.append(a)

        if ctrobject != 0:

            if category == 'books and literature':
                s.setSubject(self.pronoun)
                s.setVerb("read")
                s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)
                s.addPreModifier("already")

            elif category == 'music genres':
                pronoun = self.simplenlg.nlgfactory.createWord(self.pronoun, self.simplenlg.LexicalCategory.PRONOUN)
                pronoun.setFeature(self.simplenlg.Feature.POSSESSIVE, True)
                s.setSubject("some")
                s.setVerb("is")
                np = self.simplenlg.nlgfactory.createNounPhrase(pronoun, "favorite music")
                pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                pp.addComplement(np)
                pp.setPreposition("of")
                s.addPreModifier(pp)

            elif category == 'movies and tv':
                pronoun = self.simplenlg.nlgfactory.createWord(self.pronoun, self.simplenlg.LexicalCategory.PRONOUN)
                pronoun.setFeature(self.simplenlg.Feature.POSSESSIVE, True)

                np = self.simplenlg.nlgfactory.createNounPhrase("favorites")
                np.setDeterminer(pronoun)
                s.setSubject(np)
                s.setVerb('is')

            elif category == 'comics and animation':
                s.setSubject(self.pronoun)
                s.setVerb("like")
                s.setPlural(False)


            s.setObject(c)

        self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))
        if len(describe_assertions) != 0:
            self.describephrase(describe_assertions, objects)

    def fandomphrase(self, fandoms, artist):
        """
        returns a DocumentElement with a summary sentence about the fandoms that the user joins for a specific artist

        :param fandoms list of fandom groups that the user joins:
        :param artist persona/group that the user is a fan of:
        :returns a summary sentence which includes listing of the fandoms that the user joins:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()
        s.setSubject(self.pronoun)
        s.setVerb('follow')
        s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "also,")

        np = self.simplenlg.nlgfactory.createNounPhrase("some fandoms")

        pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp1.addComplement(artist)
        pp1.setPreposition("of")
        np.addModifier(pp1)

        for f in fandoms:
            c.addCoordinate(f)

        pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp2.addComplement(c)
        pp2.setPreposition("like")
        np.addModifier(pp2)

        s.setObject(np)

        return self.simplenlg.nlgfactory.createSentence(s)

    def describephrase(self, assertions, artists):
        """
        generates a DocumentElement with a summary sentence of the user's descriptions
        about the specific artists that he/she is a fan of

        :param assertions contains the specific assertions that includes the user's description about the artists:
        :param artists list of artists that the user describes:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        artist_list = [[a, artists.count(a)] for a in set(artists)]
        artist_list.sort(key= lambda k: -k[1])
        artists = [artist[0] for artist in artists]

        for a in assertions:
            artist = a.getspecificparameter('FanOf')
            if artist is not None and artist in artists:
                s.setSubject(self.pronoun)
                s.setVerb("describe")
                s.setObject(artist)

                pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                pp.setPreposition("as")
                pp.addComplement(a.getspecificparameter(param_name="Description"))
                s.addModifier(pp)
                self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))

                artists.remove(artist)