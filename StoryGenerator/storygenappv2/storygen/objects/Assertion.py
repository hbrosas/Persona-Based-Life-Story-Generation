class Assertion:
    category = None

    def __init__(self, assertion_type, parameterlist):
        self.assertion_type = assertion_type
        self.parameterlist = parameterlist

    def getspecificparameter(self, param_name):
        """

        :param param_name:
        :returns the value of a specific parameter:
        """
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
        """
        sets the value of a specific parameter in the assertion

        :param param_name name of the parameter:
        :param param_value value of the parameter:
        """
        for p in self.parameterlist:
            if p.name.lower() == param_name.lower():
                p.value = param_value

    # def checkspecificparam(self, param_name, param_value):
    #     isContains = False
    #     for p in self.parameterlist:
    #         # if type(p.value) is list:
    #         #     p.value = p.value[0]
    #         if p.name.lower() == param_name.lower() and param_value in p.value:
    #             isContains = True
    #
    #     return isContains

    def containsspecificparam(self, param_name, param_value):
        """
        checks if the parameter list of the assertion contains a specific parameter-value pair

        :param param_name name of the parameter:
        :param param_value value of the parameter:
        :returns ifContains (True or False):
        """
        isContains = False
        for p in self.parameterlist:
            if type(p.value) is list:
                if p.name.lower() == param_name.lower() and any(param_value.lower() in v.lower() for v in p.value):
                    isContains = True
            elif type(p.value) is str:
                if p.name.lower() == param_name.lower() and param_value.lower() == p.value.lower():
                    isContains = True
            else:
                if p.name.lower() == param_name.lower() and param_value in p.value:
                    isContains = True

        return isContains

    def setcategory(self, category):
        """
        sets the category of an assertion

        :param category:
        """
        self.category = category

    def getspecificcategory(self, categ_level):
        """

        :param categ_level category level:
        :returns the specific category in a certain category level:
        """
        categ_label = ""
        if categ_level == 'level1':
            categ_label = self.category.level1
        elif categ_level == 'level2':
            categ_label = self.category.level2
        elif categ_level == 'level3':
            categ_label == self.category.level3

        return categ_label

    # def printassertion(self):
    #     print(self.assertion_type)
    #     print(self.parameterlist.)