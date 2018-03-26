# This function contains the main process of data pre-processing

from prepros.spellcheck import SpellChecker
from prepros.normie import Normalizer
from prepros.emojiremove import EmojiRemove
from prepros.dictionaries.apostrophe_dic import ApostropheDictionary
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
	8. Removal of Punctuations except “.”, “,”,”?”
	9. Removal of Expressions. Ex. Haha, Hehe, Huhu
	10. Split Attached Words
	11. Slang Lookup
	12. Standardizing words
	13. Grammar Checking
	*14. Spelling Correction for English Words
"""

class Clean:

	def cleanData(self, posts):
		for p in posts:
			print(p.getPost())
			self.clean(p.getPost())

	def clean(self, original_post):
		print("")

		nlp = spacy.load('en')

		#1 Escape HTML Characters
		html_parser = html.parser.HTMLParser()
		post = html_parser.unescape(original_post)

		#2 Standardize
		post = ''.join(''.join(s)[:2] for _, s in itertools.groupby(post))
		print("STANDARDIZED: ", post)

		#3 Removal of Expression. Ex. Haha, Hehe, Huhu
		post = re.sub('(a*ha+h[ha]*|(?:l+o+)+l+|e*he+h[he]*|i*hi+h[hi]*|o*ho+h[ho]*|u*hu+h[hu]*)', '', post)
		post = re.sub('(A*HA+H[HA]*|(?:L+O+)+L+|E*HE+H[HE]*|I*HI+H[HI]*|O*HO+H[HO]*|U*HU+H[HU]*)', '', post)
		print("Removed Expressions: ", post)

		#4 Removal of Emoticons
		post = EmojiRemove.remove_emoji(post)
		print("Removed Emojis: ", post)

		nlp = spacy.load('en')
		#5 Separate to sentences
		doc = nlp(post)

		for sent in doc.sents:
			# sc = SpellChecker()
			# sentence = sc.spell(sent.text)
			self.separateEntities(sentence)

			print("")



		#3 Spell Correction for Tagalog Words
		#4 Apostrophe Lookup
		#5 Slang Lookup
		
		# print("")

		#6 Split Attached Words
		# post = " ".join(re.findall('[A-Z][^A-Z]*', post))

		#4 Google Translate


		# tool = language_check.LanguageTool('en-US')
		# matches = tool.check(post)
		# print(language_check.correct(original_post, matches))

	def separateEntities(self, post):
		# nlp = spacy.load('en')
		# doc = nlp(post.text)

		np_extractor = NPExtractor(post)
		result = np_extractor.extract()
		print ("This sentence is about: %s" % ", ".join(result))
		translator = TGENTranslator()
		translator.translateQuery(post)

		# for token in doc:
		# 	print(token.text + " | " + token.pos_ + " | " + token.dep_)
			# nlp = spacy.load('en')
			# doc = nlp(post)
			# tokens = []

			# for token in doc:
			# 	tokens.append(token.text)

			# print(tokens)
			# print(self.combinations(tokens))

	def combinations(self, list):
		combos = []

		# n = 0
		# while n < len(list): 11 m 



	