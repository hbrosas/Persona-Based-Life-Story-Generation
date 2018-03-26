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

	def spell(self, post):
		nlp = spacy.load('en')
		ent = Entity()
		fpost = ""
		words = []
		hyphen = re.compile('^-([A-Z]*[a-z]*)*') # Regex for any word that ends in -
		reservedWord = ""

		toBeTokenized = nlp(post)
		for token in toBeTokenized:
			word = token.text
			if not token.like_url and not token.like_email:
				if not reservedWord == "":
					words.append(Tokent((reservedWord + word), token.pos_, token.ent_type_))
					reservedWord = ""
				else:
					if hyphen.match(word):
						reservedWord = word
					else:
						words.append(Tokent(word, token.pos_, token.ent_type_))

		for w in words:
			print("Word: " + w.token)
			aposdic = ApostropheDictionary()
			slangdic = SlangDictionary()
			aposLookup = aposdic.lookup(w.token.lower())
			slangLookup = aposdic.lookup(w.token.lower())
			if aposLookup == None:
				if slangLookup == None:
					if w.entity == "" :
						entity = ent.doesExists(w.token)
						if not ent.doesExists(w.token):
							fil_tok = self.spell_Fil(w.token)
							fil_similar = self.findMostSimilar(w.token, fil_tok)
							eng_tok = self.spell_Eng(w.token)
							eng_similar = self.findMostSimilar(w.token, eng_tok)
							final = self.compareWord(token.text, fil_similar, eng_similar)
							fpost = fpost + final + " "
						else:
							fpost = fpost + entity + " "	
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
		