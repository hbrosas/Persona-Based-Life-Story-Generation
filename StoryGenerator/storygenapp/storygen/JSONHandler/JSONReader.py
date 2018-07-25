from storygenapp.storygen.models.AssertionModel import AssertionModel
import json


class JSONReader:

    def readjson(self, filename):
        f = open(filename, "r")
        if f.mode == "r":
            contents = f.read()
            contents = '{ "assertions": [' + contents
            if contents.endswith(","):
                contents = contents[:-1] + "]}"
            else:
                contents += "]}"
            # print(contents)
            self.assertions = json.loads(contents)
            print(self.assertions)

        # self.storejson()

        return self.assertions

    def storejson(self):
        for a in self.assertions['assertions']:
            assertion_type = a['type']
            user_pref = a['persona']
            parameters = a['values']




# if __name__ == "__main__":
#     JSONReader().readjson("C://Users//denis_000//PycharmProjects//StoryGenerator//assertions_foodie_demo.txt")
