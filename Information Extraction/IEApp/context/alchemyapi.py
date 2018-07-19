import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, RelationsOptions, SemanticRolesOptions, SentimentOptions, CategoriesOptions
import re

class AlchemyAPI:

	natural_language_understanding = None
	data = None

	def __init__(self):
		self.natural_language_understanding = NaturalLanguageUnderstandingV1(
			username= "ff610004-4b7a-4e65-a2cd-6dbed912d487",
  			password= "7lU17HCPOXKX",
			version='2018-03-19'
		)

	def nlu(self, query):
		try:
			response = self.natural_language_understanding.analyze(
				text=query,
				features=Features(
					entities=EntitiesOptions(
						emotion=False,
						sentiment=False
					),
					keywords=KeywordsOptions(
						emotion=False,
						sentiment=False
					),
					concepts=ConceptsOptions(),
					relations=RelationsOptions(),
					semantic_roles=SemanticRolesOptions(),
					sentiment=SentimentOptions(),
					categories=CategoriesOptions()
				)
			)

			self.data = json.loads(json.dumps(response, indent=2))
			# print(json.dumps(response, indent=2))
			return True
		except:
			return False

	def getEntities(self):
		try:
			if not self.data == None:
				return self.data['entities']
			else:
				return []
		except:
			return []

	def getKeywords(self):
		try:
			if not self.data == None:
				relevant = []
				if not len(self.data['keywords']) == 0 and self.data is not None:
					for k in self.data['keywords']:
						if k['relevance'] > 0.50:
							relevant.append(k['text'])
				return relevant
			else:
				return []
		except:
			return []

	def getKeywordsNoRelevance(self):
		try:
			if not self.data == None:
				relevant = []
				if "keywords" in self.data:
					if not len(self.data['keywords']) == 0:
						for k in self.data['keywords']:
							relevant.append(k['text'])
					return relevant
				else:
					return []
			else:
				return []
		except:
			return []

	def getConcepts(self):
		try:
			if not self.data == None:
				concepts = []
				if "concepts" in self.data:
					if not len(self.data['concepts']) == 0:
						for c in self.data['concepts']:
							concepts.append(c['text'])
						return concepts
					# print(self.data['concepts'])
				else:
					return []
			else:
				return []
		except:
			return []

	def getConceptsRelevance(self):
		try:
			if not self.data == None:
				concepts = []
				if "concepts" in self.data:
					if not len(self.data['concepts']) == 0:
						for c in self.data['concepts']:
							if c['relevance'] > 0.85:
								concepts.append(c['text'])
						return concepts
					# print(self.data['concepts'])
				else:
					return []
			else:
				return []
		except:
			return []

	def getRelations(self):
		try:
			if not self.data == None:
				return self.data['relations'] 
				# print(self.data['relations'])
			else:
				return []
		except:
			return []

	def getSemanticRoles(self):
		try:
			if not self.data == None:
				return self.data['semantic_roles']
			else:
				return []
		except:
			return []

	def getSentiment(self):
		try:
			if not self.data == None:
				if self.data['sentiment']['document']['score'] == 0.0:
					return "neutral"
				else:
					return self.data['sentiment']['document']['label']
			else:
				return "neutral"
		except:
			return "neutral"

	def getCategories(self, query):
		categories = []
		try:
			if not self.data == None:
				if "categories" in self.data:
					if not len(self.data['categories']) == 0:
						for c in self.data['categories']:
							heirarchy = []
							if c['score'] >= 0.75:
								heirarchy = c['label'].split("/")
								# print("heirarchy: ", heirarchy)
								if not len(heirarchy) == 0:
									if query in heirarchy:
										categories.append(heirarchy[(len(heirarchy)-1)])
				else:
					return []
		except:
			categories = []

		return categories

	def getCategoriesNoRelevance(self):
		try:
			if not self.data == None:
				if "categories" in self.data:
					return self.data['categories']
				else:
					return []
			else:
				return []
		except:
			return []

	def getCategoriesNoRelevance2(self):
		try:
			if not self.data == None:
				categories = []
				if "categories" in self.data:
					for c in self.data['categories']:
						categories.append(c['label'].split("/"))
					return categories
				else:
					return []
			else:
				return []
		except:
			return []