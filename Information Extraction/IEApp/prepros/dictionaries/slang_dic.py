
class SlangDictionary(object):
	dictionary = {}

	def __init__ (self):
		self.dictionary = {
			"wanna"		:	"want to"
		}

	def lookup(self, key):
		return self.dictionary.get(key)