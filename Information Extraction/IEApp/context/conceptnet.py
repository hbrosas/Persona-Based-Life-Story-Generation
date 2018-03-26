import requests

class ConceptNet:

	def search(self, query):
		req = "http://api.conceptnet.io/c/en/" + query
		obj = requests.get(req).json()
		for e in obj['edges']:
			if e['start']['language'] == "en":
				print(e['start']['label'] + " - " + e['rel']['label'] + " - " + e['end']['label'])