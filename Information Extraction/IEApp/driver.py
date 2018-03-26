from database import Database
from prepros.clean import Clean
from models.post import Post
from context.googlesearch import GoogleSearch
from context.conceptnet import ConceptNet
import nltk

class Driver:

	# Main Function
	def init(persona):
		posts = []
		db = Database()
		print("EXTRACTION: Getting labelled posts")
		posts = db.getPostsByLabel(persona)
		print("EXTRACTION: Labelled posts successfully retrieved")
		cleaner = Clean()
		print("PRE-PROCESSING: Preparing for cleaning stage")
		cleaner.cleanData(posts)

	def init2():
		query = "DLSU vs ADMU March 17, 2018"
		gs = GoogleSearch()
		gs.search(query)

	def init3():
		query = "volleyball"
		gs = ConceptNet()
		gs.search(query)		

	init("The Sports Fanatic")
	# init2() # Google Search
	# init3() # ConceptNet

	