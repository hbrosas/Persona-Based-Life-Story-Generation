from storygenappv2.storygen.models.AssertionModel import AssertionModel
from storygenappv2.storygen.objects.Assertion import Assertion
from storygenappv2.storygen.JSONHandler.JSONParser import JSONParser


class LikedPagesEventsObject:

    def __init__(self):
        self.am = AssertionModel
        self.assertionObj = []
        self.userpref_type = []

    def initializeAsseertions(self, user_pref):
        """
        initializes all the assertions for the liked pages and events of the user based on his/her user preference

        :param user_pref UserPreference object containing the user preference of user and the list of assertions:
        """
        likedpagesevents = self.am.getLikedPagesAndEvents(self=self.am)

        if likedpagesevents is not None:
            for lpe in likedpagesevents:
                if lpe.type == 'likes':
                    userpref = 'Likes'
                elif lpe.type == 'events':
                    userpref = 'Events'
                assertiontype = self.am.getAssertionType(self=self.am, assertiontype=lpe.type, user_pref=userpref)
                nameparams = self.getParametersList(assertiontype.parameters)
                parameterlist = JSONParser.getParsedParameters(self=JSONParser, parameters=lpe.parameters, assertionparameter=nameparams)

                assertion = Assertion(assertion_type=assertiontype.type, parameterlist=parameterlist)
                self.assertionObj.append(assertion)

    def getSpecificAssertions(self, type, user_pref):
        """
        returns the specific assertions based on the user preference of the user and the assertion type

        :param type assertion type of the assertions to be returned:
        :param user_pref user preference of the user:
        :return assertions:
        """
        assertions = []

        for a in self.assertionObj:
            if a.containsspecificparam("PERSONA", user_pref) and a.assertion_type == type:
                assertions.append(a)

        return assertions

    def getAssertionsBySpecificParam(self, param_name, param_value, assertions):
        """
        returns list of specific assertions based on the specific parameter-value pair requirement
        given a list of assertions

        :param param_name name of the parameter:
        :param param_value value of the parameter:
        :param assertions:
        :return specific assertions that have the parameter-value pair:
        """
        specific_assertions = []

        for a in assertions:
            if a.containsspecificparam(param_name, param_value):
                specific_assertions.append(a)

        return specific_assertions