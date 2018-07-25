from storygenappv2.storygen.controller.storygenoverview.OverviewObject import OverviewObject
from storygenappv2.storygen.controller.storygenoverview.StoryOverview import StoryOverview
from storygenappv2.storygen.controller.storyuserpreference.StoryFoodie import StoryFoodie
from storygenappv2.storygen.controller.storyuserpreference.StorySportsFanatic import StorySportsFanatic
from storygenappv2.storygen.controller.storyuserpreference.StoryFangirlFanboy import StoryFangirlFanboy
from storygenappv2.storygen.controller.storyuserpreference.StoryGamer import StoryGamer
from storygenappv2.storygen.controller.storyuserpreference.UserPreferenceObject import UserPreferenceObject
from storygenappv2.storygen.controller.storylikedpagesandevents.LikedPagesEventsObject import LikedPagesEventsObject
from storygenappv2.storygen.controller.storylikedpagesandevents.StoryLikedPagesAndEvents import StoryLikedPagesAndEvents
from storygenappv2.storygen.savetofile.FileWriter import FileWriter
# from flask import Flask, render_template

class Driver:
    def init(self):
        """
        initializes the objects needed for the story generation
        """
        self.overview = ""
        self.userpreferences = []
        self.userpref_story = []

        self.userpreferences.append("The Foodie")
        # self.userpreferences.append("The Sports Fanatic")
        self.userpreferences.append("The Fangirl/Fanboy")
        # self.userpreferences.append("The Gamer")

        self.run(Driver)
        # self.outputhtml()

    def run(self):
        """
        runs the story generator
        """
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

            if story is None:
                story = ""
                story += "\n" + storylikesevents.generatesummary(likeseventsobj, overviewobj.genderObj.pronoun, up)
            else:
                story += "\n" + storylikesevents.generatesummary(likeseventsobj, overviewobj.genderObj.pronoun, up)

            self.userpref_story.append(story)

        filewriter = FileWriter(self.overview, self.userpreferences, self.userpref_story)
        filewriter.save()