from context.asstypes import AssTypeInfo
from context.conceptnet import ConceptNet
from context.dbpedia import DBPedia
from context.googlesearch import GoogleSearch
from context.alchemyapi import AlchemyAPI
from prepros.dictionaries.fan_dic import FanDomDictionary
import spacy
import re

class FanExtractor:

	asstypeinfo = AssTypeInfo()
	nlp = spacy.load('en')
	conceptnet = ConceptNet()
	gsearch = GoogleSearch()
	api = AlchemyAPI()
	dbpedia = DBPedia()
	person = ""
	persona = ""

	# Dictionaries
	fandomDic = FanDomDictionary()

	# Keywords
	categoryType = "art and entertainment"
	applicableTypes = ["FictionalCharacter", "Broadcaster", "Publisher", "RecordLabel", "Band", "ComedyGroup", "Artist", "BeautyQueen", "Producer", "TelevisionDirector", "TheatreDirector", "Writer", "Instrument", "FilmFestival", "MusicFestival", "Media", "Fashion", "Genre", "Artwork", "Cartoon", "Film", "LineOfFasion", "MusicalWork", "TelevisionEpisode", "TelevisionSeason", "TelevisionShow", "Novel", "Comic", "Drama", "Play", "Poem", "Artist", "Writer", "Director"]
	gSearchFreq = ["novelist", "actor", "anime", "series", "journalism", "actor", "producer", "movie", "singer", "musical", "film", "author", "publisher", "editor", "writer", "author", "photographer", "book", "novel", "theater", "theatre", "personality", "music", "blogger", "podcasts", "musician", "books", "novels", "artists", "films", "actress"]

	def fanExtract(self, posts, persona, person):
		self.person = person
		self.persona = persona

		ctr = 1
		storyDict = {} # ACTION, PAGE, TAGGED, ORGANIZATION

		# For Each Cleaned Posts
		for p in posts:
			storyDict = self.extractStory(p.story)

			self.extractPost(p.post)

			print("CONTEXT: ", ctr, " of ", len(posts))
			ctr += 1

		# assertions = self.generateAssertions()
		# return assertions

	def extractPost(self, post):
		removed = ["i", "you", "it", "we", "they", "he", "she", "them"]
		print("")
		postDoc = self.nlp(post)
		print("POST: ", postDoc)

		## FIND WAYS TO FIND THE SUBJECT AND DETERMINE IF RELATED/
		# Option 1: Create a dictionary of genre and create rules for each group
		# Negative senntiment must be for USER THOUGHTS only. not on post

		if self.api.nlu(post):
			sentiment = self.api.getSentiment()
			categories = self.api.getCategoriesNoRelevance()
			print("SENTIMENT: ", sentiment)
			print("CATEGORIES: ", categories)
			if not self.api.getSentiment() == "negative":
				print(self.api.getConceptsRelevance())
				for chunk in postDoc.noun_chunks:
					if chunk.text.lower() not in removed:
						print("CHUNK: ", chunk.text)
						# print("GSEARCH: ", self.gsearch.search(chunk.text))
			else:
				print("NEGATIVE POST")

	def extractStory(self, story):
		storyDoc = self.nlp(story)
		print("ISTORYA: ", storyDoc)
		storyDict = { "ACTION":"", "PAGE":"", "TAGGED":[], "ORGANIZATION":[] }
		for token in storyDoc:
			if token.pos_ == "VERB":
				if token.text == "shared":
					storyDict['ACTION'] = "Shared"
					result = re.search("shared (.*)'s", story)
					types = []
					if result is not None:
						storyPage = result.group(1)
						storyDict['PAGE'] = storyPage

				# If "IS"
				if token.text == "is":
					print("IS CHILDREN: ", token.children)

			elif token.pos_ == "ADP":
				subchild = [child for child in token.children]
				tagged = []
				org = []

				if token.text == "with":
					subtree = subchild[0].subtree
					subtreeArr = [t.text for t in subtree]
					joinedtext = " ".join(subtreeArr)
					tagged.append(joinedtext)

				elif token.text == "at":
					subtree = subchild[0].subtree
					subtreeArr = [t.text for t in subtree]
					joinedtext = " ".join(subtreeArr)
					org.append(joinedtext)

				storyDict["TAGGED"] = tagged
				storyDict["ORGANIZATION"] = org

		return storyDict
