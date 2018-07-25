from storygenapp.storygen.models.AssertionModel import AssertionModel
from storygenapp.storygen.objects.Assertion import Assertion
from storygenapp.storygen.JSONHandler.JSONParser import JSONParser


class UserPreferenceObject:

    def __init__(self):
        self.am = AssertionModel
        self.assertionObj = []
        self.userpref_type = []

    def initializeAssertions(self, user_pref):

        directassertion = self.am.getAssertionByUserPreference(self=self.am, user_pref=user_pref)

        if directassertion is not None:
            for da in directassertion:
                assertiontype = self.am.getAssertionType(self=self.am, assertiontype=da.assertion_type)
                nameparams = self.getParametersList(assertiontype.parameters)
                # print(da.parameters)
                parameterlist = JSONParser.getParsedParameters(self=JSONParser, parameters=da.parameters, assertionparameter=nameparams)

                assertion = Assertion(assertion_type=assertiontype.type, parameterlist=parameterlist)
                self.assertionObj.append(assertion)


    # Converting the name of parameters String to parameters List
    def getParametersList(self, parameters):
        #Comma splice
        paramList = parameters.split(", ")

        return paramList

    # Returns the parameter values of a specic parameter name
    def getSpecificParamType(self, param_name):
        alltypes = []

        for a in self.assertionObj:
            type = a.getspecificparameter(param_name)

            if type != None:
                alltypes.append(type[0])

        self.userpref_type = [[ft, alltypes.count(ft)] for ft in set(alltypes)]
        self.userpref_type.sort(key=lambda k: -k[1])
        # print(self.userpref_type)

        return self.userpref_type

    # Returns the parameter values of a specic parameter name in a set of assertions
    def getSpecificParamTypeWithAssertion(self, param_name, assertions):
        alltypes = []

        for a in assertions:
            type = a.getspecificparameter(param_name)

            if type != None:
                alltypes.append(type)

        self.userpref_type = [[ft, alltypes.count(ft)] for ft in set(alltypes)]
        self.userpref_type.sort(key=lambda k: -k[1])
        # print(self.userpref_type)

        return self.userpref_type

    # Getting the list[Assertion] with food_type = parameter: foodtype_value
    def getAssertionsBySpecificParam(self, param_name, param_value):
        assertions = []

        for a in self.assertionObj:
            if a.checkspecificparam(param_name, param_value):
                assertions.append(a)

        return assertions

    # Getting the list[Assertion] with food_type = None
    def getAssertionsNoType(self, param_name):
        assertions = []

        for a in self.assertionObj:
            if a.getspecificparameter(param_name) is None:
                assertions.append(a)

        return assertions

    # Getting the list[Assertion] having assertion_type = parameter: assertiontype in parameter: assertions
    def getAssertionsByType(self, assertions, assertiontype):
        typeassertions = []

        for a in assertions:
            if a.assertion_type == assertiontype:
                typeassertions.append(a)

        return typeassertions

    # Returns the assertions which contains the specific param name that matches the given value
    def getAssertionBySpecificParamInAssertion(self, param_name, param_value, assertions):
        specific_assertions = []

        for a in assertions:
            if a.checkspecificparam(param_name, param_value):
                specific_assertions.append(a)

        return specific_assertions