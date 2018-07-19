class Post(object):
	id = 0
	fbID = ""
	original_post = ""
	label = ""
	date = ""
	time = ""
	person = []
	hashtags = []
	mentions = []
	story = ""
	post = ""
	sentiment = ""

	def __init__(self, id, fbID, post, label, date, time):
		self.id = id
		self.fbID = fbID
		self.original_post = post
		self.label = label
		self.date = date
		self.time = time

	def printDetails(self):
		print(self.id)
		print(self.post + " | " + self.label)