from storygenappv2.storygen.objects.AssertionParameters import AssertionParameters
import json

class JSONParser:

    def getParsedParameters(self, parameters, assertionparameter):
        """

        :param parameters parameters in JSON format:
        :param assertionparameter AssertionParameter object:
        :returns the list of parameters:
        """

        paramObj = json.loads(parameters)
        self.paramlist = []

        for ap in assertionparameter:
            if paramObj[ap] is not None and paramObj[ap] != "":
                parameter = AssertionParameters(ap, paramObj[ap])
                self.paramlist.append(parameter)
                # print(parameter.name + " " + parameter.value)

        return self.paramlist
