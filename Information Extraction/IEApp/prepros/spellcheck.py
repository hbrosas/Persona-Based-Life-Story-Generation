from prepros.entity import Entity
from hunspell import Hunspell
from textblob import TextBlob
from prepros.dictionaries.apostrophe_dic import ApostropheDictionary
from prepros.dictionaries.slang_dic import SlangDictionary
import spacy
import os 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import collections
import numpy as np

class SpellChecker:

	"""
	NOTE: Find ways to maximize the use of textblob and hunspell

	1. Check first the entity - if there is an entity, return.
	2. Check if exists in Wikipedia and ConceptNet. If yes, it means the spelling is correct thus return the token.
	3. Else, correct spelling.

	ISSUE # 1:
	- Since one dictionary can only be used at a time, don't know when to use the each dictionary.
	SOLUTION: Try to install hunspell (this one's cyhunspell), but that'll be hard.

	"""

	def spell(self, post):
		nlp = spacy.load('en')
		ent = Entity()
		fpost = ""

		toBeTokenized = nlp(post)
		for token in toBeTokenized:
			aposdic = ApostropheDictionary()
			slangdic = SlangDictionary()
			aposLookup = aposdic.lookup(token.orth_.lower())
			slangLookup = aposdic.lookup(token.orth_.lower())
			# print("Token: ", token.orth_, " Entity: ", token.ent_type_ + " POS: " + token.pos_ + " TAG: " + token.tag_ + " DEP: " + token.dep_)
			if aposLookup == None:
				if slangLookup == None:
					if token.ent_type_ == "" and not token.is_digit and not token.like_url and not token.like_email:
						if not token.is_punct:
							entity = ent.doesExists(token)
							if not ent.doesExists(token):
								fil_tok = self.spell_Fil(token.text)
								fil_similar = self.findMostSimilar(token.text, fil_tok)
								eng_tok = self.spell_Eng(token.text)
								eng_similar = self.findMostSimilar(token.text, eng_tok)
								final = self.compareWord(token.text, fil_similar, eng_similar)
								fpost = fpost + final + " "
							else:
								fpost = fpost + entity + " "	
						else:
							fpost = fpost + token.text + " "	
					else:
						fpost = fpost + token.text + " "
				else:
					fpost = fpost + slangLookup + " "
			else:
				fpost = fpost + aposLookup + " "

		print("Spelled: ", fpost)
		return fpost;

	def compareWord(self, word, fil, eng):
		fscore = fuzz.ratio(word, fil)
		escore = fuzz.ratio(word, eng)

		if fscore == escore:
			return eng
		elif fscore > escore:
			return fil
		else:
			return eng

	def findMostSimilar(self, word, tokens):
		similar = ""
		highest = 0

		for t in tokens:
			score = fuzz.ratio(word, t)
			# print(t, " to ", word, " SCORE: ", score)
			if score > highest:
				similar = t

		return similar

	def spell_Fil(self, token):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		tok = []
		h = Hunspell('tl', hunspell_data_dir = dir_path + '/dictionaries/')

		if not h.spell(token):
			tok = h.suggest(token)
		else:
			tok.append(token)

		return tok

	def spell_Eng(self, token):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		tok = []
		h = Hunspell('en_us', hunspell_data_dir=dir_path + '/dictionaries/')

		if not h.spell(token):
			tok = h.suggest(token)
		else:
			tok.append(token)

		return tok
		