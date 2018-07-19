class AssertionType(object):
	persona = ""
	assType = ""
	values = None
	post = None

	def __init__(self, id, fbID, post, label, timestamp):
		self.id = id
		self.fbID = fbID
		self.post = post
		self.label = label
		self.timestamp = timestamp

	def getID(self):
		return self.id

	def getPost(self):
		return self.post

	def getLabel(self):
		return self.label

	def printDetails(self):
		print(self.id)
		print(self.post + " | " + self.label)