from context.asstypes import AssTypeInfo
from context.conceptnet import ConceptNet
from context.dbpedia import DBPedia
from context.googlesearch import GoogleSearch
from context.alchemyapi import AlchemyAPI
import spacy
import re

class FanExtractorOLD:

	asstypeinfo = AssTypeInfo()
	nlp = spacy.load('en')
	conceptnet = ConceptNet()
	gsearch = GoogleSearch()
	api = AlchemyAPI()
	dbpedia = DBPedia()
	categoryType = "art and entertainment"
	applicableTypes = ["FictionalCharacter", "Broadcaster", "Publisher", "RecordLabel", "Band", "ComedyGroup", "Artist", "BeautyQueen", "Producer", "TelevisionDirector", "TheatreDirector", "Writer", "Instrument", "FilmFestival", "MusicFestival", "Media", "Fashion", "Genre", "Artwork", "Cartoon", "Film", "LineOfFasion", "MusicalWork", "TelevisionEpisode", "TelevisionSeason", "TelevisionShow", "Novel", "Comic", "Drama", "Play", "Poem", "Artist", "Writer", "Director"]

	def fanExtract(self, post, persona, person):
		people_mentioned = post.person
		hashtags = post.hashtags
		mentions = post.mentions
		assertions = [] # Append here all values of assertions
		sentiment = self.nlp(post.sentiment)
		relevantSubject = {}
		base_data = self.asstypeinfo.getChecklist(persona)
		isEvident = False
		sentimentEvident = False
		storyEvident = False
		postEvident = False
		storyActivity = ""
		storyPage = ""
		subjectSituation = -1

		# Get Mentioned Friends
		friends = []
		if not people_mentioned == None:
			for p in people_mentioned:
				if not p == person:
					friends.append(p)
		base_data['Tagged_Friends'] = friends

		# Get Person
		base_data['Person'] = person

		# Searches on the whole post if the post is related to the user preference
		if not post.sentiment == "":
			sentimentEvident = self.isCategoryEvident(self.categoryType, post.sentiment)
		if not post.story == "":
			result = re.search("shared(.*)'s", post.story)
			if result is not None:
				storyActivity = "shared"
				storyPage = result.group(1)
				storyEvident = self.isCategoryEvident(self.categoryType, "shared " + storyPage)
		if not post.post == "":
			postEvident = self.isCategoryEvident(self.categoryType, post.post)

		if sentimentEvident or storyEvident or postEvident:
			isEvident = True

		# if there is a user sentiment
		if not post.sentiment == "":
			print("postEvident: ", post.sentiment)
			sents = [child for child in sentiment.sents]
			print("SENTENCES LENGTH: ", len(sents))

			if len(sents) < 3:
				token_dict = {}
				rootToken = None
				nSubjs = None

				rootToken = self.find_root(sentiment)
				verbs = self.find_verb(sentiment)

				if not len(verbs) == 0:
					for v in verbs:
						subject = ""
						predicate = ""
						headChildren = [child for child in v.head.children]
						print("VERB: ", v.text ,"CHILDREN: ", headChildren)
						for ch in headChildren:
							token = self.find_token(ch, sentiment)
							if token.dep_ == "nsubj":
								subtree = token.subtree
								subtreeArr = [t.text for t in subtree]
								joinedtext = " ".join(subtreeArr)
								subject = joinedtext
								subchild = [child for child in v.head.children]
								print("SUBJECT: ", subject ,"CHILDREN: ", subchild)
								print("SUBJECT: ", subject)
							else:
								subtree = token.subtree
								subtreeArr = [t.text for t in subtree]
								joinedtext = " ".join(subtreeArr)
								print("JOINED: ", joinedtext)

						if subject == "i" or subject == "me" or subject == "I'm" or subject == "myself" or subject == "I":
							print("[ACTION] IF IT IS THE USER")
							print("OWN VERB: ", subject, " ", v.text)
						else:
							print("[ACTION] IF NOT THE USER")
							print("shared about", subject)
							if self.api.nlu("shared about" + subject):
								concepts = self.api.getConcepts()
								print("CONCEPTS: ", concepts)
								if concepts is not None:
									concept, location = self.getConcept(concepts)
									if len(concept) == 1:
										# data['FanOf'] = concept[0]
										print("SUBJECT: ", concept[0])
										if self.api.nlu("shared" + concept[0]):
											categories = self.api.getCategoriesNoRelevance()
											types = []
											types = self.getFinalCategory(self.categoryType, categories)
											typ = self.dbpedia.getType(concept[0])
											for t in typ:
												if t in self.applicableTypes:
													types.append(t)
											print("TYPES: ", types)
				# print("ROOT: ", rootToken.text, " NSUBJ: ", nSubjs, " SUBJSITUATION: ", subjectSituation)
			else:
				if postEvident:
					data = base_data.copy()
					if self.api.nlu(post.sentiment):
						concepts = self.api.getConcepts()
						if concepts is not None:
							concept, location = self.getConcept(concepts)
							if len(concept) == 1:
								# print("Post Evident: ", concept[0])
								data['FanOf'] = concept[0]
								if self.api.nlu("shared " + concept[0]):
									categories = self.api.getCategoriesNoRelevance()
									types = []
									types = self.getFinalCategory(self.categoryType, categories)
									typ = self.dbpedia.getType(concept[0])
									for t in typ:
										if t in self.applicableTypes:
											types.append(t)
									data['Type'] = types
					data['Action'] = "Shared About"
					assertions.append(data)
				else:
					if storyEvident:
						if self.api.nlu("shared " + storyPage):
							categories = self.api.getCategoriesNoRelevance()

							types = []
							types = self.getFinalCategory(self.categoryType, categories)
							typ = self.dbpedia.getType(storyPage)
							for t in typ:
								if t in self.applicableTypes:
									types.append(t)

							data = base_data.copy()
							data['FanOf'] = storyPage
							data['Action'] = "Shared About"
							data['Type'] = types
							assertions.append(data)
					elif postEvident:
						data = base_data.copy()
						if self.api.nlu(post.post):
							concepts = self.api.getConcepts()
							if concepts is not None:
								concept, location = self.getConcept(concepts)
								if len(concept) == 1:
									# print("Post Evident: ", concept[0])
									data['FanOf'] = concept[0]
									if self.api.nlu("shared " + concept[0]):
										categories = self.api.getCategoriesNoRelevance()
										types = []
										types = self.getFinalCategory(self.categoryType, categories)
										typ = self.dbpedia.getType(concept[0])
										for t in typ:
											if t in self.applicableTypes:
												types.append(t)
										data['Type'] = types
						data['Action'] = "Shared About"
						assertions.append(data)

			# for token in sentiment:
			# 	values = {}
			# 	values['text'] = token.text
			# 	values['dep'] = token.dep_
			# 	values['pos'] = token.pos_
			# 	values['head'] = token.head.text
			# 	values['head_pos'] = token.head.pos_
			# 	values['children'] = [child for child in token.children]
			# 	print("VALUES: ", values)

			# 	if token.dep_ == "nsubj":
			# 		if token.head.text == rootToken.text:
			# 			if token.text == "i" or token.text == "I" or token.text == "me" == token.text == "i'm" or token.text == "I'm" or token.text == "myself":
			# 				if rootToken.pos_ == "VERB":
			# 					subjectSituation = 2 # Narrating an activity
			# 				elif rootToken.pos_ == "ADJ":
			# 					subjectSituation = 3 # Describing a subject
			# 				nSubj = token.text
			# 			else:
			# 				subjectSituation = 0 # Providing a statement
			# 				nSubj = token.text

			# if nSubj == "" and rootToken.pos_ == "VERB":
			# 	nSubj = "I"
			# 	subjectSituation = 2

				# if token.dep_  == "nsubj":
				# 	subtree = token.subtree
				# 	subtreeArr = [t.text for t in subtree]
				# 	subj = " ".join(subtreeArr)
				# 	print("SUBJ: ", subj)
				# 	# If I... Get the action, etc.
				# 	if token.text == "i":
				# 		print("subj: ", subj)
				# 		print("Root: ", values['head'], " POS: ", values['head_pos'])
				# 		headChildren = [child for child in token.head.children]
				# 		print("CHILDREN: ", headChildren)
				# 		# if token.pos_ == "VERB":
				# 			# base_data['Action'] == values['head']


				# token_dict[token.text] = values
		else:
			if storyEvident:
				# print("Story Evident: ", storyPage)
				if self.api.nlu("shared " + storyPage):
					categories = self.api.getCategoriesNoRelevance()

					types = []
					types = self.getFinalCategory(self.categoryType, categories)
					typ = self.dbpedia.getType(storyPage)
					for t in typ:
						if t in self.applicableTypes:
							types.append(t)

					data = base_data.copy()
					data['FanOf'] = storyPage
					data['Action'] = "Shared About"
					data['Type'] = types
					assertions.append(data)
			elif postEvident:
				data = base_data.copy()
				if self.api.nlu(post.post):
					concepts = self.api.getConcepts()
					if concepts is not None:
						concept, location = self.getConcept(concepts)
						if len(concept) == 1:
							# print("Post Evident: ", concept[0])
							data['FanOf'] = concept[0]
							if self.api.nlu("shared " + concept[0]):
								categories = self.api.getCategoriesNoRelevance()
								types = []
								types = self.getFinalCategory(self.categoryType, categories)
								typ = self.dbpedia.getType(concept[0])
								for t in typ:
									if t in self.applicableTypes:
										types.append(t)
								data['Type'] = types
				data['Action'] = "Shared About"
				assertions.append(data)
		# print(assertions)
		return assertions

	def find_root(self, docu):
		for token in docu:
			if token.dep_ == "ROOT":
				return token
		return None

	def find_token(self, text, docu):
		for token in docu:
			if token.text == text.text:
				return token
		return None

	def find_verb(self, docu):
		verbs = []
		for token in docu:
			if token.pos_ == "VERB":
				verbs.append(token)
		return verbs

	def find_nsubj(self, docu):
		subj = []
		for token in docu:
			if token.dep_ == "nsubj":
				subj.append(token)
		return subj
	
	def findCommonValue(self, a, b):
		a_set = set(a)
		b_set = set(b)
		if (a_set & b_set):
			return True
		else:
			return False

	def getConcept(self, concepts):
		concept = []
		location = []
		if concepts is not None:
			for c in concepts:
				con = c['text']
				if c['relevance'] >= 0.5:
					types = self.dbpedia.getType(con)
					if "Location" in types:
						location.append(con)
					elif "Place" in types:
						location.append(con)
					elif "Facility" in types:
						location.append(con)
					else:
						if len(concept) == 0:
							concept.append(con)
				
			return concept, location
		else:
			return None, None

	def isCategoryEvident(self, category, text):
		evident = False

		if self.api.nlu(text):
			categories = self.api.getCategoriesNoRelevance()
			if self.checkIfCategoryExists(category, categories):
				evident = True

		return evident

	def isCategoryEvidentAll(self, category, p):
		sentiment = False
		story = False
		post = False

		if not p.sentiment == "":
			if self.api.nlu(p.sentiment):
				categories = self.api.getCategoriesNoRelevance()
				if self.checkIfCategoryExists(category, categories):
					sentiment = True

		if not p.story == "":
			if self.api.nlu(p.story):
				categories = self.api.getCategoriesNoRelevance()
				if self.checkIfCategoryExists(category, categories):
					story = True

		if not p.post == "":
			if self.api.nlu(p.post):
				categories = self.api.getCategoriesNoRelevance()
				if self.checkIfCategoryExists(category, categories):
					post = True

		return sentiment, story, post

	def checkIfCategoryExists(self, category, categories):
		for c in categories:
			each = c['label'].split("/")
			if each[1] == category:
				return True
		return False

	def getFinalCategory(self, category, categories):
		cat = []
		for c in categories:
			each = c['label'].split("/")
			if each[1] == category:
				cat.append(each[len(each)-1])
		return cat


	def extractStoryInformation(self, story):
		if self.api.nlu(story):
			semanticRoles = self.api.getSemanticRoles()
			entities = self.api.getEntities()

			action = ""
			org = []
			location = []
			taggedperson = []

			for s in semanticRoles:
				# Get Action
				action = s['action']['verb']['text']

				for ent in entities:
					if ent['type'] == "Company" or ent['type'] == "Facility":
						org.append(ent['text'])

					if ent['type'] == "Location":
						location.append(ent['text'])

					if ent['type'] == "Person":
						taggedperson.append(ent['text'])

			if action == "share":
				return action, org, [], []
			else:
				return action, org, location, taggedperson
		else:
			return [], [], [], []


	def getPersonMentioned(self):
		entities = self.api.getEntities()
		people = []

		for ent in entities:
			if ent['relevance'] >= 0.50:
				if ent['type'] == "Person":
					people.append(ent['text'])

		return people

	def getPlace_Organization(self):
		entities = self.api.getEntities()
		orgs = []
		places = []

		for ent in entities:
			if ent['relevance'] >= 0.75:
				if ent['type'] == "Company" or ent['type'] == "Facility":
					orgs.append(ent['text'])

				if ent['type'] == "Location":
					places.append(ent['text'])

		return orgs, places	