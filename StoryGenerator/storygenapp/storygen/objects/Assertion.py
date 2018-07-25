class Assertion:

    def __init__(self, assertion_type, parameterlist):
        self.assertion_type = assertion_type
        self.parameterlist = parameterlist

    def getspecificparameter(self, param_name):
        isFound = False
        value = ""

        for p in self.parameterlist:
            if p.name.lower() == param_name.lower() and p.value != "null":
                isFound = True
                value = p.value

        if isFound == True:
            return value
        else:
            return None

    def setspecificparam(self, param_name, param_value):
        for p in self.parameterlist:
            if p.name.lower() == param_name.lower():
                p.value = param_value

    def checkspecificparam(self, param_name, param_value):
        isContains = False
        for p in self.parameterlist:
            if p.name.lower() == param_name.lower() and param_value in p.value:
                isContains = True

        return isContains

    # def printassertion(self):
    #     print(self.assertion_type)
    #     print(self.parameterlist.)