class Event(object):
	id = 0
	fbID = ""
	original_event = ""
	event = ""
	rsvp = ""

	def __init__(self, id, fbID, original_event):
		self.id = id
		self.fbID = fbID
		self.original_event = original_event