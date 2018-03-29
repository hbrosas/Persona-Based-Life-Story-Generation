import re, sys
import spacy

"""
	Author: Fanjun
	Base Code: remove_emoji
"""

class EmojiRemove:

	def removeExtras(text):
		nlp = spacy.load('en')
		doc = nlp(text)
		ftext = ""
		for w in doc:
			if not w.like_url and not w.like_email:
				ftext += w.text + " "

		return ftext

	def removeWhitespaces(text):
		wsPattern = re.compile(u"""[* ]+""")
		text = wsPattern.sub(r' ', text).encode('utf8')
		return text.decode('utf8')

	def removeNewLine(text):
		newlinePattern = re.compile(u"""[*\n]+""", flags=re.UNICODE)
		text = newlinePattern.sub(r' ', text).encode('utf8')
		return text.decode('utf8')

	def remove_specialChars(text):
		specialCharPattern = re.compile(u"""[^A-Za-z0-9.!?,'" @&:/]+""", flags=re.UNICODE)
		text = specialCharPattern.sub(r'', text).encode('utf8')
		return text.decode('utf8')

	def remove_emoji(text):
		emoji_pattern = re.compile(
					    """(\:\w+\:|\<[\/\\]*3|[\(\)\\\D|\*\$][\-\^]?[\:\;\=]|[\:\;\=B8]"""+
					    """[\-\^\"\']*[3DOPp\@\$\*\\\)\(\/\|\>\]\}\<\[\{]*)(?=\s|[\!\.\?]|$)""") 

		text = emoji_pattern.sub(r'.', text).encode('utf8')
		return text.decode('utf8')