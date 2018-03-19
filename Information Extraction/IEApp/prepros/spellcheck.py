from prepros.entity import Entity
from hunspell import Hunspell
from textblob import TextBlob
from prepros.dictionaries.apostrophe_dic import ApostropheDictionary
import spacy
import os 

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

		toBeTokenized = nlp(post)
		for token in toBeTokenized:
			aposdic = ApostropheDictionary()
			aposLookup = aposdic.lookup(token.orth_.lower())
			if aposLookup == None:
				if not token.ent_type_ == None and not token.is_stop and not token.like_url:
					ent.isAnEntity(token)
					# fil_tok = self.spell_Fil(token.text)
					# eng_tok = self.spell_Eng(token.text)
					# print(fil_tok)
					# print(eng_tok)
				else:
					print(token.text)

	def spell_Fil(self, token):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		tok = None
		h = Hunspell('tl', hunspell_data_dir = dir_path + '/dictionaries/')

		if not h.spell(token):
			tok = h.suggest(token)
		else:
			tok = token

		return tok

	def spell_Eng(self, token):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		tok = None
		h = Hunspell('en_us', hunspell_data_dir=dir_path + '/dictionaries/')

		if not h.spell(token):
			tok = h.suggest(token)
		else:
			tok = token

		return tok
		