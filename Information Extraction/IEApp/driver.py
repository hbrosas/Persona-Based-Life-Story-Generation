from database import Database
from prepros.clean import Clean
from models.post import Post

class Driver:

	# Main Function
	def init():
		posts = []
		db = Database()
		print("EXTRACTION: Getting labelled posts")
		posts = db.getPosts()
		print("EXTRACTION: Labelled posts successfully retrieved")

		cleaner = Clean()
		print("PRE-PROCESSING: Preparing for cleaning stage")
		cleaner.cleanData(posts)

	init()
	