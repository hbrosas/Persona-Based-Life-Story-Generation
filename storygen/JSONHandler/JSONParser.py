from objects.AssertionParameters import AssertionParameters
import json

class JSONParser:

    def getParsedParameters(self, parameters, assertionparameter):
        try:
            paramObj = json.loads(parameters)
            self.paramlist = []

            for ap in assertionparameter:
                if paramObj[ap] is not None and paramObj[ap] != "":
                    parameter = AssertionParameters(ap, paramObj[ap])
                    self.paramlist.append(parameter)
                    #print(parameter.name + " " + parameter.value)

        except ValueError:
            # print("Error loading JSON!")
            print("")

        return self.paramlist
