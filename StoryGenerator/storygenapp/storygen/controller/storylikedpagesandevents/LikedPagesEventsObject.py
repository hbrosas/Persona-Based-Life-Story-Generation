from storygenapp.storygen.models.AssertionModel import AssertionModel
from storygenapp.storygen.objects.Assertion import Assertion
from storygenapp.storygen.JSONHandler.JSONParser import JSONParser


class LikedPagesEventsObject:

    def __init__(self):
        self.am = AssertionModel
        self.assertionObj = []
        self.userpref_type = []

    def initializeAsseertions(self, user_pref):

        likedpagesevents = self.am.getLikedPagesAndEvents(self=self.am)

        if likedpagesevents is not None:
            for lpe in likedpagesevents:
                assertiontype = self.am.getAssertionType(self=self.am, assertiontype=lpe.type)
                nameparams = self.getParametersList(assertiontype.parameters)
                parameterlist = JSONParser.getParsedParameters(self=JSONParser, parameters=lpe.parameters, assertionparameter=nameparams)

                assertion = Assertion(assertion_type=assertiontype.type, parameterlist=parameterlist)
                self.assertionObj.append(assertion)

    def getParametersList(self, parameters):
        #Comma splice
        paramList = parameters.split(", ")

        return paramList

    def getSpecificAssertions(self, type, user_pref):
        assertions = []

        for a in self.assertionObj:
            if a.checkspecificparam("User_Pref", user_pref) and a.assertion_type == type:
                assertions.append(a)

        return assertions

    def getAssertionsBySpecificParam(self, param_name, param_value, assertions):
        specific_assertions = []

        for a in assertions:
            if a.checkspecificparam(param_name, param_value):
                specific_assertions.append(a)

        return specific_assertions