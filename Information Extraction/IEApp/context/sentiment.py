import requests

"""
	api from vivekn - http://sentiment.vivekn.com/docs/api/
"""

class Sentimenter:

	def getSentiment(query):
		response = requests.post("http://sentiment.vivekn.com/api/text/",
                        	data={
                        		"txt": query
                        	}
                    )
		obj = response.json()
		return obj['result']['sentiment']