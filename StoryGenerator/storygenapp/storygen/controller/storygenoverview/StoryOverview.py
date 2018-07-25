from storygenapp.storygen.SimpleNLG import SimpleNLG
from datetime import date
from datetime import datetime

class StoryOverview:

    def __init__(self):
        self.simplenlg = SimpleNLG()
        self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()

    def generateoverview(self, overviewobject):
        self.pronoun = overviewobject.genderObj.pronoun

        self.documentlist.append(self.agephrase(overviewobject.birthObj, overviewobject.personObj.name))
        self.documentlist.append(self.birthphrase(overviewobject.birthObj))
        self.documentlist.append(self.locationphrase(overviewobject.livinginObj))
        self.documentlist.append(self.hometownphrase(overviewobject.livinginObj))
        self.documentlist.append(self.educationphrase(overviewobject.educationObj))
        self.documentlist.append(self.workphrase(overviewobject.workObj))

        paragraph = self.simplenlg.nlgfactory.createParagraph(self.documentlist)

        story = self.simplenlg.realiser.realise(paragraph).getRealisation()
        print(story)

        return story

    """This method returns a DocumentElement with the information of the user's age
        :param birth object containing the birthday of the user
         and name object containing the full name of the user
         :return sentence with the user's age information"""
    def agephrase(self, birth, name):
        birthday = birth.birthday
        age = self.getage(birthday)
        # print("age " + str(age))

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        s.setSubject(name)
        s.setVerb("is")
        s.setObject(str(age) + " years old")

        return self.simplenlg.nlgfactory.createSentence(s)

    def getage(self, birthday):
        bday = datetime.strptime(birthday, '%m/%d/%Y').date()
        today = date.today()
        return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))

    """This method returns a DocumentElement with the information of the user's birthdate
        :param birth object containing the birthday of the user
        :return sentence with the user's age information"""
    def birthphrase(self, birth):
        birthday = birth.birthday

        birthdayformat = datetime.strptime(birthday, '%m/%d/%Y').date()
        birthday = birthdayformat.strftime("%B %d %Y")
        # print(birthday)

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
        s.setSubject(self.pronoun)
        s.setVerb("is")
        s.setObject("born")

        p = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
        p.setPreposition("on")
        p.addComplement(birthday)
        s.addModifier(p)

        return self.simplenlg.nlgfactory.createSentence(s)

    def locationphrase(self, livingin):

        if livingin.location is not None or livingin.address is not None:

            if livingin.address is not None and livingin.address != "":
                location = livingin.address
            elif livingin.location is not None and livingin.location != "":
                location = livingin.location

            # print("location ", location)

            s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
            s.setSubject(self.pronoun)

            # adds adverb
            adv = self.simplenlg.nlgfactory.createAdverbPhrase("currently")

            # setting the verb phrase in the sentence
            verb = self.simplenlg.nlgfactory.createVerbPhrase("live")
            verb.addPreModifier(adv)
            s.setVerbPhrase(verb)
            # s.setFeature(self.Feature.FORM, self.Form.GERUND)

            # adding the prepositional phrase containing the living in - location
            pp = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
            pp.setPreposition("in")
            pp.addComplement(location)
            s.addModifier(pp)

            return self.simplenlg.nlgfactory.createSentence(s)
        else:
            return None

    def hometownphrase(self, livingin):
        if livingin.hometown is not None and livingin.hometown != "" and livingin.hometown != livingin.location:

            pronoun = self.simplenlg.nlgfactory.createWord(self.pronoun, self.simplenlg.LexicalCategory.PRONOUN)

            pronoun.setFeature(self.simplenlg.Feature.POSSESSIVE, True)
            hometown = livingin.hometown

            np = self.simplenlg.nlgfactory.createNounPhrase(pronoun, "hometown")

            s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)
            s.setSubject(np)
            s.setVerb("is")
            s.setObject(hometown)

            return self.simplenlg.nlgfactory.createSentence(s)
        else:
            return None

    def educationphrase(self, educationalbackground):
        if len(educationalbackground) != 0:
            pn = self.simplenlg.nlgfactory.createNounPhrase(self.pronoun)

            educationcp = self.simplenlg.nlgfactory.createCoordinatedPhrase()

            for eb in educationalbackground:
                s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

                school = eb.school
                course = eb.course
                yeargraduated = eb.yeargraduated

                s.setVerb("study")

                # "He studies <course>"
                if course is not None and course != "":
                    s.setObject(course)

                # "He studies at <school>"
                if school is not None and school != "":
                    p1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                    p1.addComplement(school)
                    p1.setPreposition("at")
                    s.addModifier(p1)

                yearnow = int(date.today().year)

                if yeargraduated is not None and yeargraduated != "":
                    p2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                    p2.addComplement(yeargraduated)
                    p2.setPreposition("last")
                    s.addModifier(p2)

                    # "He studied last <yeargraduated>"
                    if int(yeargraduated) <= yearnow:
                        s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)

                    # "He is studying"
                    else:
                        s.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.GERUND)

                elif yeargraduated is None and yeargraduated == "":
                    s.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.GERUND)

                educationcp.addCoordinate(s)

            pn.addPostModifier(educationcp)
            return self.simplenlg.nlgfactory.createSentence(pn)

        else:
            return None

    def workphrase(self, works):
        if len(works) != 0:
            pn = self.simplenlg.nlgfactory.createNounPhrase(self.pronoun)

            workcp = self.simplenlg.nlgfactory.createCoordinatedPhrase()

            for w in works:
                s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

                company = w.company
                startdate = w.startdate
                enddate = w.enddate
                position = w.position
                if startdate != "0000-00" and startdate != "0000-00-00" and startdate != '':
                    startdateformat = datetime.strptime(startdate, '%Y-%m-%d').date()
                    startdate = startdateformat.strftime("%B %Y")
                # print(startdate)

                if enddate != "0000-00" and enddate != "0000-00-00" and enddate != '':
                    enddateformat = datetime.strptime(enddate, '%Y-%m-%d').date()
                    enddate = enddateformat.strftime("%B %Y")
                # print(enddate)

                s.setVerb("work")

                # "He works as <position>"
                if position is not None and position != "":
                    p1 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                    p1.addComplement(position)
                    p1.setPreposition("as")
                    s.addModifier(p1)

                # "He works at <company>"
                if company is not None and company != "":
                    p2 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                    p2.addComplement(company)
                    p2.setPreposition("at")
                    s.addModifier(p2)

                # # "He works in <location>"
                # if location is not None and location != "":
                #     p3 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                #     p3.addComplement(location)
                #     p3.setPreposition("in")
                #     s.addModifier(p3)

                # "He works since <startdate>"
                if startdate != '' and startdate != "" and startdate != "0000-00" and startdate != "0000-00-00":
                    p4 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                    p4.addComplement(startdate)
                    p4.setPreposition("since")
                    s.addModifier(p4)

                # "He worked until <enddate>"
                if enddate != '' and enddate != "" and enddate != "0000-00" and enddate != "0000-00-00":
                    p5 = self.simplenlg.PPPhraseSpec(self.simplenlg.nlgfactory)
                    p5.addComplement(enddate)
                    p5.setPreposition("until")
                    s.addModifier(p5)
                    s.setFeature(self.simplenlg.Feature.TENSE, self.simplenlg.Tense.PAST)

                # "He is working"
                else:
                    s.addFrontModifier("is")
                    s.setFeature(self.simplenlg.Feature.FORM, self.simplenlg.Form.GERUND)

                workcp.addCoordinate(s)

            pn.addPostModifier(workcp)
            return self.simplenlg.nlgfactory.createSentence(pn)

        else:
            return None
