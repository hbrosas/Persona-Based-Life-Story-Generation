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
		
	def doesExists(self, token):
		tokText = token.capitalize()
		url = "http://dbpedia.org/resource/" + tokText
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery( """ 
		               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

		    			SELECT ?label, ?value
		    			WHERE { <""" + url + """> 
		    				?label ?value }""")
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

	def dbPedia(self, url, tokText):
		#DBPedia
		db = Database()
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery( """ 
		               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
					PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
					prefix owl: <http://www.w3.org/2002/07/owl#>
					prefix prov: <http://www.w3.org/ns/prov#>
					prefix foaf: <http://xmlns.com/foaf/0.1/>
					prefix dct: <http://purl.org/dc/terms/>

		    			SELECT ?property, ?value
		    			WHERE { <""" + url + """> 
		    				?property ?value }""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		typeURLs = ["http://www.w3.org/2002/07/owl#", "http://xmlns.com/foaf/0.1/", "http://dbpedia.org/ontology/"]
		redirectURL = "http://dbpedia.org/ontology/wikiPageRedirects"
		birthPlaceURL = "http://dbpedia.org/ontology/birthPlace"
		birthDateURL = "http://dbpedia.org/ontology/birthDate"
		nameURL = "http://xmlns.com/foaf/0.1/givenName"
		descURL = "http://purl.org/dc/terms/description"

		if len(results["results"]["bindings"]) == 0:
			print("Not found")
		else: 
			print("Length: ", len(results["results"]["bindings"]))

		# for result in results["results"]["bindings"]:
		# 	prop = result["property"]["value"]
		# 	value = result["value"]["value"]
			# print(prop, " - ", value)

			# if prop == redirectURL:
			# 	ent = Entity()
			# 	subj = value.replace("http://dbpedia.org/resource/", '')
			# 	ent.dbPedia(value, subj)

			# if "type" in result["property"]["value"]:
			# 	relation = db.findRelation("IsA")
			# 	for url in typeURLs:
			# 		if url in value:
			# 			val = value.replace(url, '')
			# 	db.feedSemRel(relation, tokText, val)
			# 	# print(tokText + " - " + "RELATED" + " - " + val)

			# if prop == birthPlaceURL:
		 #    		relation = db.findRelation("BirthPlace")
		 #    		val = value.replace("http://dbpedia.org/resource/", '')
		 #    		db.feedSemRel(relation, tokText, val)
		 #    		# print(tokText + " - " + "RELATED" + " - " + val)

			# if prop == birthDateURL:
			# 	relation = db.findRelation("BirthDate")
			# 	val = value
			# 	db.feedSemRel(relation, tokText, val)
			# 	# print(tokText + " - " + "RELATED" + " - " + val)

			# if prop == nameURL:
			# 	relation = db.findRelation("PersonName")
			# 	val = value
			# 	db.feedSemRel(relation, tokText, val)
			# 	# print(tokText + " - " + "RELATED" + " - " + val)

			# # Get Description
			# if prop == descURL:
			# 	relation = db.findRelation("Description")
			# 	val = value
			# 	db.feedSemRel(relation, tokText, val)
			# 	# print(tokText + " - " + "RELATED" + " - " + val)


