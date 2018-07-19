
class SportsTeamsDictionary(object):
	dictionary = {}

	def __init__ (self):
		self.dictionary = {
			 "Boston Celtics" : {
			 	"ABBR" : ["BOS", "CELT", "CELTS"],
			 },
			 "Atlanta Hawks" : {
			 	"ABBR" : "ATL",
			 },
			 "Broklyn Nets" : {
			 	"ABBR" : "BKN",
			 },
			 "Charlotte Hornets" : {
			 	"ABBR" : "CHA",
			 },
			 "Chicago Bulls" : {
			 	"ABBR" : "CHI",
			 },
			 "Cleveland Cavalies" : {
			 	"ABBR" : ["CAVS", "CLE", "CAV"],
			 },
			 "Dallas Mavericks" : {
			 	"ABBR" : "DAL",
			 },
			 "Denver Nuggets" : {
			 	"ABBR" : "DEN",
			 },
			 "Detroit Pistons" : {
			 	"ABBR" : "DET",
			 },
			 "Golden State Warriors" : {
			 	"ABBR" : "GSW",
			 },
			 "Houston Rockets" : {
			 	"ABBR" : "HOU",
			 },
			 "Indiana Pacers" : {
			 	"ABBR" : "IND",
			 },
			 "Los Angeles Clippers" : {
			 	"ABBR" : "LAC",
			 },		 
			 "Los Angeles Lakers" : {
			 	"ABBR" : "LAL",
			 },		
			 "Memphis Grizzlies" : {
			 	"ABBR" : "MEM",
			 },	 
			 "Miami Heat" : {
			 	"ABBR" : "MIA",
			 },
			 "Milwaukee Bucks" : {
			 	"ABBR" : "MIL",
			 },
			 "Minnesota Timberwolves" : {
			 	"ABBR" : "DET",
			 },
			 "New Orleans Pelicans" : {
			 	"ABBR" : "NOP",
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