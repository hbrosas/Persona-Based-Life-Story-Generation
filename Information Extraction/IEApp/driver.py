from database import Database
from prepros.clean import Clean
from models.post import Post
from context.googlesearch import GoogleSearch
from context.conceptnet import ConceptNet
from context.dbpedia import DBPedia
from context.contextunderstanding import ContextUnderstanding
from context.alchemyapi import AlchemyAPI
from context.likedpagesevents import LikedPagesEvents
from filemanager import FileManager
import nltk

class Driver:

	# Main Function
	def init(persona, name, data):
		print("")
		posts = []
		print("DATABASE: Connecting to the database")
		db = Database()
		print("DATABASE: Successfully connected to the database")
		print("EXTRACTION: Getting your personal information")
		profile = db.getProfile(name)
		print("EXTRACTION: profile successfully retrieved")

		if data == 1:
			print("EXTRACTION: Getting labelled posts")
			posts = db.getPostsByLabel(persona, profile.tablename + "_posts")
			print("EXTRACTION: Labelled posts successfully retrieved")
			cleaner = Clean()
			print("PRE-PROCESSING: Preparing for cleaning stage")
			cleaned_posts = cleaner.cleanData(posts, profile)
			print("PRE-PROCESSING: Posts successfully cleaned")
			print("CONTEXT: Getting ready for context understanding")
			contexter = ContextUnderstanding()
			print("CONTEXT: Currently on context understanding")
			assertions = contexter.getContext(persona, cleaned_posts, profile)
			print("CONTEXT: Successfully extracted all the assertion types")
			print("CONTEXT: You've got ", len(assertions), " number of assertions")
			# print(assertions)

			if persona == "The Fangirl/Fanboy":
				filename = profile.tablename + "_fangirlfanboy_posts" 
			elif persona == "The Gamer":
				filename = profile.tablename + "_gamer_posts" 
			elif persona == "The Sports Fanatic":
				filename = profile.tablename + "_sports_posts" 
			elif persona == "The Foodie":
				filename = profile.tablename + "_foodie_posts" 

			print("SAVING: Currently saving your assertions...")
			FileManager.writeFile(assertions, filename)
			print("SAVING: Successfully saved your assertions")

		elif data == 2:
			print("EXTRACTION: Getting labelled likes")
			likes = db.getLikesByLabel(persona, profile.tablename + "_likes")
			print("EXTRACTION: Labelled posts successfully retrieved")
			print("BUILDING: Currently on building assertions for liked pages")
			lpe = LikedPagesEvents()
			assertions = lpe.extractLikedPages(likes, persona)
			print("CONTEXT: Successfully extracted all the assertion types")
			print("CONTEXT: You've got ", len(assertions), " number of assertions")
			# print(assertions)

			if persona == "The Fangirl/Fanboy":
				filename = profile.tablename + "_fangirlfanboy_likes" 
			elif persona == "The Gamer":
				filename = profile.tablename + "_gamer_likes" 
			elif persona == "The Sports Fanatic":
				filename = profile.tablename + "_sports_likes" 
			elif persona == "The Foodie":
				filename = profile.tablename + "_foodie_likes" 

			print("SAVING: Currently saving your assertions...")
			FileManager.writeFile(assertions, filename)
			print("SAVING: Successfully saved your assertions")


		elif data == 3:
			print("EXTRACTION: Getting labelled events")
			events = db.getEventsByLabel(persona, profile.tablename + "_events")
			print("EXTRACTION: Labelled posts successfully retrieved")
			print("BUILDING: Currently on building assertions for events")
			lpe = LikedPagesEvents()
			assertions = lpe.extractEvents(events, persona)
			print("CONTEXT: Successfully extracted all the assertion types")
			print("CONTEXT: You've got ", len(assertions), " number of assertions")
			# print(assertions)

			if persona == "The Fangirl/Fanboy":
				filename = profile.tablename + "_fangirlfanboy_events" 
			elif persona == "The Gamer":
				filename = profile.tablename + "_gamer_events" 
			elif persona == "The Sports Fanatic":
				filename = profile.tablename + "_sports_events" 
			elif persona == "The Foodie":
				filename = profile.tablename + "_foodie_events" 

			print("SAVING: Currently saving your assertions...")
			FileManager.writeFile(assertions, filename)
			print("SAVING: Successfully saved your assertions")

		

	# def init2():
	# 	query = "Teejay Marquez"
	# 	gs = GoogleSearch()
	# 	# print(gs.searchGoogleAPI(query))
	# 	print(gs.search(query))

	# def init3():
	# 	query = "volleyball"
	# 	gs = ConceptNet()
	# 	gs.search(query)		

	# def init4():
	# 	api = AlchemyAPI()
	# 	api.nlu("bby mochi? ?")

	# def init5():
	# 	dbpedia = DBPedia()
	# 	dbpedia.getHypernym("isaw")

	# # 1 for Posts, 2 for Liked Pages, 3 for Events
	persona = "The Fangirl/Fanboy"
	name = "AR QLazaga"
	init(persona, name, 1)
	init(persona, name, 2)
	init(persona, name, 3)

	# init2() # Google Search
	# init3() # ConceptNet
	# init4()
	# init5()

	