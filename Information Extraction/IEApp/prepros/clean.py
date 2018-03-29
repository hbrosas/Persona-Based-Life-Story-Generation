# This function contains the main process of data pre-processing

from prepros.spellcheck import SpellChecker
from prepros.normie import Normalizer
from prepros.emojiremove import EmojiRemove
from prepros.dictionaries.apostrophe_dic import ApostropheDictionary
from prepros.dictionaries.slang_dic import SlangDictionary
from context.npextractor import NPExtractor
from context.translator import TGENTranslator
import spacy
import ciseau
import language_check
import html.parser
import itertools
import re

"""
	From  Source: https://www.analyticsvidhya.com/blog/2014/11/text-data-cleaning-steps-python/ (Not all)
	FINAL METHOD:
	1. Escape HTML Characters
	2. Spell Correction for Tagalog Words
		- if it does not have an entity yet, search through semantic ontology and get if it has any entity
	3. Lowercase everything first because of lookup dictionary
	4. Google Translate
	5. Apostrophe Lookup
	8. Removal of Punctuations except “.”, “,”, ”?”
	9. Removal of Expressions. Ex. Haha, Hehe, Huhu
	10. Split Attached Words
	11. Slang Lookup
	12. Standardizing words
	13. Grammar Checking
	*14. Spelling Correction for English Words
"""

class Clean:

	def cleanData(self, posts):
		cleaned_posts = []
		for p in posts:
			# print(p.getPost())
			post = self.clean(p.getPost())
			cleaned_posts.append(post)

		return cleaned_posts

	def clean(self, original_post):
		nlp = spacy.load('en')

		#1 Escape HTML Characters
		html_parser = html.parser.HTMLParser()
		post = html_parser.unescape(original_post)

		#2 Standardize
		post = ''.join(''.join(s)[:2] for _, s in itertools.groupby(post))
		# print("STANDARDIZED: ", post)

		#3 Removal of Expression. Ex. Haha, Hehe, Huhu
		post = re.sub('(a*ha+h[ha]*|(?:l+o+)+l+|e*he+h[he]*|i*hi+h[hi]*|o*ho+h[ho]*|u*hu+h[hu]*)', '', post)
		post = re.sub('(A*HA+H[HA]*|(?:L+O+)+L+|E*HE+H[HE]*|I*HI+H[HI]*|O*HO+H[HO]*|U*HU+H[HU]*)', '', post)
		# print("Removed Expressions: ", post)

		# Remove New Line
		post = EmojiRemove.removeNewLine(post)
		# print("Removed New Lines: ", post)

		# Remove Emoticons
		post = EmojiRemove.remove_emoji(post)
		# print("Removed Emojis: ", post)

		# Remove Special Characters
		post = EmojiRemove.remove_specialChars(post)
		# print("Removed Special Characters: ", post)

		aposdic = ApostropheDictionary()
		fromIsApos = False
		doc = nlp(post)
		post = ""

		for x in range(0, len(doc)):
			if fromIsApos:
				# Ignore next token
				fromIsApos = False
			else:
				if not x == len(doc)-1:
					key = doc[x].text + doc[x+1].text

					#3 Apostrophe Lookup
					isApos = aposdic.lookup(key.lower())

					if not isApos == None:
						post += isApos + " "
						fromIsApos = True
					else:
						post += doc[x].text + " "
				else:
					post += doc[x].text + " "
		
		# print("Apostrophe Lookup: ", post)

		# Remove URLS and Emails
		post = EmojiRemove.removeExtras(post)
		# print("Removed URLs and Emails: ", post)

		#4 Slang Lookup
		slangdic = SlangDictionary()
		post = slangdic.replace(post.lower())
		# print("Slang Lookup: ", post)

		# Whitespaces
		post = EmojiRemove.removeWhitespaces(post)
		# print("Removed Whitespaces: ", post)

		# Spell Correct
		sc = SpellChecker()
		post = sc.spell(post)

		# Google Translate
		translator = TGENTranslator()
		post = translator.translateQuery(post)

		# print("CLEANED: ", post)

		# Language Check
		# tool = language_check.LanguageTool('en-US')
		# matches = tool.check(post) 
		# print(language_check.correct(post, matches))

		return post

	def separateEntities(self, post):
		# nlp = spacy.load('en')
		# doc = nlp(post.text)

		np_extractor = NPExtractor(post)
		result = np_extractor.extract()
		print ("This sentence is about: %s" % ", ".join(result))
		translator = TGENTranslator()
		translator.translateQuery(post)



	