
class SportsEventsDictionary(object):
	dictionary = {}

	def __init__ (self):
		self.dictionary = {
			 "International Basketball Federation" : {
			 	"ABBR" : "FIBA",
			 	"SPORT" : ["Basketball"]
			 },
			 "FIBA" : {
			 	"ABBR" : "FIBA",
			 	"SPORT" : ["Basketball"]
			 },
			 "Philippine Basketball Association" : {
			 	"ABBR" : "PBA",
			 	"SPORT" : ["Basketball"]
			 },
			 "PBA" : {
			 	"ABBR" : "PBA",
			 	"SPORT" : ["Basketball"]
			 },
			 "Commisioners Cup" : {
			 	"ABBR" : "CC",
			 	"SPORT" : ["Basketball"]
			 },
			 "CC" : {
			 	"ABBR" : "CC",
			 	"SPORT" : ["Basketball"]
			 },
			 "University Athletic Association of the Philippines" : {
			 	"ABBR" : "UAAp",
			 	"SPORT" : ["Basketball", "Table Tennis", "Volleyball", "Football", "Cheering Squad", "Badmintom", "Baseball", "Beach Volleyball", "Chess"]
			 },
			 "UAAP" : {
			 	"ABBR" : "UAAp",
			 	"SPORT" : ["Basketball", "Table Tennis", "Volleyball", "Football", "Cheering Squad", "Badmintom", "Baseball", "Beach Volleyball", "Chess"]
			 },
			 "National Collegiate Athletic Association" : {
			 	"ABBR" : "NCAA",
			 	"SPORT" : ["Basketball", "Volleyball"]
			 },
			 "NCAA" : {
			 	"ABBR" : "NCAA",
			 	"SPORT" : ["Basketball", "Volleyball"]
			 },
			 "National Basketball Association" : {
			 	"ABBR" : "NBA",
			 	"SPORT" : "Basketball"
			 },
			 "NBA" : {
			 	"ABBR" : "NBA",
			 	"SPORT" : "Basketball"
			 },
			 "FIFA World Cup" : {
			 	"ABBR" : "World Cup",
			 	"SPORT" : "Football"
			 },
			 "FIFA" : {
			 	"ABBR" : "World Cup",
			 	"SPORT" : "Football"
			 },
			 "World Wrestling Entertainment" : {
			 	"ABBR" : "WWE",
			 	"SPORT" : "Wrestling"
			 },
			 "WWE" : {
			 	"ABBR" : "WWE",
			 	"SPORT" : "Wrestling"
			 },
			 "Ultimate Fighting Champion" : {
			 	"ABBR" : "UFC",
			 	"SPORT" : ["Martial Arts", "Wrestling"]
			 },
			 "UFC" : {
			 	"ABBR" : "UFC",
			 	"SPORT" : ["Martial Arts", "Wrestling"]
			 },
			 "International Table Tennis Federation" : {
			 	"ABBR" : "ITTF",
			 	"SPORT" : "Table Tennis"
			 },
			 "ITTF" : {
			 	"ABBR" : "ITTF",
			 	"SPORT" : "Table Tennis"
			 },

		}
	


	def replace(self, key):
		# print("Key: ", key)
		return self.replace_all(key, self.dictionary)

	def replace_all(self, text, dic):
		for i, j in dic.items():
			text = text.replace(i, j)
		return text

	def lookup(self, key):
		return self.dictionary.get(key)