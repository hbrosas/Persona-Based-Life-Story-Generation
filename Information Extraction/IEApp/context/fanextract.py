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
	fandomDic = FanDomDictionary()
	categoryType = "art and entertainment"
	applicableTypes = ["FictionalCharacter", "Broadcaster", "Publisher", "RecordLabel", "Band", "ComedyGroup", "Artist", "BeautyQueen", "Producer", "TelevisionDirector", "TheatreDirector", "Writer", "Instrument", "FilmFestival", "MusicFestival", "Media", "Fashion", "Genre", "Artwork", "Cartoon", "Film", "LineOfFasion", "MusicalWork", "TelevisionEpisode", "TelevisionSeason", "TelevisionShow", "Novel", "Comic", "Drama", "Play", "Poem", "Artist", "Writer", "Director"]
	gSearchFreq = ["novelist", "actor", "anime", "series", "journalism", "actor", "producer", "movie", "singer", "musical", "film", "author", "publisher", "editor", "writer", "author", "photographer", "book", "novel", "theater", "theatre", "personality", "music", "blogger", "podcasts", "musician", "books", "novels", "artists", "films", "actress"]

	def fanExtract(self, post, persona, person):
		# "Person" 			: None,
		# "FanOf" 			: None,
		# "Description"		: None,
		# "Action"			: None,
		# "Event"			: None,
		# "Tagged_Friends" 	: None,
		# "Location" 		: None,
		# "Organization" 	: None,
		# "Sentiment" 		: None,
		# "Date"		 	: None,
		# "Type"		 	: None,
		# "Time"			: None

		people_mentioned = post.person
		hashtags = post.hashtags
		mentions = post.mentions
		assertions = [] # Append here all values of assertions
		base_data = self.asstypeinfo.getChecklist(persona)

		# Get Mentioned Friends
		friends = []
		if not people_mentioned == None:
			for p in people_mentioned:
				if not p == person:
					friends.append(p)
		base_data['Tagged_Friends'] = friends

		# Get Person
		base_data['Person'] = person

		storyInfo = {}
		postInfo = {}
		activityInfo = []
		describeInfo = []
		subjectInfo = {}

		if not post.story == "":
			storyInfo = self.extractStory(post.story)
			# print("STORY: ", storyInfo)

		if not post.post == "":
			postInfo = self.extractPost(post.post)
			# print("POST: ", postInfo)

		sentInfo = ""
		
		if not post.sentiment == "":
			activityInfo, describeInfo, subjectInfo, sentInfo = self.extractSentiment(post.sentiment)
			# print("ACTIVITY: ", activityInfo)
			# print("DESCRIBE: ", describeInfo)
			# print("SUBJECT: ", subjectInfo)
			# print("SENTIMENT: ", sentInfo)

		if sentInfo == "positive" or sentInfo == "negative":
			base_data['Sentiment'] = sentInfo

		if not post.sentiment == "":
			# If has sentiment

			if not len(activityInfo) == 0:

				for act in activityInfo:
					# For every action
					data = base_data.copy()

					if act['OBJECT'] == "it":
						# If "it", get subject from Post and set verb as action
						data['Action'] = act['VERB']
						# If has post, get subjects and create an assertion for each an copy type for each
						if not post.post == "":
							# If has subjects
							if "SUBJECTS" in postInfo:
								if len(postInfo['SUBJECTS']) == 0:
									for pSubj in postInfo['SUBJECTS']:
										postData = data.copy()
										postData['FanOf'] = pSubj
										postData['Type'] = postInfo['TYPE']
										postData['Organization'] = postInfo['ORG']
										postData['Location'] = postInfo['LOCATION']
										assertions.append(postData)
								else:
									# Get from story
									if not post.story == "":
										if len(storyInfo['TYPES']) != 0:
											postData = data.copy()
											postData['FanOf'] = storyInfo['PAGE']
											postData['Type'] = storyInfo['TYPES']

											if "ORGANIZATION" in storyInfo:
												postData['Organization'] = storyInfo['ORGANIZATION']

											assertions.append(postData)

									if "FANDOM" in storyInfo:
										postData = data.copy()
										postData['Type'] = storyInfo['TYPES']

										if "ORGANIZATION" in storyInfo:
											postData['Organization'] = storyInfo['ORGANIZATION']

										postData['Fandom'] = storyInfo['FANDOM']
										postData['FanOf'] = storyInfo['FANOF']
										assertions.append(postData)
							else:
								# Get from story
								if not post.story == "":
									if "TYPES" in storyInfo:
										if len(storyInfo['TYPES']) != 0:
											postData = data.copy()
											postData['FanOf'] = storyInfo['PAGE']
											postData['Type'] = storyInfo['TYPES']

											if "ORGANIZATION" in storyInfo:
												postData['Organization'] = storyInfo['ORGANIZATION']

											assertions.append(postData)

								if "FANDOM" in storyInfo:
									postData = data.copy()
									postData['Type'] = storyInfo['TYPES']

									if "ORGANIZATION" in storyInfo:
										postData['Organization'] = storyInfo['ORGANIZATION']

									postData['Fandom'] = storyInfo['FANDOM']
									postData['FanOf'] = storyInfo['FANOF']
									assertions.append(postData)
			else:
				assertions = self.createAssertionStoryPost(base_data, post, postInfo, storyInfo, assertions)
		else:
			assertions = self.createAssertionStoryPost(base_data, post, postInfo, storyInfo, assertions)

		# print("ASSERTIONS: ", assertions)
		# print("")
		return assertions

	def createAssertionStoryPost(self, base_data, post, postInfo, storyInfo, assertions):
		data = base_data.copy()
		# If has post, get subjects and create an assertion for each an copy type for each
		if not post.post == "":
			# If has subjects
			if "SUBJECTS" in postInfo:
				if len(postInfo['SUBJECTS']) == 0:
					for pSubj in postInfo['SUBJECTS']:
						postData = data.copy()
						postData['FanOf'] = pSubj
						postData['Type'] = postInfo['TYPE']
						postData['Organization'] = postInfo['ORG']
						postData['Location'] = postInfo['LOCATION']
						assertions.append(postData)
				else:
					# Get from story
					if not post.story == "":
						if "TYPES" in storyInfo:
							if len(storyInfo['TYPES']) != 0:
								postData = data.copy()
								postData['FanOf'] = storyInfo['PAGE']
								postData['Type'] = storyInfo['TYPES']

								if "ORGANIZATION" in storyInfo:
									postData['Organization'] = storyInfo['ORGANIZATION']

								assertions.append(postData)

					if "FANDOM" in storyInfo:
						postData = data.copy()
						postData['Type'] = storyInfo['TYPES']

						if "ORGANIZATION" in storyInfo:
							postData['Organization'] = storyInfo['ORGANIZATION']

						postData['Fandom'] = storyInfo['FANDOM']
						postData['FanOf'] = storyInfo['FANOF']
						assertions.append(postData)
			else:
				# Get from story
				if not post.story == "":
					if "TYPES" in storyInfo:
						if len(storyInfo['TYPES']) != 0:
							postData = data.copy()
							postData['FanOf'] = storyInfo['PAGE']
							postData['Type'] = storyInfo['TYPES']

							if "ORGANIZATION" in storyInfo:
								postData['Organization'] = storyInfo['ORGANIZATION']

							assertions.append(postData)

				if "FANDOM" in storyInfo:
					postData = data.copy()
					postData['Type'] = storyInfo['TYPES']

					if "ORGANIZATION" in storyInfo:
						postData['Organization'] = storyInfo['ORGANIZATION']

					postData['Fandom'] = storyInfo['FANDOM']
					postData['FanOf'] = storyInfo['FANOF']
					assertions.append(postData)
		else:
			# Get from story
			if not post.story == "":
				if "TYPES" in storyInfo:
					if len(storyInfo['TYPES']) != 0:
						postData = data.copy()
						postData['FanOf'] = storyInfo['PAGE']
						postData['Type'] = storyInfo['TYPES']

						if "ORGANIZATION" in storyInfo:
							postData['Organization'] = storyInfo['ORGANIZATION']

						assertions.append(postData)

			if "FANDOM" in storyInfo:
				postData = data.copy()
				postData['Type'] = storyInfo['TYPES']

				if "ORGANIZATION" in storyInfo:
					postData['Organization'] = storyInfo['ORGANIZATION']

				postData['Fandom'] = storyInfo['FANDOM']
				postData['FanOf'] = storyInfo['FANOF']
				assertions.append(postData)

		return assertions


	def extractSentiment(self, sentiment):
		activity = self.narratingActivity(sentiment)
		describe = self.describeSubject(sentiment)
		subject = self.findSubject(sentiment)
		sentiment = self.getSentiment(sentiment)
		return activity, describe, subject, sentiment

	def getSentiment(self, sentiment):
		sent = ""
		if self.api.nlu(sentiment):
			sent = self.api.getSentiment()
		return sent

	# SUBJECT SITUATION: Narrating an Activity
	def narratingActivity(self, sentiment):
		modals = ["is", "are", "was", "were"]
		ownself = ["I", "i", "me", "Me", "myself", "Myself", "I'm", "i'm", "who"]
		wentVerbs = ["going", "go", "went"]

		sentDoc = self.nlp(sentiment)
		verbs = self.find_verb(sentDoc)

		activity = []
		for v in verbs:
			if not v.text in modals:
				children = [child for child in v.children]
				# print("VERB: ", v.text ," CHILDREN: ", children)
				hasNSubj = False # Magiging true lang if nsubj does not belong kay ownself
				hasObj = False # Magiging true lang if may direct object
				obj = ""
				objToken = None
				for child in children:
					if child.dep_ == "nsubj":
						if not child.text in ownself:
							hasNSubj = True
							break
					elif child.dep_ == "dobj" or child.dep_ == "advcl":
						hasObj = True
						subtree = child.subtree
						subtreeArr = [t.text for t in subtree]
						joinedtext = " ".join(subtreeArr)
						obj = joinedtext
						objToken = child

				if not hasNSubj and hasObj:
					values = {}
					values['VERB'] = v.text
					values['OBJECT'] = obj
					values['OBJTOKEN'] = objToken
					activity.append(values)

		# print("Activity: ", activity)
		return activity

	# SUBJECT SITUATON: Describing the Subject
	def describeSubject(self, sentiment):
		modals = ["is", "are", "was", "were"]

		sentDoc = self.nlp(sentiment)
		adj = self.find_adj(sentDoc)

		describe = []
		for a in adj:
			if a.head.text in modals:
				describe.append(a.text)
			if a.dep_ == "ROOT":
				describe.append(a.text)

		# print("DESCRIBE: ", describe)
		return describe


	def find_verb(self, docu):
		verbs = []
		for token in docu:
			if token.pos_ == "VERB":
				verbs.append(token)
		return verbs

	def find_adj(self, docu):
		adj = []
		for token in docu:
			if token.pos_ == "ADJ":
				adj.append(token)
		return adj

	# EXTRACT POST AND FIND SUBJECT
	def extractPost(self, post):
		postDoc = self.nlp(post)
		# print("POST CAPSYON: ", postDoc)
		postDict = {}
		subject = []
		types = []
		org = []
		location = []

		if self.api.nlu(post):
			keywords = self.api.getKeywordsNoRelevance()
			categories = self.api.getCategoriesNoRelevance2()
			concepts = self.api.getConcepts()
			entities = self.api.getEntities()
			relCategories = []
			relConcepts = []

			if concepts is not None:
				found = False
				con = []
				for c in concepts:
					freqs = self.gsearch.search(c)
					if freqs is not None:
						if not ("online" in freqs and "buy" in freqs and "movie" in freqs):
							for f in freqs:
								if f in self.gSearchFreq:
									found = True
									break
					if found:
						con.append(c)

				for rc in con:
					if rc in post:
						found = False
						if entities is not None:
							for e in entities:
								if e['text'] == rc:
									if e['type'] == "Company" or e['type'] == "Facility":
										found = True
										org.append(rc)

									if e['type'] == "Location":
										found = True
										location.append(rc)
						if not found:
							relConcepts.append(rc)

				title = self.findTitleInQuotes(post)
				if self.isArt(title):
					relConcepts.append(title)

				postDict['SUBJECTS'] = relConcepts
				postDict['ORG'] = org
				postDict['LOCATION'] = location

			if categories is not None:
				for c in categories:
					if c[1] == self.categoryType and len(c) > 2:
						relCategories.append(c[len(c)-1])
				if len(relConcepts) != 0:
					postDict['TYPE'] = relCategories

		return postDict

	def findSubject(self, post):
		postDoc = self.nlp(post)
		postDict = {}
		subject = []
		types = []
		org = []
		location = []

		if self.api.nlu(post):
			categories = self.api.getCategoriesNoRelevance2()
			concepts = self.api.getConcepts()
			entities = self.api.getEntities()
			relCategories = []
			relConcepts = []

			if concepts is not None:
				found = False
				con = []
				for c in concepts:
					freqs = self.gsearch.search(c)
					if freqs is not None:
						if not ("online" in freqs and "buy" in freqs and "movie" in freqs):
							for f in freqs:
								if f in self.gSearchFreq:
									found = True
									break
					if found:
						con.append(c)

				for rc in con:
					found = False
					if entities is not None:
						for e in entities:
							if e['text'] == rc:
								if e['type'] == "Company" or e['type'] == "Facility":
									found = True
									org.append(rc)

								if e['type'] == "Location":
									found = True
									location.append(rc)
					if not found:
						relConcepts.append(rc)

				title = self.findTitleInQuotes(post)
				if self.isArt(title):
					relConcepts.append(title)

				postDict['SUBJECTS'] = relConcepts
				postDict['ORG'] = org
				postDict['LOCATION'] = location

			if categories is not None:
				for c in categories:
					if c[1] == self.categoryType and len(c) > 2:
						relCategories.append(c[len(c)-1])
				if len(relConcepts) != 0:
					postDict['TYPE'] = relCategories

		return postDict

	def isArt(self, title):
		arts = ["novel", "books", "song", "movies"]
		if title is not None:
			# print("TITLE: ", title)
			freqs = self.gsearch.search(title)
			if freqs is not None:
				for f in freqs:
					if f in arts:
						return True
		return False


	def findTitleInQuotes(self, post):
		result = re.search(""" "(.*)" """, post)
		if result is not None:
			title = result.group(1)
		else:
			title = None
		return title

	def extractStory(self, story):
		storyDoc = self.nlp(story)
		# print("ISTORY: ", storyDoc)
		storyDict = {}
		for token in storyDoc:

			if token.pos_ == "VERB":

				if token.text == "shared":
					storyDict['ACTION'] = "Shared"
					result = re.search("shared (.*)'s", story)
					types = []
					if result is not None:
						storyPage = result.group(1)

						# REMOVE "MEME" WORD
						storyPage = storyPage.replace('Meme', '')
						storyPage = storyPage.replace('Memes', '')
						storyPage = storyPage.replace('meme', '')
						storyPage = storyPage.replace('memes', '')

						storyDict['PAGE'] = storyPage
						freqs = self.gsearch.search(storyPage)
						if freqs is not None:
							if not ("online" in freqs and "buy" in freqs and "movie" in freqs):
								for f in freqs:
									if f in self.gSearchFreq:
										types.append(f)

						# FIND FANDOM
						pageDoc = self.nlp(storyPage)
						for tok in pageDoc:
							fandom = self.fandomDic.lookup(tok.text)
							if fandom is not None:
								storyDict["FANDOM"] = tok.text
								storyDict["FANOF"] = fandom['FanOf']
								freqs = self.gsearch.search(fandom['FanOf'][0])
								if freqs is not None:
									if not ("online" in freqs and "buy" in freqs and "movie" in freqs):
										for f in freqs:
											if f in self.gSearchFreq:
												types.append(f)

						storyDict['TYPES'] = types

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