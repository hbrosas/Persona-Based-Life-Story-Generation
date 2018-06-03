
class ApostropheDictionary(object):
	dictionary = {}

	def __init__ (self):
		self.dictionary = {
			# "n't "		:	"not",
			# "'ve "		:	"have",
			# "'d "		:	"had",
			# "'m "		:	"am",
			# "'ll "		:	"will",
			# "'re "		:	"are",
			"doesn't"		:	"does not",
			"can't"		:	"can not",
			"won't"		:	"will not",
			"don't"		:	"do not",
			"i've"		:	"I have",
			"i'd"		:	"I had",
			"i'm"		:	"I am",
			"i'll"		:	"I will",
			"she's "		:	"she is",
			"he's"		:	"he is",
			"it's"		:	"it is",
			"there's"		:	"there is",
			"they're"		:	"they are",
			"we're"		:	"we are",
			"you've"		:	"you have",
			"you're"		:	"you are",
			"couldn't"	:	"could not",
			"shouldn't "	:	"should not",
			"wouldn't"	:	"would not",
			"doesnt"		:	"does not",
			"cant"		:	"can not",
			"wont"		:	"will not",
			"dont"		:	"do not",
			"ive"		:	"I have",
			"id"			:	"I had",
			"im"			:	"I am",
			"ill"		:	"I will",
			"shes"		:	"she is",
			"hes"		:	"he is",
			"theres"		:	"there is",
			"theyre"		:	"they are",
			"youve"		:	"you have",
			"youre"		:	"you are",
			"couldnt"		:	"could not",
			"shouldnt"	:	"should not",
			"wouldnt"		:	"would not",
			"'cos"		:	"because",
			"'cause "		:	"because",
			"'coz"		:	"because"
		}

	def replace(self, key):
		return self.replace_all(key, self.dictionary)
		

	def replace_all(self, text, dic):
		for i, j in dic.items():
			text = text.replace(i, j)
		return text

	def lookup(self, key):
		return self.dictionary.get(key)