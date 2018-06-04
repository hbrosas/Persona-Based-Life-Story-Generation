from controller.storygenoverview.OverviewObject import OverviewObject
from controller.storygenoverview.StoryOverview import StoryOverview
from controller.storyuserpreference.StoryFoodie import StoryFoodie
from controller.storyuserpreference.StorySportsFanatic import StorySportsFanatic
from controller.storyuserpreference.StoryFangirlFanboy import StoryFangirlFanboy
from controller.storyuserpreference.StoryGamer import StoryGamer
from controller.storyuserpreference.UserPreferenceObject import UserPreferenceObject
from controller.storylikedpagesandevents.LikedPagesEventsObject import LikedPagesEventsObject
from controller.storylikedpagesandevents.StoryLikedPagesAndEvents import StoryLikedPagesAndEvents
from savetofile.FileWriter import FileWriter
from flask import Flask, render_template

class Driver:

    def init(self):
        self.overview = ""
        self.userpreferences = []
        self.userpref_story = []

        self.userpreferences.append("The Foodie")
        self.userpreferences.append("The Sports Fanatic")
        self.userpreferences.append("The Fangirl/Fanboy")
        self.userpreferences.append("The Gamer")

        self.run()
        # self.outputhtml()

    def run(self):
        overviewobj = OverviewObject()
        storyoverview = StoryOverview()
        self.overview = storyoverview.generateoverview(overviewobj)

        for up in self.userpreferences:

            if up == "The Foodie":
                foodieobj = UserPreferenceObject()
                foodieobj.initializeAssertions("The Foodie")
                storyfoodie = StoryFoodie()
                story = storyfoodie.generatefoodie(foodieobj, overviewobj.genderObj.pronoun)

            elif up == "The Sports Fanatic":
                sportsfanaticobj = UserPreferenceObject()
                sportsfanaticobj.initializeAssertions("The Sports Fanatic")
                storysportsfanatic = StorySportsFanatic()
                story = storysportsfanatic.generatesportsfanatic(sportsfanaticobj, overviewobj.genderObj.pronoun)

            elif up == "The Fangirl/Fanboy":
                fangirlobj = UserPreferenceObject()
                fangirlobj.initializeAssertions("The Fangirl/Fanboy")
                storyfangirlfanboy = StoryFangirlFanboy()
                story = storyfangirlfanboy.generateFangirlFanboy(fangirlobj, overviewobj.genderObj.pronoun)

            elif up == "The Gamer":
                gamerobj = UserPreferenceObject()
                gamerobj.initializeAssertions("The Gamer")
                storygamer = StoryGamer()
                story = storygamer.generategamer(gamerobj, overviewobj.genderObj.pronoun)

            likeseventsobj = LikedPagesEventsObject()
            likeseventsobj.initializeAsseertions(up)
            storylikesevents = StoryLikedPagesAndEvents()
            story += "\n" + storylikesevents.generatesummary(likeseventsobj, overviewobj.genderObj.pronoun, up)

            self.userpref_story.append(story)

        filewriter = FileWriter(self.overview, self.userpreferences, self.userpref_story)
        filewriter.save()

    # def outputhtml(self):
    #     self.userpref_dict = {}
    #     for u in range(len(self.userpreferences)):
    #         userpref = self.userpreferences[u]
    #         story = self.userpref_story[u]
    #         self.userpref_dict[userpref] = story
    #
    #     print(self.userpref_dict)

# def loadtohtml():
#     overview = Driver.overview
#     userpref_dict = Driver.userpref_dict
#     return render_template('profile.html', **locals())

# def create_app(overview, userpref_dict, debug):
#     app = Flask(__name__)
#     app.debug = debug
#     app.overview = overview
#     app.userpref_dict = userpref_dict
#
#     render_template('profile.html', **locals())
#
#     return app


if __name__ == '__main__':
    driver = Driver()
    driver.init()
    # app = create_app(driver.overview, driver.userpref_dict, True)
    # app.run()



