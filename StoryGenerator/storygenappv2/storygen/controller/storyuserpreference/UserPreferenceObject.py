from storygenappv2.storygen.models.AssertionModel import AssertionModel
from storygenappv2.storygen.objects.Assertion import Assertion
from storygenappv2.storygen.JSONHandler.JSONParser import JSONParser
from storygenappv2.storygen.objects.Category import Category
from storygenappv2.storygen.models.CategoryModel import CategoryModel


class UserPreferenceObject:

    def __init__(self):
        self.am = AssertionModel
        self.cm = CategoryModel
        self.assertionObj = []
        self.userpref_type = []
        self.categories = []

    def initializeAssertions(self, user_pref):
        """
        initializes the all the assertions related to the user preference of the user

        :param user_pref user preference:
        """
        directassertion = self.am.getAssertionByUserPreference(self=self.am, user_pref=user_pref)

        if directassertion is not None:
            for da in directassertion:
                assertiontype = self.am.getAssertionType(self=self.am, assertiontype=da.assertion_type, user_pref=user_pref)
                nameparams = self.getParametersList(assertiontype.parameters)
                # print(da.parameters)
                parameterlist = JSONParser.getParsedParameters(self=JSONParser, parameters=da.parameters, assertionparameter=nameparams)

                assertion = Assertion(assertion_type=assertiontype.type, parameterlist=parameterlist)
                self.assertionObj.append(assertion)


    # Converting the name of parameters String to parameters List
    def getParametersList(self, parameters):
        """
        converts and returns the name of the parameters from thegiven String format to list format

        :param parameters:
        :returns list of all parameter names:
        """
        #Comma splice
        paramList = parameters.split(", ")

        return paramList

    # Returns the parameter values of a specific parameter name
    def getSpecificParamType(self, param_name):
        """
        returns the parameter values of a given parameter name in all assertions of the user preference
        of the user

        :param param_name parameter name:
        :return list of values for a parameter name in all assertions:
        """

        alltypes = []

        for a in self.assertionObj:
            param_value = a.getspecificparameter(param_name)

            if param_value != None:
                if type(param_value) is list:
                    alltypes.append(param_value[0].lower())
                else:
                    alltypes.append(param_value.lower())

        self.userpref_type = [[ft, alltypes.count(ft)] for ft in set(alltypes)]
        self.userpref_type.sort(key=lambda k: -k[1])
        # print(self.userpref_type)

        return self.userpref_type

    # Returns the parameter values of a specific parameter name in a set of assertions
    def getSpecificParamTypeWithAssertion(self, param_name, assertions):
        """
        returns the parameter values of a given parameter name in a set of assertions

        :param param_name name of the parameter:
        :param assertions:
        :returns list of parameter values:
        """

        alltypes = []

        for a in assertions:
            param_value = a.getspecificparameter(param_name)

            if param_value != None and param_value != []:
                # print("TYPE ", type)
                if param_name == 'Location' or param_name == 'Organization':
                    alltypes.append(param_value[0])
                else:
                    if type(param_value) is list:
                        alltypes.append(param_value[0])
                    else:
                        alltypes.append(param_value)


        self.userpref_type = [[ft, alltypes.count(ft)] for ft in set(alltypes)]
        self.userpref_type.sort(key=lambda k: -k[1])
        # print(self.userpref_type)

        return self.userpref_type

    # Getting the list[Assertion] with food_type = parameter: foodtype_value
    def getAssertionsBySpecificParam(self, param_name, param_value):
        """
        return assertions given a specific paramater-value pair requirement

        :param param_name name of the parameter:
        :param param_value expected value of the parameter:
        :returns list of assertions containing all the assertions that have the parameter-value pair requirement:
        """
        assertions = []

        for a in self.assertionObj:
            if a.containsspecificparam(param_name, param_value):
                assertions.append(a)

        return assertions

    # Getting the list[Assertion] with food_type = None
    # def getAssertionsNoType(self, param_name):
    #     assertions = []
    #
    #     for a in self.assertionObj:
    #         if a.getspecificparameter(param_name) is None:
    #             assertions.append(a)
    #
    #     return assertions

    # Getting the list[Assertion] having assertion_type = parameter: assertiontype in parameter: assertions
    def getAssertionsByType(self, assertiontype):
        """
        returns the assertions that belongs to the user's specified assertion type

        :param assertiontype :
        :returns list of assertions containing those that have the specified assertion type:
        """

        typeassertions = []

        for a in self.assertionObj:
            if a.assertion_type == assertiontype:
                typeassertions.append(a)

        return typeassertions

    def getAssertionsBySpecificType(self, assertions, assertiontype):
        """
        returns the assertions that belongs to the given assertion type on a specific list of assertions

        :param assertions:
        :param assertiontype:
        :returns the list of assertions that belongs to the given assertion type:
        """
        typeassertions = []
        for a in assertions:
            if a.assertion_type == assertiontype:
                typeassertions.append(a)

        return typeassertions

    # Returns the assertions which contains the specific param name that matches the given value
    def getAssertionBySpecificParamInAssertion(self, param_name, param_value, assertions):
        """
        returns the assertions that contains the given parameter-value pair requirements on a specific list of assertions

        :param param_name name of the parameter:
        :param param_value value of the parameter:
        :param assertions:
        :returns list of assertions containing all that satisfy the parameter-value pair requirement:
        """

        specific_assertions = []
        if type(param_value) is list:
            param_value = param_value[0]
        for a in assertions:
            if a.containsspecificparam(param_name, param_value):
                specific_assertions.append(a)

        return specific_assertions

    # Get categories by user_pref
    # def getCategoriesUserPref(self, user_pref):
    #     self.categories = self.cm.getCategoryByUserPref(user_pref)
    #
    #     return self.categories

    def getAssertionsWithCategory(self, user_pref):
        """
        returns the assertions of a given user preference of the user that contains a category

        :param user_pref user preferences:
        :returns list of assertions containing all that belongs to the user preference:
        """
        categ_assertions = []
        type = ''

        for a in self.assertionObj:
            if user_pref == 'The Foodie' or user_pref == 'The Fangirl/Fanboy':
                type = a.getspecificparameter("Type")
            if type is not None:
                for t in type:
                    result = self.cm.checkIfContainsCategory(self=self.cm, pref_type=t, user_pref=user_pref)
                    isContain = result[0]
                    category = result[1]
                    if isContain:
                        a.setspecificparam("Type", t)
                        a.setcategory(category)
                        categ_assertions.append(a)
                        # print(a.assertion_type, a.getspecificparameter("Type"))
                        break

        return categ_assertions

    def getCategoryOfAssertions(self, categ_level, assertions):
        """
        returns all the categories found in the assertions given a specific category level

        :param categ_level category level:
        :param assertions:
        :returns list of categories that are found in the assertions:
        """
        categories = []

        for a in assertions:
            category = a.getspecificcategory(categ_level)
            # sentiment = a.getspecificparameter('Sentiment_Class')
            # if category != None and category != '' and sentiment != 'negative':
            if category != None and category != '':
                categories.append(category)

        categories = [[c, categories.count(c)] for c in set(categories)]
        categories.sort(key=lambda k: -k[1])

        return categories

    def getAssertionsByCategory(self, assertions, category, categ_level):
        """
        returns the asssertions of a category in the specific list of assertions given the category and its level

        :param assertions:
        :param category:
        :param categ_level:
        :returns list of assertions containing all the assertions of a specific category:
        """

        categ_assertions = []

        for a in assertions:
            categ = a.getspecificcategory(categ_level)
            if category == categ:
                categ_assertions.append(a)

        return categ_assertions

    def removeSpecificAssertions(self, param_name, param_value, assertions):
        """
        returns the updated list of assertions after removing specific assertions based on their parameter-value pairs

        :param param_name name of the parameter:
        :param param_value value of the parameter:
        :param assertions:
        :returns list of assertions excluding the specific assertions to be removed:
        """
        dislikefoods = []
        specific_assertions = []
        for a in assertions:
            food = a.getspecificparameter('Food')
            if a.containsspecificparam(param_name, param_value):
                dislikefoods.append(food)

        for a in assertions:
            food = a.getspecificparameter('Food')
            if food not in dislikefoods:
                # assertions.remove(a)
                specific_assertions.append(a)

        return specific_assertions
