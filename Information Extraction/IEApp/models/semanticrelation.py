class SemanticRelation(object):
	id = 0
	relationid = 0
	term1 = ""
	term2 = ""

	def __init__(self, id, relationid, term1, term2):
		self.id = id
		self.relationid = relationid
		self.term1 = term1
		self.term2 = term2

	def getID(self):
		return self.id

	def getRelationId(self):
		return self.relationid

	def getTerm1(self):
		return self.term1

	def getTerm2(self):
		return self.term2

	def printDetails(self):
		print("\n------")
		print(self.id)
		print(self.relationid)
		print(self.term1 + " | " + self.label)
		print("------\n")