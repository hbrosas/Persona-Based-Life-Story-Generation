
class GameTeamsDictionary(object):
	dictionary = {}

	def __init__ (self):
		self.dictionary = {
			 "Team Solo Mid" : {
			 	"NAME" : "Team Solo Mid",
			 	"ABBR" : "TSM",
			 	"Categories": ["League of Legends", "Fortnite", "Player Unkown's Battlegrounds", "H1Z1", "Super Smash Bros", "Overwatch", "VainGlory",],
			 	"Country": ["North America"],
			 },
			 "Cloud 9" : {
			 	"NAME" : "Cloud 9",
			 	"ABBR" : "C9",
			 	"Categories": ["League of Legends", "Fortnite", "Player Unkown's Battlegrounds", "H1Z1", "Super Smash Bros", "Overwatch", "Clash Royale", "Rocket League", "Rainbow Six Siege"],
			 	"Country": ["North America"],
			 },			 
			 "Golden Guardians" : {
			 	"NAME" : "Golden Guardians",
			 	"ABBR" : ["Golden Guardians"],
			 	"Categories" : ["League of Legends"],
			 	"Country": ["North America"],
			 },
			 "FlyQuest" : {
			 	"NAME" : "FlyQuest",
			 	"ABBR" : ["FlyQuest"],
			 	"Categories" :["League of Legends"],
			 	"Country": ["North America"],
			 },
			 "Echo Fox" : {
			 	"NAME" : "EchoFox",
 			 	"ABBR" : ["EchoFox"],
			 	"Categories" : ["League of Legends"],
			 	"Country": ["North America"],
			 },
			 "Clutch Gaming" : {
			 	"NAME" : "Clutch Gaming",
			 	"ABBR" : ["CG",],
			 	"Type" : ["League of Legends"],
			 	"Country": ["Europe"],
			 },
			 "Team Liquid" : {
			 	"NAME" : "Team Liquid",
			 	"ABBR" : ["TL"],
			 	"Categories" : ["League of Legends", "Streamers", "Rocket League", "Counter Strike: Global Offensive", "Smash", "Smite"],
			 	"Country": ["North America"],
			 },
			 "Optic Gaming" : {
			 	"NAME" : "Optic Gaming",
			 	"ABBR" : ["Optic"],
			 	"Categories" : ["League of Legends", "Defense of the Ancients", "Counter Strike: Global Offensive"],
			 	"Country": ["North America"],
			 },
			 "Counter Logic Gaming" : {
			 	"NAME" :  "Counter Logic Gaming",
			 	"ABBR" : ["CLG"],
			 	"Categories" : ["League of Legends","Counter Strike: Global Offensive"],
			 	"Country": ["North America"],
			 },
			 "Astralis" : {
			 	"NAME" :  "Astralis",
			 	"ABBR" : ["Astralis"],
			 	"Categories" : ["Counter Strike: Global Offensive"],
			 	"Country": ["Europe"],
			 },
			 "Natus Vincere" : {
			 	"NAME" :  "Natus Vincere",
			 	"ABBR" : ["NAVI"],
			 	"Categories" : ["Counter Strike: Global Offensive","Defense of the Ancients"],
			 	"Country":  ["Europe"],
			 },
			 "Faze" : {
			 	"NAME" :  "Faze" ,
			 	"ABBR" : ["Faze"],
			 	"Categories" : ["Counter Strike: Global Offensive","Call of Duty"],
			 	"Country":  ["Europe"],
			 },
			 "Fnatic" : {
			 	"NAME" :  "Fnatic",
			 	"ABBR" : ["FNC", "Fnatic"],
			 	"Categories" : ["Counter Strike: Global Offensive","Defense of the Ancients", "League of Legends"],
			 	"Country":  ["Europe"],
			 },
			 "North" : {
			 	"NAME" :  "North" ,
			 	"ABBR" : ["North"],
			 	"Categories" : ["Counter Strike: Global Offensive"],
			 	"Country":  ["Europe"],
			 },
			 "mousesports" : {
			 	"NAME" :  "mousesports",
			 	"ABBR" : ["mouz"],
			 	"Categories" : ["Counter Strike: Global Offensive","Defense of the Ancients"],
			 	"Country":  ["Europe"],
			 },
			 "NRG Esports" : {
			 	"NAME" : "NRG Esports",
			 	"ABBR" : ["NRG"],
			 	"Categories" : ["Counter Strike: Global Offensive"],
			 	"Country": ["North America"],
			 },
			 "G2 Esports" : {
			 	"NAME" :  "G2 Esports",
			 	"ABBR" : ["G2"],
			 	"Categories" : ["Counter Strike: Global Offensive", "League of Legends", "Hearthstone"],
			 	"Country": ["Europe"],
			 },
			 "Ninjas in Pyjamas" : {
			 	"NAME" :  "Ninjas in Pyjamas",
			 	"ABBR" : ["NIP"],
			 	"Categories" : ["Counter Strike: Global Offensive", "Defense of the Ancients", "Overwatch"],
			 	"Country": ["Europe"],
			 "Virtus Pro" : {
			 	"NAME" : "Virtus Pro",
			 	"ABBR" : ["VP"],
			 	"Categories" : ["Counter Strike: Global Offensive", "Defense of the Ancients"],
			 	"Country": ["Europe"],
			 },
			 "Evil Geniuses" : {
			 	"NAME" : "Evil Geniuses",
			 	"ABBR" : ["EG"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["North America"],
			 },
			 "Newbee" : {
			 	"NAME" :  "Newbee",
			 	"ABBR" : ["Newbee"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["China"],
			 },
			 "Mineski" : {
			 	"NAME" :  "Mineski",
			 	"ABBR" : ["MSK", "mineski"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["Philippines"],
			 },
			 "Team Kinguin" : {
			 	"NAME" :  "Team Kinguin",
			 	"ABBR" : ["Kinguin"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["Europe"],
			 },
			 "EnvyUs" : {
			 	"NAME" : "EnvyUs",
			 	"ABBR" : ["NV"],
			 	"Categories" : ["Counter Strike: Global Offensive", "Overwatch"],
			 	"Country": ["Europe", "North America"],
			 },
			 "The Net Com" : {
			 	"NAME" :  "The Net Com",
			 	"ABBR" : ["TNC"],
			 	"Categories" : ["Counter Strike: Global Offensive", "Defense of the Ancients"],
			 	"Country": ["Philippines", "Malaysian"]
			 },
			 "Team Secret" : {
			 	"NAME" : "Team Secret",
			 	"ABBR" : ["Secret"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["Europe"],
			 },			 
			 "Digital Chaos" : {
			 	"NAME" :  "Digital Chaos",
			 	"ABBR" : ["DC"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["North America"],
			 },
			 "OG DOTA 2" : {
			 	"NAME" :  "OG DOTA 2",
			 	"ABBR" : ["OG"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["Europe"],
			 },
			 "paiN Gaming" : {
			 	"NAME" :  "paiN Gaming",
			 	"ABBR" : ["paiN"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["Brazil"],
			 },
			 "VG.J Thunder" : {
			 	"NAME" :  "VG.J Thunder",
			 	"ABBR" : ["VGJ.T"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["China"],
			 },
			 "Complexity Gaming" : {
			 	"NAME" :  "Complexity Gaming",
			 	"ABBR" : ["coL"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["North America"],
			 },
			 "Team Spirit" : {
			 	"NAME" :  "Team Spirit" ,
			 	"ABBR" : ["TS"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["Europe"],
			 },
			 "TNC Tiger" : {
			 	"NAME" :  "TNC Tiger",
			 	"ABBR" : ["TNC.T"],
			 	"Categories" : ["Defense of the Ancients"],
			 	"Country": ["Malaysia"],
			 },
			 "SK Telecom" : {
			 	"NAME" : "SK Telecom",
			 	"ABBR" : ["SKT"],
			 	"Categories" : ["League of Legends"],
			 	"Country":  ["Korea"],
			 },
			 "KT Rolster" : {
			 	"NAME" :  "KT Rolster",
			 	"ABBR" : ["KT"],
			 	"Categories" : ["League of Legends"],
			 	"Country": ["Korea"],
			 },
			 "Afreeca Freecs" : {
			 	"NAME" :  "Afreeca Freecs",
			 	"ABBR" : ["AFS"],
			 	"Categories" : ["League of Legends"],
			 	"Country": ["Korea"],
			 },
			 "Kingzone DragonX" : {
			 	"NAME" :  "Kingzone DragonX",
			 	"ABBR" : ["KZ"],
			 	"Categories" : ["League of Legends"],
			 	"Country": ["Korea"],
			 },
			 "Griffin" : { 
			 	"NAME" :  "Griffin",
			 	"ABBR" : ["Griffin"],
			 	"Categories" : ["League of Legends"],
			 	"Country": ["Korea"],
			 },
			 "Royal Never Give Up" : {
			 	"NAME" :  "Royal Never Give Up",
			 	"ABBR" : ["RNG"],
			 	"Categories" : ["League of Legends"],
			 	"Country": ["China"],
			 },
			 "Oh My God" : {
			 	"NAME" :  "Oh My God",
			 	"ABBR" : ["OMG"],
			 	"Categories" : ["League of Legends"],
			 	"Country": ["China"],
			 },
			 "Vici Gaming" : {
			 	"NAME" : "Vici Gaming",
			 	"ABBR" : ["VG"],
			 	"Categories" : ["League of Legends","Counter Strike: Global Offensive", "Defense of the Ancients"],
			 	"Country": ["China"],
			 },
			 "World Elite" : {
			 	"NAME" :  "World Elite",
			 	"ABBR" : ["WE"],
			 	"Categories" : ["League of Legends"],
			 	"Country": ["China"],
			 },				 			 
		}
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

	def lookupAbbr(self, key):
		for k, v in self.dictionary.items():
			for abbr in v['ABBR']:
				if abbr.lower() in key.lower():
					return v