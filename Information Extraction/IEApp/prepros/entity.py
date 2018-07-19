from database import Database
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import spacy

class Entity:

	def isAnEntity(self, token):
		db = Database()
		semrel = db.searchSemRel(token)
		if len(semrel) == 0:
			ent = Entity()
			ent.learn(token)
		
	# def fetchdata(self, url, retry):
	# 	try:
	# 		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	# 		sparql.setQuery(""" PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?label, ?value WHERE {<""" + url + """> ?label ?value} """)
	# 		sparql.setReturnFormat(JSON)
	# 		results = sparql.query().convert()
	# 		return results
	# 	except:
	# 		if(retry == 3):
	# 			return None
	# 		else:
	# 			retry += 1
	# 			results = self.fetchdata(self, url, retry)
	# 			return results

	def doesExists(self, token):
		try:
			tokText = token.capitalize()

			url = "http://dbpedia.org/resource/" + tokText
			# results = self.fetchdata(url, 0)
			sparql = SPARQLWrapper("http://dbpedia.org/sparql")
			sparql.setQuery(""" PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?label, ?value WHERE {<""" + url + """> ?label ?value} """)
			sparql.setReturnFormat(JSON)
			results = sparql.query().convert()

			if len(results["results"]["bindings"]) == 0:
				# Check if ABBREVIATION
				tokText = token.upper()
				url = "http://dbpedia.org/resource/" + tokText
				sparql.setQuery( """ 
				               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

				    			SELECT ?label, ?value
				    			WHERE { <""" + url + """> 
				    				?label ?value }""")
				sparql.setReturnFormat(JSON)
				results = sparql.query().convert()
				# results = self.fetchdata(url, 0)
				if len(results["results"]["bindings"]) == 0:
					return False
				else:
					return True
				# if results is not None:
					
				# else:
				# 	return False
			else: 
				return True
		except:
			return False

		# if results is not None:
			
		# else:
		# 	return False

	def learn(self, token):
		tokText = token.capitalize()
		ent = Entity()
		ent.conceptNet(tokText)
		ent.dbPedia("http://dbpedia.org/resource/" + tokText, tokText)

				
	def conceptNet(self, tokText):
		# ConceptNet
		db = Database()
		req = "http://api.conceptnet.io/c/en/" + tokText
		obj = requests.get(req).json()
		for e in obj['edges']:
			if e['start']['language'] == "en":
				rel = e['rel']['label']
				relId = db.findRelation(rel)
				if not relId == -1:
					db.feedSemRel(relId, e['start']['label'], e['end']['label'])
					# print(e['start']['label'] + " - " + rel + " - " + e['end']['label'])


