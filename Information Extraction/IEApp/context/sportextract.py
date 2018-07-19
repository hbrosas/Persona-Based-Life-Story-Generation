from context.asstypes import AssTypeInfo
from context.conceptnet import ConceptNet
from context.dbpedia import DBPedia
from context.googlesearch import GoogleSearch
from context.alchemyapi import AlchemyAPI
from prepros.dictionaries.fan_dic import FanDomDictionary
from prepros.dictionaries.sports_team_dic import SportsTeamsDictionary
from prepros.dictionaries.sports_legends import SportsLegendsDictionary
from prepros.dictionaries.sports_events import SportsEventsDictionary
import spacy
import re

class SportExtractor:

	asstypeinfo = AssTypeInfo()
	nlp = spacy.load('en')
	conceptnet = ConceptNet()
	gsearch = GoogleSearch()
	api = AlchemyAPI()
	dbpedia = DBPedia()
	sportsTeamDic = SportsTeamsDictionary()
	sportsLegends = SportsLegendsDictionary()
	sportsLeagues = SportsEventsDictionary()
	categoryType = "sports"
	person = ""
	persona = ""
	sports = []
	athletes = {}
	teams = {}
	leagues = {}
	subjects = {} # SUBJECT - FREQUENCY
	sportsTypes = ["archery", "auto racing", "badminton", "baseball", "basketball", "bicycling", "bicycling", "billiards", "boat racing", "bobsled", "bodybuilding", "bowling", "boxing", "canoeing and kayaking", "cheerleading", "climbing", "cricket", "curling", "diving","dogsled", "fencing","fishing", "football", "go kart", "golf", "gymnastics", "handball", "hockey", "horse racing", "horses", "hunting and shooting", "martial arts","motorcycling", "olympics", "paintball","parachuting", "polo", "rodeo", "rowing", "rugby", "running and jogging", "sailing", "scuba diving", "skateboarding","skating", "skiing", "snowboarding", "soccer", "softball", "sports news", "surfing and bodyboarding", "swimming", "table tennis and ping pong", "tennis", "trekking", "tennis", "volleyball", "wakeboarding", "walking", "water polo", "weightlifting", "wrestling", "windsurfing"]

	def sportExtract(self, posts, persona, person):
		self.person = person
		self.persona = persona
		ctr = 1
		storyDict = {} # ACTION, PAGE, TAGGED, ORGANIZATION

		# For Each Cleaned Posts
		for p in posts:
			storyDict = self.extractStory(p.story)

			# ASSERTION TYPE: PLAY
			cleaned = self.combinePost(p)
			self.determineSport(cleaned)

			# ASSERTION TYPE: SHARED ABOUT
			storySearch = "shared " + storyDict['PAGE']
			self.getSubjects(storySearch)

			if not p.post == "":
				self.getSubjects(p.post)

			# ASSERTION TYPE: FANOF
			if not p.sentiment == "":
				sentiment = self.getSentiment(p.sentiment)
				if sentiment == "positive" or sentiment == "neutral":
					self.extractFanOf(p.sentiment)

			# ASSERTION TYPE: LEAGUES
			self.searchLeague(storyDict['PAGE'])

			print("CONTEXT: ", ctr, " of ", len(posts))
			ctr += 1


		# print("SPORTS: ", self.sports)
		# print("")
		# print("SUBJECTS: ", self.subjects)
		# print("")
		# print("ATHLETES: ", self.athletes)
		# print("")
		# print("TEAMS: ", self.teams)
		# print("")
		# print("LEAGUES: ", self.leagues)

		assertions = self.generateAssertions()
		return assertions

	def generateAssertions(self):
		assertions = []

		for s in self.sports:
			assertions.append({
				'type' : "Play",
				'values' : {
					"Person" : self.person,
					"Sport" : s,
				},
				'persona' : "The Sports Fanatic",
			})

		for sub in self.subjects.values():
			assertions.append({
				'type' : "Shared_About",
				'values' : {
					"Person" : self.person,
					"Action" : "Shared About",
					"Subject" : sub["SUBJECT"],
					"Frequency" : sub["FREQUENCY"],
					"Sport" : sub["SPORT"],
				},
				'persona' : "The Sports Fanatic",
			})

		for t in self.teams.values():
			assertions.append({
				'type' : "Supports",
				'values' : {
					"Person" : self.person,
					"Action" : "Supports",
					"Team" : t["TEAM"],
					"Sport" : t["SPORT"],
				},
				'persona' : "The Sports Fanatic",
			})

		for a in self.athletes.values():
			assertions.append({
				'type' : "FanOf",
				'values' : {
					"Person" : self.person,
					"Athlete" : a["ATHLETE"],
					"Sport" : a["SPORT"],
				},
				'persona' : "The Sports Fanatic",
			})

		for l in self.leagues.values():
			assertions.append({
				'type' : "League",
				'values' : {
					"Person" : self.person,
					"League" : l['LEAGUE'],
					"Sport" : l['SPORT'],
				},
				'persona' : "The Sports Fanatic",
			})

		return assertions

	def searchLeague(self, page):
		pageDoc = self.nlp(page)

		for token in pageDoc:
			l = self.sportsLeagues.lookup(token.text)
			if l is not None:
				if not token.text in self.leagues:
					values = {}
					values['LEAGUE'] = token.text
					values['SPORT'] = l["SPORT"]
					self.leagues[token.text] = values

	def extractFanOf(self, statement):
		# Get Person Entity
		person = []
		if self.api.nlu(statement):
			entities = self.api.getEntities()
			if not len(entities) == 0:
				for e in entities:
					if e['type'] == "Person":
						person.append(e['text'])

		for p in person:
			isRelated = False
			freqs = self.gsearch.search(p)
			if freqs is not None:
				for f in freqs:
					if f in self.sportsTypes:
						isRelated = True
						break
			
			if isRelated:
				tokens = freqs[0] + " " + freqs[1] + " " + freqs[2] + " " + freqs[3] + " " + freqs[4]
				if self.api.nlu(tokens):
					concepts = self.api.getConceptsRelevance()
					categories = self.api.getCategories(self.categoryType)
					if not len(concepts) == 0:
						for c in concepts:
							team = self.sportsTeamDic.lookup(c)
							if team is not None:
								self.addToTeam(c, categories)

							legend = self.sportsLegends.lookup(c)
							if legend is not None:
								self.addToFanOf(c, categories)

	def addToTeam(self, team, categories):
		if not team in self.teams:
			values = {}
			values['TEAM'] = team
			values['SPORT'] = categories
			self.teams[team] = values

	def addToFanOf(self, fanOf, categories):
		if not fanOf in self.athletes:
			values = {}
			values['ATHLETE'] = fanOf
			values['SPORT'] = categories
			self.athletes[fanOf] = values

	def getSentiment(self, statement):
		if self.api.nlu(statement):
			return self.api.getSentiment()

	def getSubjects(self, statement):
		inCategory = False
		isRelated = False

		if self.api.nlu(statement):
			# Check if category exists
			categories = self.api.getCategories(self.categoryType)
			if not len(categories) == 0:
				inCategory = True

			# Get Concepts
			concepts = self.api.getConceptsRelevance()
			categories = self.api.getCategories(self.categoryType)
			if concepts is not None:
				for c in concepts:
					if c in self.subjects:
						# Mentioned
						freq = self.subjects[c]["FREQUENCY"]
						self.subjects[c]["FREQUENCY"] += 1
					else:
						# Not mentioned yet
						isRelated = False
						types = []
						freqs = self.gsearch.search(c)
						if freqs is not None:
							for f in freqs:
								if f in self.sportsTypes:
									isRelated = True
									types.append(f)

						if isRelated:
							values = {}
							values['SUBJECT'] = c
							values['FREQUENCY'] = 1
							values['SPORT'] = types
							self.subjects[c] = values

	def combinePost(self, p):
		cleaned = ""
		if not p.story == "":
			cleaned += p.story
		if not p.post == "":
			cleaned += p.post + " "
		if not p.sentiment == "":
			cleaned += p.sentiment + " "
		return cleaned

	def determineSport(self, post):
		if self.api.nlu(post):
			categories = self.api.getCategories(self.categoryType)
			if not len(categories) == 0:
				for c in categories:
					if not c in self.sports:
						self.sports.append(c)

	def extractStory(self, story):
		storyDoc = self.nlp(story)
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

