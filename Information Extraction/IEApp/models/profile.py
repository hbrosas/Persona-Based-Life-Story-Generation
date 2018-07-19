class Profile(object):
	fbid = ""
	name = ""
	gender = ""
	birthday = ""
	address = ""
	location = ""
	hometown = ""
	about = ""
	friends = ""
	tablename = ""

	def __init__(self, fbID, name, gender, birthday, address, location, hometown, about, friends, tablename):
		self.fbID = fbID
		self.name = name
		self.gender = gender
		self.birthday = birthday
		self.address = address
		self.location = location
		self.hometown = hometown
		self.about = about
		self.friends = friends
		self.tablename = tablename