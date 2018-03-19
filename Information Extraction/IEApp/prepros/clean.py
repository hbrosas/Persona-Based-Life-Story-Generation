# This function contains the main process of data pre-processing

from prepros.spellcheck import SpellChecker
from prepros.normie import Normalizer
from prepros.dictionaries.apostrophe_dic import ApostropheDictionary
import spacy
import ciseau
import language_check
import html.parser

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

	def clean(self, original_post):

		nlp = spacy.load('en')

		#1 Escape HTML Characters
		html_parser = html.parser.HTMLParser()
		post = html_parser.unescape(original_post)

		#2 Spell Correction for Tagalog Words
		sc = SpellChecker()
		sc.spell(post)

		#3 Lowercase post
		nlp_post = nlp(post)
		lowercased = nlp_post.text.lower()

		#3 Apostrophe Lookup
		# aposdic = ApostropheDictionary()


		# tool = language_check.LanguageTool('en-US')
		# matches = tool.check(original_post)
		# print(language_check.correct(original_post, matches))

	def cleanData(self, posts):
		for p in posts:
			print(p.getPost())
			# print(ciseau.tokenize(p.getPost()))
			self.clean(p.getPost())

			# normedSentences = []
			# # print('')
			# # print("Input: ", post)
			# nlp = spacy.load('en')
			# nm = Normalizer()
			# sc = SpellChecker()

			# doc = nlp(p.getPost())
			# for st in doc.sents:
			# 	# print("Before: ", st)
			# 	# newpost = nm.normalize(st.text)
			# 	# newpost = sc.spell3(st)
			# 	# print("After: ", newpost)
			# 	normedSentences.append(st.text)

			# for nsen in normedSentences:
			# 	tokens = []
			# 	toBeTokenized = nlp(nsen)
			# 	for token in toBeTokenized:
			# 		tok = sc.spell(token.text)
			# 		print(token.text, " - ", token.ent_type_, " - ", token.norm_)