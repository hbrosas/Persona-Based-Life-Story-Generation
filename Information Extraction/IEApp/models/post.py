class Post(object):
	id = 0
	post = ""
	label = ""

	def __init__(self, id, post, label):
		self.id = id
		self.post = post
		self.label = label

	def getID(self):
		return self.id

	def getPost(self):
		return self.post

	def getLabel(self):
		return self.label

	def printDetails(self):
		print(self.id)
		print(self.post + " | " + self.label)