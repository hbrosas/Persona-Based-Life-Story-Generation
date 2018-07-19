from context.foodextract import FoodieExtractor
from context.fanextract import FanExtractor
from context.sportextract import SportExtractor
from context.gameextract import GameExtractor
from context.asstypes import AssTypeInfo

"""
	Story [SUPPORT]: 
		To get the action if there's no action in sentiment

	Post [SUPPORT]: 
		To get the subject
		What topic is subject
		What/Whom the user is referring to
		Get the location or organization of the subject

	Sentiment [MAIN]:
		User's sentiment
		User's post
"""

class ContextUnderstanding:

	asstypeinfo = AssTypeInfo()
	foodie = FoodieExtractor()
	fan = FanExtractor()
	sport = SportExtractor()
	game = GameExtractor()

	def getContext(self, persona, cleaned, profile):
		assertions = []
		ctr = 1

		if persona == "The Foodie" or persona == "The Fangirl/Fanboy":
			for post in cleaned:
				person = profile.name
				if persona == "The Foodie":
					ass = self.foodie.foodieExtract(post, persona, person)
					asserts = self.asstypeinfo.getAssertion(post.label, ass)
					for a in asserts:
						assertions.append(a)
				if persona == "The Fangirl/Fanboy":
					ass = self.fan.fanExtract(post, persona, person)
					asserts = self.asstypeinfo.getAssertion(post.label, ass)
					for a in asserts:
						assertions.append(a)
				print("CONTEXT: ", ctr, " of ", len(cleaned))
				ctr += 1

		elif persona == "The Sports Fanatic":
			assertions = self.sport.sportExtract(cleaned, persona, profile.name)

		elif persona == "The Gamer":
			assertions = self.game.gameExtract(cleaned, persona, profile.name)

		return assertions

