import json

class FileManager:
	def writeFile(assertions, filename):
		url = "C://Users//Hazel//Documents//GitHub//Persona-Based-Life-Story-Generation//Information Extraction//IEApp//"
		f = open(url + filename + ".txt", "w+")

		for a in assertions:
			f.write(json.dumps(a, indent=2))
			f.write(",")

		f.close