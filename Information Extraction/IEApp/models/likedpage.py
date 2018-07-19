class LikedPage(object):
	id = 0
	fbID = ""
	liked_page = ""
	category = ""
	title = ""
	description = ""

	def __init__(self, id, fbID, liked_page, category):
		self.id = id
		self.fbID = fbID
		self.liked_page = liked_page
		self.category = category