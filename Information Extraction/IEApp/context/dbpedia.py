from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import spacy
import re

class DBPedia:
	sparql = None
	nlp = spacy.load('en')

	def __init__(self):
		self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		self.sparql.setReturnFormat(JSON)

	def getHypernym(self, query):
		token = query.replace(" ", "_")
		tokText = token.capitalize()

		url = "http://dbpedia.org/resource/" + tokText

		self.sparql.setQuery(""" 
	          PREFIX dbc: <http://dbpedia.org/resource/Category:>
			PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
			PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			PREFIX dbo: <http://dbpedia.org/ontology/>
			PREFIX dct: <http://purl.org/dc/terms/>

				SELECT DISTINCT ?values
				WHERE {
					<""" + url + """> <http://purl.org/linguistics/gold/hypernym> ?values.
				}
		""")

		results = self.sparql.query().convert()
		print(results['results']['bindings'])
		hypernym = ""
		for r in results['results']['bindings']:
			hypernym = r['values']['value'].replace("http://dbpedia.org/resource/", "")

		return hypernym

	def getType(self, query):
		try:
			token = query.replace(" ", "_")
			tokText = token.capitalize()

			url = "http://dbpedia.org/resource/" + tokText
			# print("URL: ", url)

			types = []
			self.sparql.setQuery(""" 
			               PREFIX dbc: <http://dbpedia.org/resource/Category:>
						PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
						PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
						PREFIX dbo: <http://dbpedia.org/ontology/>
						PREFIX dct: <http://purl.org/dc/terms/>

		    				SELECT DISTINCT ?type
		    				WHERE {
		    					<""" + url + """> rdf:type ?type.
		    				}
		    			""")

			results = self.sparql.query().convert()
			for r in results['results']['bindings']:
				tayp = r['type']['value'].replace("http://dbpedia.org/ontology/","")
				tayp = tayp.replace("http://dbpedia.org/class/yago/","")
				tayp = ''.join([i for i in tayp if not i.isdigit()])
				types.append(tayp)

			# Find LEMMA
			if len(types) == 0:
				nlpword = self.nlp(query)
				token = nlpword[0].lemma_.replace(" ", "_")
				tokText = token.capitalize()

				url = "http://dbpedia.org/resource/" + tokText

				types = []
				self.sparql.setQuery(""" 
				               PREFIX dbc: <http://dbpedia.org/resource/Category:>
							PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
							PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
							PREFIX dbo: <http://dbpedia.org/ontology/>
							PREFIX dct: <http://purl.org/dc/terms/>

			    				SELECT DISTINCT ?type
			    				WHERE {
			    					<""" + url + """> rdf:type ?type.
			    				}
			    			""")

				results = self.sparql.query().convert()
				for r in results['results']['bindings']:
					tayp = r['type']['value'].replace("http://dbpedia.org/ontology/","")
					tayp = tayp.replace("http://dbpedia.org/class/yago/","")
					tayp = ''.join([i for i in tayp if not i.isdigit()])
					types.append(tayp)

			# print("TYPES: ", types)
			return types
		except:
			return []
		

	def searchFoodCategory(self, query):
		token = query.replace(" ", "_")
		tokText = token.capitalize()

		url = "http://dbpedia.org/resource/" + tokText

		self.sparql.setQuery(""" 
	               PREFIX dbc: <http://dbpedia.org/resource/Category:>
				PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
				PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
				PREFIX dbo: <http://dbpedia.org/ontology/>
				PREFIX dct: <http://purl.org/dc/terms/>

    				SELECT DISTINCT ?categories
    				WHERE {
    					<""" + url + """> dct:subject ?categories.
    				}
    			""")

		categories = []
		results = self.sparql.query().convert()
		for r in results['results']['bindings']:
			categories.append(r['categories']['value'].replace("http://dbpedia.org/resource/Category:", ""))

		# Find LEMMA
		if len(categories) == 0:
			nlpword = self.nlp(query)
			token = nlpword[0].lemma_.replace(" ", "_")
			tokText = token.capitalize()

			url = "http://dbpedia.org/resource/" + tokText

			types = []
			self.sparql.setQuery(""" 
			               PREFIX dbc: <http://dbpedia.org/resource/Category:>
						PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
						PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
						PREFIX dbo: <http://dbpedia.org/ontology/>
						PREFIX dct: <http://purl.org/dc/terms/>

		    				SELECT DISTINCT ?categories
		    				WHERE {
		    					<""" + url + """> dct:subject ?categories.
		    				}
		    			""")

			results = self.sparql.query().convert()
			for r in results['results']['bindings']:
				categories.append(r['categories']['value'].replace("http://dbpedia.org/resource/Category:", ""))

		return categories

	def search(self, query):
		token = query.replace(" ", "_")
		tokText = token.capitalize()

		url = "http://dbpedia.org/resource/" + tokText

		sparql.setQuery( """ 
	               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

	    			SELECT *
	    			WHERE { <""" + url + """> 
	    				?label ?value }"""
	    		)

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
			if len(results["results"]["bindings"]) == 0:
				return False
			else:
				return True
			return False
		else: 
			return True
