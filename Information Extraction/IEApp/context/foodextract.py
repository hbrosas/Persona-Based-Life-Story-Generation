from context.asstypes import AssTypeInfo
from context.conceptnet import ConceptNet
from context.dbpedia import DBPedia
from context.googlesearch import GoogleSearch
from context.alchemyapi import AlchemyAPI
import spacy
import re

class FoodieExtractor:

	asstypeinfo = AssTypeInfo()
	nlp = spacy.load('en')
	conceptnet = ConceptNet()
	gsearch = GoogleSearch()
	api = AlchemyAPI()
	dbpedia = DBPedia()
	person = ""

	def foodieExtract(self, post, persona, person):
		self.person = person
		people_mentioned = post.person
		hashtags = post.hashtags
		mentions = post.mentions
		assertions = [] # Append here all values of assertions
		sentiment = self.nlp(post.sentiment)

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
		base_data['Date'] = post.date
		base_data['Time'] = post.time

		# Check if it has sentiment
		if not sentiment.text == "":
			token_dict = {}
			for token in sentiment:
				values = {}
				values['dep'] = token.dep_
				values['pos'] = token.pos_
				values['head'] = token.head.text
				values['lemma'] = token.head.lemma_
				values['head_pos'] = token.head.pos_
				values['children'] = [child for child in token.children]
				token_dict[token.text] = values

			for chunk in sentiment.noun_chunks:
				text = chunk.text
				root_dep = chunk.root.dep_
				root_head = chunk.root.head.text

				if root_dep == "advmod" or root_dep == "":
					# Describes Adjective
					head = token_dict[root_head]['head']
					if token_dict[head]['head_pos'] == "ADJ":
						base_data['Description'] = token_dict[root_head]['head']
				elif root_dep == "pobj":
					head = token_dict[root_head]['head']
					lemma = token_dict[root_head]['lemma']
					if token_dict[head]['head_pos'] == "VERB":
						base_data['Action'] = lemma

			
			sentPeople = self.getPersonMentioned()
			if not sentPeople == None:
				for p in sentPeople:
					if not p == person and not p in friends:
						friends.append(p)
			base_data['Tagged_Friends'] = friends

			# If not post
			if post.post == "":
				# Case 3: Has Sentiment; No Post; No Story
				if post.story == "":
					if self.api.nlu(sentiment.text):
						keywords = self.api.getKeywords()
						foods = self.getFood(keywords)
						if not len(foods) == 0:
							for food in foods:
								# Copy Base Dict
								data = base_data.copy()

								# Set Food
								data['Food'] = food

								# Get Food Type/Categories
								data['Type'] = self.getFoodType(food)

								# Get Organization & Location
								data['Organization'], data['Location'] = self.getPlace_Organization()

								# Get Sentiment
								sent = self.api.getSentiment()
								if not sent == None:
									data['Sentiment_Class'] = sent
									data['Sentiment'] = sentiment.text

								assertions.append(data)
				else:
					# Case 4: Has Sentiment; No Post; Has Story
					story_action, story_org, story_location, story_person = self.extractStoryInformation(post.story)
					if self.api.nlu(sentiment.text):
						keywords = self.api.getKeywords()
						foods = self.getFood(keywords)
						if not len(foods) == 0:
							for food in foods:
								# Copy Base Dict
								data = base_data.copy()

								# Set Food
								data['Food'] = food

								# Get Food Type/Categories
								data['Type'] = self.getFoodType(food)

								data['Organization'] = story_org
								data['Tagged_Friends'] = story_person
								data['Location'] = story_location

								if data['Action'] == "":
									data['Action'] = story_action

								# Get Sentiment
								sent = self.api.getSentiment()
								if not sent == None:
									data['Sentiment_Class'] = sent
									data['Sentiment'] = sentiment.text

								assertions.append(data)
						else:
							# Copy Base Dict
							data = base_data.copy()

							data['Organization'] = story_org
							data['Tagged_Friends'] = story_person
							data['Location'] = story_location
							data['Action'] = "Went to"

							assertions.append(data)
					else:
						# Copy Base Dict
						data = base_data.copy()

						data['Organization'] = story_org
						data['Tagged_Friends'] = story_person
						data['Location'] = story_location
						data['Action'] = "Went to"

						assertions.append(data)

			else:
				# Has everything
				story_action, story_org, story_location, story_person = self.extractStoryInformation(post.story)
				post_food, post_org= self.extractFoodPostInformation(post.post)

				if not len(story_person) == 0:
					for p in story_person:
						if not p == person and not p in friends:
							friends.append(p)
					base_data['Tagged_Friends'] = friends

				if self.api.nlu(sentiment.text):
					# Food
					keywords = self.api.getKeywords()
					foods = self.getFood(keywords)
					if not len(foods) == 0:
						for food in foods:
							# Copy Base Dict
							data = base_data.copy()

							# Set Food
							data['Food'] = food

							# Get Food Type/Categories
							data['Type'] = self.getFoodType(food)

							# Get Organization & Location
							data['Organization'], data['Location'] = self.getPlace_Organization()

							if data['Organization'] == None:
								if len(post_org) == 0:
									data['Organization'] = story_org
								else:
									data['Organization'] = post_org

							if data['Location'] == None:
								data['Location'] = story_location

							if data['Action'] == "":
								data['Action'] == story_action

							# Get Sentiment
							sent = self.api.getSentiment()
							if not sent == None:
								data['Sentiment_Class'] = sent
								data['Sentiment'] = sentiment.text

							assertions.append(data)
					else:
						if not len(post_food) == 0:
							for food in post_food:
								# Copy Base Dict
								data = base_data.copy()

								# Set Food
								data['Food'] = food

								# Get Food Type/Categories
								data['Type'] = self.getFoodType(food)

								# Get Organization & Location
								data['Organization'], data['Location'] = self.getPlace_Organization()

								if data['Organization'] == None:
									if len(post_org) == 0:
										data['Organization'] = story_org
									else:
										data['Organization'] = post_org

								if data['Location'] == None:
									data['Location'] = story_location

								if data['Action'] == "":
									data['Action'] == story_action

								assertions.append(data)
						else:
							# No Found Foods
							data = base_data.copy()

							# Get Organization & Location
							data['Organization'], data['Location'] = self.getPlace_Organization()

							if data['Organization'] == None:
								if len(post_org) == 0:
									data['Organization'] = story_org
								else:
									data['Organization'] = post_org

							if data['Location'] == None:
								data['Location'] = story_location

							if data['Action'] == "":
								data['Action'] == story_action

							assertions.append(data)
		else:
			# Case 1 (No Sentiment; Has Post; Has Story)
			if not post.post == "":
				story_action, story_org, story_location, story_person = self.extractStoryInformation(post.story)
				post_food, post_org= self.extractFoodPostInformation(post.post)

				if not len(post_food) == 0:
					for food in post_food:
						# Copy Base Dict
						data = base_data.copy()

						# Set Food
						data['Food'] = food

						# Get Food Type/Categories
						data['Type'] = self.getFoodType(food)

						# Get Organization & Location
						if len(post_org) == 0:
							data['Organization'] = story_org
						else:
							data['Organization'] = post_org

						if data['Location'] == None:
							data['Location'] = story_location

						if data['Action'] == "":
							data['Action'] == story_action

						assertions.append(data)
				else:
					# No Found Foods
					data = base_data.copy()

					# Get Organization & Location
					if len(post_org) == 0:
						data['Organization'] = story_org
					else:
						data['Organization'] = post_org

					if data['Location'] == None:
						data['Location'] = story_location

					if data['Action'] == "":
						data['Action'] == story_action

					assertions.append(data)
			else:
				# Case 2 (No Sentiment; No Post; Has Story)
				data = base_data.copy()
				data['Action'], data['Organization'], data['Location'], story_person = self.extractStoryInformation(post.story)

				if not len(story_person) == 0:
					for p in story_person:
						if not p == person and not p in friends:
							friends.append(p)
					data['Tagged_Friends'] = friends

				assertions.append(data)

		# print(assertions)
		return assertions

	def extractFoodPostInformation(self, post):
		if self.api.nlu(post):
			keywords = self.api.getKeywords()
			foods = self.getFood(keywords)
			orgs, places = self.getPlace_Organization()
			return foods, orgs
		else:
			return [], []
		

	def extractStoryInformation(self, story):
		# print("EXTRACTING STORY INFORMATION")
		org = []
		location = []
		taggedperson = []

		storyDoc = self.nlp(story)
		for token in storyDoc:
			if token.pos_ == "ADP":
				subchild = [child for child in token.children]
				# print("SUBJECT: ", token.text)
				if token.text == "with":
					subtree = subchild[0].subtree
					subtreeArr = [t.text for t in subtree]
					joinedtext = " ".join(subtreeArr)
					# print("CHILDREN: ", joinedtext)
					taggedperson.append(joinedtext)
				if token.text == "at":
					subtree = subchild[0].subtree
					subtreeArr = [t.text for t in subtree]
					joinedtext = " ".join(subtreeArr)
					# print("CHILDREN: ", joinedtext)
					org.append(joinedtext)

		if self.api.nlu(story):
			semanticRoles = self.api.getSemanticRoles()
			entities = self.api.getEntities()

			action = ""

			for s in semanticRoles:
				# Get Action
				action = s['action']['verb']['text']

				for ent in entities:
					if ent['type'] == "Company" or ent['type'] == "Facility":
						org.append(ent['text'])

					if ent['type'] == "Location":
						location.append(ent['text'])

					if ent['type'] == "Person":
						if ent['text'] != self.person: 
							taggedperson.append(ent['text'])

			if action == "share":
				return action, org, [], []
			else:
				return action, org, location, taggedperson
		else:
			return [], org, location, taggedperson

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

	def getFoodType(self, query):
		categories = self.api.getCategories("food and drink")

		if len(categories) == 0:
			doc = self.nlp(query)
			# Find the root word and search
			rootWord = ""
			for token in doc:
				if token.dep_ == "ROOT":
					rootWord = token.text
					break;

			catg = self.dbpedia.searchFoodCategory(rootWord)
			if not len(catg) == 0:
				for c in catg:
					categories.append(c.replace("_", " "))

		return categories

	def getFood(self, keywords):
		foods = []
		for k in keywords:
			doc = self.nlp(k)
			# Find the root word and search
			# print(k)
			rootWord = ""
			for token in doc:
				if token.dep_ == "ROOT":
					rootWord = token.text
					break;

			types = self.dbpedia.getType(rootWord)
			categories = self.dbpedia.searchFoodCategory(rootWord)

			if "Food" in types:
				foods.append(k)
				break
			elif "Lists_of_brand_name_foods" in categories:
				foods.append(k)
				break
			elif "Edible_fruits" in categories:
				foods.append(k)
				break
			elif "Rice" in categories:
				foods.append(k)
				break

		return foods

	def find_root(self, docu):
		for token in docu:
			if token.head is token:
				return token
		return None