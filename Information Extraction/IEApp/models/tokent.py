# Object for Token/Entity

class Tokent(object):
	token = ""
	posTag = ""
	entity = ""

	def __init__(self, token, posTag, entity):
		self.token = token
		self.posTag = posTag
		self.entity = entity

	def printDetails(self):
		print(self.token + " | " + self.posTag + " | " + self.entity)