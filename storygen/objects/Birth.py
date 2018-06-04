class Birth(object):
    def __init__(self, birthday, place):
        self.birthday = birthday
        self.place = place

    @property
    def birthday(self):
        return self.birthday

    @birthday.setter
    def birthday(self, birthday):
        self.birthday = birthday

    @property
    def place(self):
        return self.place

    @place.setter
    def place(self, place):
        self.place = place
