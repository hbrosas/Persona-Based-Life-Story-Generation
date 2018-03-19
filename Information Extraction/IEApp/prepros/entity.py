from database import Database
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import spacy

class Entity:

	def isAnEntity(self, token):
		db = Database()
		semrel = db.searchSemRel(token.orth_)

		if len(semrel) == 0:
			ent = Entity()
			ent.learn(token)

		# search if it has an entity

	def learn(self, token):
		# ConceptNet
		req = "http://api.conceptnet.io/c/en/" + token.orth_
		obj = requests.get(req).json()
		for e in obj['edges']:
			if e['start']['language'] == "en":
				rel = e['rel']['label']
				db = Database()
				relId = db.findRelation(rel)
				if not relId == -1:
					# db.feedSemRel(relId, e['start']['label'], e['end']['label'])
					print(e['start']['label'] + " - " + rel + " - " + e['end']['label'])
		#DBPedia
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		url = "http://dbpedia.org/resource/" + token.orth_.capitalize()
		print(url)
		sparql.setQuery( """ 
		               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
					PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
					prefix dbo: <http://dbpedia.org/ontology/>
					prefix owl: <http://www.w3.org/2002/07/owl#>
					prefix prov: <http://www.w3.org/ns/prov#>
					prefix foaf: <http://xmlns.com/foaf/0.1/>
					prefix dbp: <http://dbpedia.org/property/>
					prefix dct: <http://purl.org/dc/terms/>

		    			SELECT ?property, ?value
		    			WHERE { <""" + url + """> 
		    				?property ?value }""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		# print(results)

		for result in results["results"]["bindings"]:
		    print(result)

