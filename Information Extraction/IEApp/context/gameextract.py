from context.asstypes import AssTypeInfo
from context.conceptnet import ConceptNet
from context.dbpedia import DBPedia
from context.googlesearch import GoogleSearch
from context.alchemyapi import AlchemyAPI
from prepros.dictionaries.game_dic import GameDictionary
from prepros.dictionaries.game_team_dic import GameTeamsDictionary
import spacy
import re

class GameExtractor:

	asstypeinfo = AssTypeInfo()
	nlp = spacy.load('en')
	conceptnet = ConceptNet()
	gsearch = GoogleSearch()
	api = AlchemyAPI()
	dbpedia = DBPedia()
	game_dic = GameDictionary()
	game_team = GameTeamsDictionary()
	person = ""
	persona = ""

	games = {} # GAME, TYPE
	teams = {} # TEAM, GAMES, COUNTRY
	activitiesDone = [] # ACTIVITY, GAME, ACTION

	subjects = {} # SUBJECT - FREQUENCY
	peopleEntities = ["gamer", "streamer"]
	terms = ["gaming", "game"]
	eventTerms = ["festival", "fest", "concert", "cup", "tournament"]
	activitiesTerms = ["giveaway", "giveaways", "livestreaming", "livestreams", "livestream"]

	def gameExtract(self, posts, persona, person):
		self.person = person
		self.persona = persona
		ctr = 1
		storyDict = {} # ACTION, PAGE, TAGGED, ORGANIZATION

		# For Each Cleaned Posts
		for p in posts:
			storyDict = self.extractStory(p.story)

			# ASSERTION TYPE: PLAY [STORY]
			self.playOnStory(storyDict)
			self.playOnPost(p.post)
			self.playOnSentiment(p.sentiment)

			# ASSERTION TYPE: TEAMS [FANOF, TYPE (Streamer, Gamer, etc.)]
			self.teamOnPost(p.post)
			self.teamOnStory(storyDict)
			self.teamOnSentiment(p.sentiment)

			# ASSERTION TYPE: Activities [ACTIVITY, ACTION, GAME]
			self.activities(p.post)

			print("CONTEXT: ", ctr, " of ", len(posts))
			ctr += 1

		# print("PLAY GAMES: ", self.games)
		# print("SUPPORT TEAMS: ", self.teams)
		# print("ACTIVITIES: ", self.activitiesDone)
		assertions = self.generateAssertions()
		return assertions

	def activities(self, post):
		doc = self.nlp(post)
		activitiesFound = []
		gamesFound = []
		for token in doc:
			# Find if activity mentioned
			if token.text in self.activitiesTerms:
				activitiesFound.append(token.text)

			# Find Related Game
			key = self.game_dic.lookupAbbr(token.text)
			if key is not None:
				gamesFound.append(key['NAME'])
			else:
				key = self.game_dic.lookup(token.text)
				if key is not None:
					gamesFound.append(key['NAME'])

		# ["giveaway", "giveaways", "livestreaming", "livestreams", "livestream"]
		for af in activitiesFound:
			for g in gamesFound:
				if af.lower() == "giveaway" or af.lower() == "giveaways":
					if not self.activityExists(af, g):
						self.addToActivities(af, g, "join")
				elif af.lower() == "livestreaming" or af.lower() == "livestreams"  or af.lower() == "livestream":
					if not self.activityExists(af, g):
						self.addToActivities(af, g, "watch")

	def activityExists(self, af, g):
		same = False
		for a in self.activitiesDone:
			if a['ACTIVITY'] == af and a['GAME'] == g:
				same = True
				break
		return same

	def teamOnStory(self, storyDict):
		doc = self.nlp(storyDict['PAGE'])
		# Whole post
		whole = self.game_team.lookup(storyDict['PAGE'])
		if whole is not None:
			self.addToTeams(whole['NAME'], whole['Categories'], whole['Country'])
		else:
			# Per Token
			for token in doc:
				key = self.game_team.lookupAbbr(token.text)
				if key is not None:
					self.addToTeams(key['NAME'], key['Categories'], key['Country'])
				else:
					key = self.game_team.lookup(token.text)
					if key is not None:
						self.addToTeams(key['NAME'], key['Categories'], key['Country'])

	def teamOnSentiment(self, sentiment):
		doc = self.nlp(sentiment)
		# print("DOC: ", doc)
		for token in doc:
			key = self.game_team.lookupAbbr(token.text)
			if key is not None:
				self.addToTeams(key['NAME'], key['Categories'], key['Country'])
			else:
				key = self.game_team.lookup(token.text)
				if key is not None:
					self.addToTeams(key['NAME'], key['Categories'], key['Country'])

	def teamOnPost(self, post):
		doc = self.nlp(post)
		# print("DOC: ", doc)
		for token in doc:
			key = self.game_team.lookupAbbr(token.text)
			if key is not None:
				self.addToTeams(key['NAME'], key['Categories'], key['Country'])
			else:
				key = self.game_team.lookup(token.text)
				if key is not None:
					self.addToTeams(key['NAME'], key['Categories'], key['Country'])

	def playOnSentiment(self, sentiment):
		doc = self.nlp(sentiment)
		for token in doc:
			key = self.game_dic.lookupAbbr(token.text)
			if key is not None:
				self.addToGames(key['NAME'], key['Type'])
			else:
				key = self.game_dic.lookup(token.text)
				if key is not None:
					self.addToGames(key['NAME'], key['Type'])

	def playOnPost(self, post):
		doc = self.nlp(post)
		for token in doc:
			key = self.game_dic.lookupAbbr(token.text)
			if key is not None:
				self.addToGames(key['NAME'], key['Type'])
			else:
				key = self.game_dic.lookup(token.text)
				if key is not None:
					self.addToGames(key['NAME'], key['Type'])

	def playOnStory(self, storyDict):
		doc = self.nlp(storyDict['PAGE'])
		# Whole post
		whole = self.game_dic.lookup(storyDict['PAGE'])
		if whole is not None:
			self.addToGames(whole['NAME'], whole['Type'])
		else:
			# Per Token
			for token in doc:
				key = self.game_dic.lookupAbbr(token.text)
				if key is not None:
					self.addToGames(key['NAME'], key['Type'])
				else:
					key = self.game_dic.lookup(token.text)
					if key is not None:
						self.addToGames(key['NAME'], key['Type'])

	def addToActivities(self, activity, game, action):
		values = {}
		values['ACTIVITY'] = activity
		values['GAME'] = game
		values['ACTION'] = action
		self.activitiesDone.append(values)

	def addToGames(self, gamee, typee):
		if not gamee in self.games:
			values = {}
			values['GAME'] = gamee
			values['TYPE'] = typee
			self.games[gamee] = values

	def addToTeams(self, team, games, country):
		if not team in self.teams:
			values = {}
			values['TEAM'] = team
			values['GAMES'] = games
			values['COUNTRY'] = country
			self.teams[team] = values

	def extractStory(self, story):
		storyDoc = self.nlp(story)
		# print("ISTORYA: ", storyDoc)
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

				# If is playing
				if token.text == "playing":
					for child in token.children:
						if child.dep_ == "dobj":
							self.games = child.text

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

	#################################################################

	def generateAssertions(self):
		assertions = []

		# games = {} # GAME, TYPE
		# teams = {} # TEAM, GAMES, COUNTRY
		# activitiesDone = [] # ACTIVITY, GAME, ACTION

		for g in self.games.values():
			assertions.append({
				'type' : "Play",
				'values' : {
					"Person" : self.person,
					"Game" : g["GAME"],
					"Type" : g["TYPE"],
				},
				'persona' : "The Gamer",
			})

		for t in self.teams.values():
			assertions.append({
				'type' : "Supports",
				'values' : {
					"Person" : self.person,
					"Team" : t["TEAM"],
					"Game" : t["GAMES"],
					"Country" : t["COUNTRY"],
				},
				'persona' : "The Gamer",
			})

		for act in self.activitiesDone:
			assertions.append({
				'type' : "Activity",
				'values' : {
					"Person" : self.person,
					"Activity" : act['ACTIVITY'],
					"Action" : act['ACTION'],
					"Game" : act['GAME'],
				},
				'persona' : "The Gamer",
			})

		return assertions

