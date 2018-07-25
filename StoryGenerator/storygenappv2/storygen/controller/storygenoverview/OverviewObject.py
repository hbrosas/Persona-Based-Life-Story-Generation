from storygenappv2.storygen.objects.Person import Person
from storygenappv2.storygen.objects.Birth import Birth
from storygenappv2.storygen.objects.LivingIn import LivingIn
from storygenappv2.storygen.objects.Gender import Gender
from storygenappv2.storygen.models.ProfileModel import ProfileModel

class OverviewObject:
    personObj = Person
    birthObj = Birth
    genderObj = Gender
    livinginObj = LivingIn


    def __init__(self):
        self.workObj = []
        self.educationObj = []
        self.pm = ProfileModel
        # self.wem = WorkEducationModel
        self.initializeobject()

    def initializeobject(self):
        """
        initializes all the objects
        """
        self.initializePerson()
        self.initializeBirthday()
        self.initializeGender()
        self.initializeLivingIn()
        # self.initializeEducation()
        # self.initializeWork()

    def initializePerson(self):
        """
        initializes the name of the person
        """
        name = self.pm.getspecificdirectknowledge(self=self.pm,type="name")

        if name is not None and name != "":
            self.personObj.name = name
            # print(self.personObj.name)

    def initializeBirthday(self):
        """
        initializes the birth date of the user
        """
        bday = self.pm.getspecificdirectknowledge(self=self.pm, type="birthday")

        if bday is not None and bday != "":
            self.birthObj.birthday = bday
            # print(self.birthObj.birthday)

    def initializeGender(self):
        """
        initializes the gender of the user
        """
        gender = self.pm.getspecificdirectknowledge(self=self.pm, type="gender")

        if gender is not None and gender != "":
            self.genderObj.gender = gender
            # print(self.genderObj.gender)

            if gender.lower() == "Female".lower():
                self.genderObj.pronoun = "she"
            elif gender.lower() == "Male".lower():
                self.genderObj.pronoun = "he"

            # print(self.genderObj.pronoun)

    def initializeLivingIn(self):
        """
        initializes the location, hometown and current living of the user
        """
        address = self.pm.getspecificdirectknowledge(self=self.pm, type="address")
        location = self.pm.getspecificdirectknowledge(self=self.pm, type="location")
        hometown = self.pm.getspecificdirectknowledge(self=self.pm, type="hometown")

        if address is not None and address != "":
            self.livinginObj.address = address
            # print(self.livinginObj.address)

        if location is not None and location != "":
            self.livinginObj.location = location
            # print(self.livinginObj.location)

        if hometown is not None and hometown != "":
            self.livinginObj.hometown = hometown
            # print(self.livinginObj.hometown)