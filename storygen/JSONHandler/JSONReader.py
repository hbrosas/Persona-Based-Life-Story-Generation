from models.AssertionModel import AssertionModel
import json

class JSONReader:
    assertions = []
    am = AssertionModel

    def readjson(self, filename):
        f = open(filename, "r")
        if f.mode == "r":
            f1 = f.readlines()
            for json in f1:
                self.assertions.append(json)
                print(json)

        self.storejson()

    def storejson(self):
        self.am.createAssertionTable(self=self.am)
        # self.am.createAssertionTypesTable(self=self.am)
        for a in self.assertions:
            assertion = json.loads(a)
            # user_pref = assertion["user_pref"]
            user_pref = "The Foodie"
            assertion_type = assertion["type"]
            parameters = assertion["values"]
            print(user_pref)
            print(assertion_type)
            print(parameters)

            # Store to db
            self.am.addAssertion(self=self.am, user_pref=user_pref, assertion_type=assertion_type, parameters=str(parameters[0]))

if __name__ == "__main__":
    JSONReader().readjson("C:/Users/denis_000/PycharmProjects/storygen/JSONReceiver/sample_foodie.txt")
