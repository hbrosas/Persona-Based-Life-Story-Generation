#from objects import Person, Birth, Work, LivingIn, Gender, Education
from objects.Education import Education
from objects.Work import Work
from objects.Person import Person
from objects.Birth import Birth
from objects.LivingIn import LivingIn
from objects.Gender import Gender
from models.ProfileModel import ProfileModel
from models.WorkEducationModel import WorkEducationModel

class OverviewObject:
    personObj = Person
    birthObj = Birth
    genderObj = Gender
    livinginObj = LivingIn
    workObj = []
    educationObj = []

    def __init__(self):
        self.pm = ProfileModel
        self.wem = WorkEducationModel
        self.initializeobject()

    def initializeobject(self):
        self.initializePerson()
        self.initializeBirthday()
        self.initializeGender()
        self.initializeLivingIn()
        self.initializeEducation()
        self.initializeWork()

    def initializePerson(self):
        name = self.pm.getspecificdirectknowledge(self=self.pm,type="name")

        if name is not None and name != "":
            self.personObj.name = name
            # print(self.personObj.name)

    def initializeBirthday(self):
        bday = self.pm.getspecificdirectknowledge(self=self.pm, type="birthday")

        if bday is not None and bday != "":
            self.birthObj.birthday = bday
            # print(self.birthObj.birthday)

    def initializeGender(self):
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

    def initializeWork(self):
        worklist = self.wem.getSpecificWork(self=self.pm)

        if worklist is not None:
            for w in worklist:
                work = Work(company=w.organization, startdate=w.yearstarted, enddate=w.yearended, position=w.courseorposition)
                # print(str(work.company) + " " + str(work.startdate) + " " + str(work.enddate) + " " + str(work.position))
                self.workObj.append(work)

    def initializeEducation(self):
        educationlist = self.wem.getSpecificEducation(self=self.pm)

        if educationlist is not None:
            for e in educationlist:
                education = Education(school=e.organization, yeargraduated=e.yearended, type=e.type, course=e.courseorposition)
                self.educationObj.append(education)

        # for ed in self.educationObj:
        #     print(str(ed.school) + " " + str(ed.yeargraduated) + " " + str(ed.type) + " " + str(ed.course))

