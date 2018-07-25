from storygenappv2.storygen.SimpleNLG import SimpleNLG
import random

class StoryFoodie:

    def __init__(self):
        self.simplenlg = SimpleNLG()
        self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()
        self.meals = ['breakfast', 'lunch', 'dinner', 'brunch', 'meal', 'snacks']
        self.userpref = "The Foodie"

    def generatefoodie(self, foodieobj, pronoun):
        """
        calls the methods needed to form the story for The Foodie
        and realizes the elements into one paragraph.

        :param fangirlobj contains the different object needed by this method:
        :param pronoun contains the referring expression, prononun:
        :returns story a foodie paragraph containing the story for "The Foodie":
        """
        self.pronoun = pronoun

        self.generatebycategory(foodieobj)

        # generate phrases for assertions with Location
        activity_assertions = foodieobj.getAssertionsByType("food_activity")
        places = foodieobj.getSpecificParamTypeWithAssertion('Location', activity_assertions)
        places_list = [place[0] for place in places]
        organizations = foodieobj.getSpecificParamTypeWithAssertion('Organization', activity_assertions)
        organization_list = [org[0] for org in organizations]
        list = places_list + organization_list

        placesvisited = [[ft, list.count(ft)] for ft in set(list)]
        placesvisited.sort(key=lambda k: -k[1])
        placesvisited_list = [place[0] for place in placesvisited]
        if len(placesvisited_list) != 0:
            self.documentlist.append(self.placevisitedphrase(placesvisited_list))

        # other assertions that are not in the category table

        paragraph = self.simplenlg.nlgfactory.createParagraph(self.documentlist)

        story = self.simplenlg.realiser.realise(paragraph).getRealisation()
        print(story)

        return story

    def generatebycategory(self, foodieobj):
        """
        calls the methods to generate and to form the story by category

        :param foodieobj contains the different object needed by this method:
        """

        # get assertions with category
        categ_assertions = foodieobj.getAssertionsWithCategory(self.userpref)

        # get level1 categories
        categories = foodieobj.getCategoryOfAssertions('level1', categ_assertions)
        print(categories)

        if len(categories) != 0:
            favorite_categ = categories[0]

        for c in categories:
            # get assertions with specific category
            assertions = foodieobj.getAssertionsByCategory(categ_assertions, c[0], 'level1')

            specific_assertions = foodieobj.removeSpecificAssertions('Sentiment_Class', 'negative', assertions)

            if c[0] == 'cuisines':
                # intro phrase for cuisine
                # 1. get all the different cuisines
                cuisines = foodieobj.getCategoryOfAssertions('level2', specific_assertions)
                # 2. pass to the intro phrase function
                self.documentlist.append(self.introphrase(c[0], cuisines))

                # 3. For each cuisine, get the assertions
                for cuisine in cuisines:
                    cuisine_assertions = foodieobj.getAssertionBySpecificParamInAssertion('Type', cuisine[0],
                                                                                          specific_assertions)
                    foods = foodieobj.getSpecificParamTypeWithAssertion('Food', cuisine_assertions)
                    food_list = [food[0] for food in foods]
                    if len(food_list) != 0:
                        self.cuisinephrase(cuisine[0], cuisine_assertions, food_list)

            elif c[0] == 'food':
                # 1. get all level 2 category of foods
                subfoods = foodieobj.getCategoryOfAssertions('level2', specific_assertions)
                self.documentlist.append(self.introphrase(c[0], []))
                # 2. get assertions by category
                self.food_ctr = 0
                for food in subfoods:
                    food_assertions = foodieobj.getAssertionsByCategory(specific_assertions, food[0], 'level2')
                    foods = foodieobj.getSpecificParamTypeWithAssertion('Food', food_assertions)
                    food_list = [food[0] for food in foods]
                    if len(food_list) != 0 and len(food_assertions) != 0:
                        self.food_ctr += 1
                        self.foodphrase(food[0], food_assertions, food_list)

            elif c[0] == 'desserts and baking':
                foods = foodieobj.getSpecificParamTypeWithAssertion('Food', specific_assertions)
                food_list = [food[0] for food in foods]
                if len(food_list) != 0:
                    self.dessertphrase(specific_assertions, food_list)

            elif c[0] == 'beverages':
                nonalcoholic_assertions = foodieobj.getAssertionsByCategory(specific_assertions,
                                                                            'non alcoholic beverages', 'level2')
                drinks = foodieobj.getSpecificParamTypeWithAssertion('Food', nonalcoholic_assertions)
                nonalcoholic_drinks = [drink[0] for drink in drinks]
                if len(nonalcoholic_drinks) != 0:
                    self.drinkphrase('non alcoholic beverages', nonalcoholic_assertions, nonalcoholic_drinks)

                alcoholic_assertions = foodieobj.getAssertionsByCategory(specific_assertions, 'alcoholic beverages',
                                                                         'level2')
                drinks = foodieobj.getSpecificParamTypeWithAssertion('Food', alcoholic_assertions)
                alcoholic_drinks = [drink[0] for drink in drinks]
                if len(alcoholic_drinks) != 0:
                    self.drinkphrase('alcoholic beverages', alcoholic_assertions, alcoholic_drinks)

            else:
                foods = foodieobj.getSpecificParamTypeWithAssertion('Food', specific_assertions)
                food_list = [food[0] for food in foods]
                if len(food_list) != 0 and len(specific_assertions) != 0:
                    self.foodphrase(c[0], specific_assertions, food_list)

    def introphrase(self, main_categ, categories):
        """
        returns a DocumentElement with the sentence introductory about
        the food categories that the user usually eats

        :param main_categ main category which the user likes:
        :param categories containing the subcategories:
        :returns a sentence introductory about the main food category that the user usually eats:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        if main_categ == 'cuisines' and len(categories) != 0:
            s.setSubject(self.pronoun)
            s.setVerb("enjoy")

            clause = self.simplenlg.nlgfactory.createClause()
            clause.setVerb("eat")
            clause.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.GERUND)
            clause.setObject("different " + main_categ)

            c = self.simplenlg.nlgfactory.createCoordinatedPhrase()
            for categ in categories:
                c.addCoordinate(categ[0])

            pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp.addComplement(c)
            pp.setPreposition("specifically")
            clause.addModifier(pp)

            s.setObject(clause)

        elif main_categ == 'food':
            s.setSubject(self.pronoun)
            s.setVerb("likes")

            clause = self.simplenlg.nlgfactory.createClause()
            clause.setVerb("eat")
            clause.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.INFINITIVE)
            clause.setObject("different types of " + main_categ)
            s.setObject(clause)

        return self.simplenlg.nlgfactory.createSentence(s)

    def cuisinephrase(self, cuisine, assertions, foods):
        """
        returns a DocumentElement with a summary sentence about the foods of a specific cuisine

        :param cuisine specific cuisine:
        :param assertions containing the specific cuisine as its category:
        :param foods list of foods that the user likes:
        :returns a summary sentence about the foods that the user likes which belong to the specified cuisine:
        """

        describe_assertions = []

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb('like')
        s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "for " + cuisine + ",")

        clause = self.simplenlg.nlgfactory.createClause()
        clause.setVerb("eat")
        clause.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.INFINITIVE)
        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for a in assertions:
            if a.getspecificparameter('Sentiment_Class') != 'negative':
                food = a.getspecificparameter('Food')
                if food is not None and food in foods:
                    foods.remove(food)
                    c.addCoordinate(food)
            if a.assertion_type == 'food_describe':
                describe_assertions.append(a)

        clause.setObject(c)
        s.setObject(clause)

        self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))
        if len(describe_assertions) != 0:
            self.describephrase(describe_assertions)

    def foodphrase(self, category, assertions, foods):
        """
        returns a DocumentElement with a summary sentence about the foods of a specific category that the user likes

        :param category specific category that the user likes:
        :param assertions containing the specific food as its category:
        :param foods list of foods that the user likes:
        :returns a summary sentence about the foods that the user likes which belong to the specified category:
        """

        describe_assertions = []
        cue_phrases = ['apart from that', 'besides that', 'additionally', 'other than that', 'also']
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb('enjoy')
        if self.food_ctr != 1:
            s.setFeature(self.simplenlg.Feature.CUE_PHRASE, random.choice(cue_phrases) + ",")

        clause = self.simplenlg.nlgfactory.createClause()
        clause.setVerb("eat")
        clause.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.GERUND)
        clause.setObject(category + " food")
        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for a in assertions:
            if a.getspecificparameter('Sentiment_Class') != 'negative':
                food = a.getspecificparameter('Food')
                if food is not None and food in foods:
                    foods.remove(food)
                    c.addCoordinate(food)
            if a.assertion_type == 'food_describe':
                describe_assertions.append(a)

        pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp.addComplement(c)
        pp.setPreposition("like")
        clause.addModifier(pp)
        s.setObject(clause)

        self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))
        if len(describe_assertions) != 0:
            self.describephrase(describe_assertions)

    def drinkphrase(self, category, assertions, drinks):
        """
        returns a DocumentElement with a summary sentence about the specific beverages that the user usually drinks based on the
        specific category

        :param category specific category of the beverages:
        :param assertions:
        :param drinks list of beverages that the user usually drinks:
        :returns a summary sentence about the beverages that the user usually drinks according to its category:
        """
        describe_assertions = []

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        clause = self.simplenlg.nlgfactory.createClause()
        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for a in assertions:
            if a.getspecificparameter('Sentiment_Class') != 'negative':
                drink = a.getspecificparameter('Food')
                if drink is not None and drink in drinks:
                    drinks.remove(drink)
                    c.addCoordinate(drink)
            if a.assertion_type == 'food_describe':
                describe_assertions.append(a)

        s.setSubject(self.pronoun)
        if category == 'non alcoholic beverages':
            s.setVerb('prefer')
            clause.setVerb("drink")
            clause.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.GERUND)
            clause.setObject(c)
            s.setObject(clause)
            s.setFeature(self.simplenlg.Feature.CUE_PHRASE, "for beverages,")

        elif category == 'alcoholic beverages':
            s.setVerb('drink')
            s.setPreModifier('also')
            s.setObject(category)

            pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp.addComplement(c)
            pp.setPreposition("like")
            s.addModifier(pp)

        self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))
        if len(describe_assertions) != 0:
            self.describephrase(describe_assertions)

    def dessertphrase(self, assertions, foods):
        """
        returns a DocumentElement with a summary sentence about the specific desserts that the user usually eats

        :param assertions containing "desserts and baking" as its category:
        :param foods list of desserts:
        :returns a summary sentence about the favorite desserts of the user:
        """

        describe_assertions = []
        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb('like')

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for a in assertions:
            if a.getspecificparameter('Sentiment_Class') != 'negative':
                food = a.getspecificparameter('Food')
                if food is not None and food in foods:
                    foods.remove(food)
                    c.addCoordinate(food)
            if a.assertion_type == 'food_describe':
                describe_assertions.append(a)

        s.setObject(c)
        s.setPostModifier("for dessert")

        self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))
        if len(describe_assertions) != 0:
            self.describephrase(describe_assertions)

    def placevisitedphrase(self, places):
        """
        returns a DocumentElement with a summary sentence about where did the user usually go for the food places

        :param places list of food places that the user went to:
        :returns a summary sentence about the food places that the user have visited:
        """

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("go")
        s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)

        pp1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp1.addComplement("food places")
        pp1.setPreposition("to")
        s.addModifier(pp1)

        c = self.simplenlg.nlgfactory.createCoordinatedPhrase()

        for place in places:
            c.addCoordinate(place)

        pp2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        pp2.addComplement(c)
        pp2.setPreposition("like")
        s.addModifier(pp2)

        return self.simplenlg.nlgfactory.createSentence(s)

    def describephrase(self, assertions):
        """
        returns a DocummentElement with a summary about the user's description about a specific food

        :param assertions containing those that the user have described a specific food:
        :returns a summary sentence about the food's description made by the user:
        """

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

        self.documentlist.append(self.simplenlg.nlgfactory.createSentence(s))
