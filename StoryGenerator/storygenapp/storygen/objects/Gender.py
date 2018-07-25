class Gender(object):

    def __init__(self, gender, pronoun):
        self.gender = gender
        self.pronoun = pronoun

    @property
    def gender(self):
        return self.gender

    @gender.setter
    def gender(self, gender):
        self.gender = gender

    @property
    def pronoun(self):
        return self.pronoun

    @pronoun.setter
    def pronoun(self, pronoun):
        self.pronoun = pronoun
