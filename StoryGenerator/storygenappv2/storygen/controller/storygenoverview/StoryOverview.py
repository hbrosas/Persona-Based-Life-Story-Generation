from storygenappv2.storygen.SimpleNLG import SimpleNLG
from datetime import date
from datetime import datetime

class StoryOverview:

    def __init__(self):
        self.simplenlg = SimpleNLG()
        self.documentlist = self.simplenlg.gateway.jvm.java.util.ArrayList()

    def generateoverview(self, overviewobject):
        """
        calls the methods needed to form the Overview and realizes the elements into one paragraph

        :param overviewobject contains different objects needed by this method:
        :returns story an overview paragraph containing the basic information about the user:
        """
        self.pronoun = overviewobject.genderObj.pronoun

        self.documentlist.append(self.agephrase(overviewobject.birthObj, overviewobject.personObj.name))
        self.documentlist.append(self.birthphrase(overviewobject.birthObj))
        self.documentlist.append(self.locationphrase(overviewobject.livinginObj))
        self.documentlist.append(self.hometownphrase(overviewobject.livinginObj))

        paragraph = self.simplenlg.nlgfactory.createParagraph(self.documentlist)

        story = self.simplenlg.realiser.realise(paragraph).getRealisation()
        print(story)

        return story

    def agephrase(self, birth, name):
        """
        returns a DocumentElement with the information of the user's age

        :param birth Birth object containing the birth date of the user:
        :param name whole name of the user:
        :returns DocumentElement extension of NLG comprises of a sentence with the user's age:
        """

        birthday = birth.birthday
        age = self.getage(birthday)

        s = self.simplenlg.SPhraseSpec(self.simplenlg.nlgfactory)

        s.setSubject(name)
        s.setVerb("is")
        s.setObject(str(age) + " years old")

        return self.simplenlg.nlgfactory.createSentence(s)

    def getage(self, birthday):
        """
        computes the user's age

        :param birthday birth date of the user in Date format:
        :returns current age of the user:
        """
        bday = datetime.strptime(birthday, '%m/%d/%Y').date()
        today = date.today()
        return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))

    def birthphrase(self, birth):
        """
        returns a DocumentElement with the information of the user's birth date

        :param birth Birth object containing the birth date of the user:
        :returns DocumentElement extension of NLG comprises of a sentence with the user's birth information:
        """
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
        """
        returns a DocumentElement with the information of the user's location

        :param livingin LivingIn object containing the location and address where the user lives:
        :returns DocumentElement extension of NLG comprises of a sentence with the user's location:
        """
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
        """
        returns a DocumentElement with the information of the user's hometown

        :param livingin LivingIn object containing the the hometown of the user:
        :returns DocumentElement extension of NLG comprises of a sentence with the user's hometown:
        """
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

