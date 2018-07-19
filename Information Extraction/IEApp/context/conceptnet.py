import requests

class ConceptNet:

	def search(self, query):
		req = "http://api.conceptnet.io/c/en/" + query
		obj = requests.get(req).json()
		return obj['edges']

	def getIsTypeOf(self, query):
		results = self.search(query)

		for res in results:
			if res['start']['language'] == "en":
				print(res['start']['label'] + " - " + res['rel']['label'] + " - " + res['end']['label'])