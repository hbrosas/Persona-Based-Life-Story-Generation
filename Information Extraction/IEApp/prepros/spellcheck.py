from prepros.entity import Entity
from hunspell import Hunspell
from textblob import TextBlob
from prepros.dictionaries.apostrophe_dic import ApostropheDictionary
from prepros.dictionaries.slang_dic import SlangDictionary
from models.tokent import Tokent
import spacy
import os 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import collections
import numpy as np
import re

class SpellChecker:

	def spell(self, text, post):
		nlp = spacy.load('en')
		doc = nlp(text)
		ent = Entity()
		fpost = ""
		words = []
		reservedWord = ""

		for w in doc:
			if w.is_punct:
				fpost = fpost + w.text + " "
			else:
				if w.ent_type_ == "":
					if not self.inPeople(w.text, post.person):
						if not self.spellCorrect(w.text):
							if not ent.doesExists(w.text):
								fil_tok = self.spell_Fil(w.text)
								fil_similar = self.findMostSimilar(w.text, fil_tok)
								eng_tok = self.spell_Eng(w.text)
								eng_similar = self.findMostSimilar(w.text, eng_tok)
								final = self.compareWord(w.text, fil_similar, eng_similar)
								fpost = fpost + final + " "
							else:
								fpost = fpost + w.text + " "	
						else:
							fpost = fpost + w.text + " "	
					else:
						fpost = fpost + w.text + " "	
				else:
					fpost = fpost + w.text + " "

		# print("Spelled: ", fpost)
		return fpost;

	def inPeople(self, text, people):
		if any(text in s for s in people):
			return True
		else:
			return False

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
				highest = score

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

	def spellCorrect(self, token):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		h = Hunspell('tl', hunspell_data_dir = dir_path + '/dictionaries/')

		if not h.spell(token):
			h = Hunspell('en_us', hunspell_data_dir=dir_path + '/dictionaries/')
			if not h.spell(token):
				return False
			else:
				return True
		else:
			return True
		