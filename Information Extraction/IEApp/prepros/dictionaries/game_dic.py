
class GameDictionary(object):
	dictionary = {}

	def __init__ (self):
		self.dictionary = {
			 "League of Legends" : {
			 	"NAME" : "League of Legends",
			 	"ABBR" : ["LoL", "League", "L0L", "lol"],
			 	"Type" : "Multiplayer Online Battle Arena",
			 	"MODES": ["Ranked"]
			 },
			 "Defense of the Ancients" : {
			 	"NAME" : "Defense of the Ancients",
			 	"ABBR" : ["DOTA", "Dota", "Dota 2"],
			 	"Type" : "Multiplayer Online Battle Arena",
			 	"MODES": ["Ranked"]
			 },
			 "Counter Strike: Global Offensive" : {
			 	"NAME" : "Counter Strike: Global Offensive",
			 	"ABBR" : ["CS:GO", "csgo", "CSGO", "CS"],
			 	"Type" : "First Person Shooter",
			 	"MODES": ["Competitive"]
			 },
			 "Fortnite Battle Royale" : {
			 	"NAME" : "Fornite Batle Royale",
			 	"ABBR" : ["Fortnite"],
			 	"Type" : "Battle Royale",
			 	"MODES": ["Ranked"]
			 },
			 "Realm Royale" : {
			 	"NAME": "Realm Royale",
			 	"ABBR" : ["RR"],
			 	"Type" : "Battle Royale",
			 	"MODES": ["Ranked"]
			 },
			 "Player Unknown's Battlegrounds" : {
			 	"NAME": "Player Unknown's Battlegrounds",		 	
				"ABBR" : ["PUBG","POBG", "PUGG", "P0BG", "PABG", "PABGI"],
			 	"Type" : "Battle Royale",
			 	"MODES": ["Ladder"]
			 },
			 "Overwatch" : {
			 	"NAME": "Overwatch",
			 	"ABBR" : ["OW"],
			 	"Type" : "First Person Shooter",
			 	"MODES": ["Ranked"]
			 },
			 "Hearthstone" : {
			 	"NAME": "Hearthstone",
			 	"ABBR" : ["HS"],
			 	"Type" : "Collectible Card Game",
			 	"MODES": ["Ranked"]
			 },
			 "Monster Hunter" : {
			 	"NAME": "Monster Hunter",
			 	"ABBR" : ["Monster Hunter"],
			 	"Type" : "Action Role-playing Game",
			 	"MODES": ["Single Player", "Multiplayer"]
			 },
			 "Monster Hunter: World" : {
			 	"NAME": "Monster Hunter: World",
			 	"ABBR" : ["MOnster Hunter: World"],
			 	"Type" : "Action Role-playing Game",
			 	"MODES": ["Single Player", "Multiplayer"]
			 },
			 "Far Cry 5" : {
			 	"NAME": "Far Cry 5",
			 	"ABBR" : ["Far Cry 5", "Farcry 5", "Far Cry", "FC5"],
			 	"Type" : ["Action-adventure Game", "First Person Shooter"],
			 	"MODES": ["Multiplayer"]
			 },
			 "Fallout 76" : {
			 	"NAME": "Fallout 76",
			 	"ABBR" : ["Fallout 76", "F76", "Fallout", "Fallout-76"],
			 	"Type" : "Action role-playing Game",
			 	"MODES": ["Multiplayer"]
			 },
			 "Vampyr" : {
			 	"NAME": "Vampyr",
			 	"ABBR" : ["Vampyr", "Vamp", "Vampire"],
			 	"Type" : "Action Role-playing Game",
			 	"MODES": ["Multiplayer"]
			 },
			 "Jurrasic World Evolution" : {
			 	"NAME": "Jurrasic World Evolution",
			 	"ABBR" : ["Jurrasic", "Jurrasic World", "JWE"],
			 	"Type" : "Economic simulation",
			 	"MODES": ["Single Player"]
			 },
			 "Dragon Ball FighterZ" : {
			 	"NAME": "Dragon Ball FighterZ",
			 	"ABBR" : "DBZ",
			 	"Type" : "Fighting Game",
			 	"MODES": ["Multiplayer", "Ranked"]
			 },
			 "Rainbow Six Siege" : {
			 	"NAME": "Rainbow Six Siege",
			 	"ABBR" : ["R6", "Rainbow Six Siege", "R6 Siege", "R6S"],
			 	"Type" : "Tactical Shooter",
			 	"MODES": ["Ranked"]
			 },
			 "Warframe" : {
			 	"NAME": "Warframe",
			 	"ABBR" : ["Warframe", "WF" "WFrame"],
			 	"Type" : "Third Person Shooter",
			 	"MODES": ["Ranked"]
			 },
			 "The Sims" : {
			 	"NAME": "The Sims",
			 	"ABBR" : ["SIMS", "SIM", "THE SIMS"],
			 	"Type" : "Simulation Video Game",
			 	"MODES": ["Single Player"]
			 },
			 "Rocket League" : {
			 	"NAME": "Rocket League",
			 	"ABBR" : ["Rocket League", "RL"],
			 	"Type" : "Sports Game",
			 	"MODES": ["Ranked"]
			 },
			 "Rules of Survival" : {
			 	"NAME": "Rules of Survival",
			 	"ABBR" : ["ROS"],
			 	"Type" : "Battle Royale",
			 	"MODES": ["Ladder"]
			 },
			 "BattleField 1" : {
			 	"NAME": "BattleField 1",
			 	"ABBR" : ["BF", "Bfield", "BattleField"],
			 	"Type" : "First-person shooter",
			 	"MODES": ["Ranked"]
			 },
			 "Call of Duty" : {
			 	"NAME": "Call of Duty",
			 	"ABBR" : ["COD"],
			 	"Type" : "First-person shooter",
			 	"MODES": ["Ranked"]
			 },
			  "Black Desert Online": {
			  	"NAME": "Black Desert Online",
			 	"ABBR" : ["Black Desert", "BDO"],
			 	"Type" : "Massively multiplayer online role-playing game",
			 	"MODES": ["Multiplayer"]
			 },	
			 "Farmville" : {
			 	"NAME": "Farmville",
			 	"ABBR" : ["Farmville", "FarmVille"],
			 	"Type" : "Role-playing Video Game",
			 	"MODES": ["Single Player"]
			 },
			 "Pet Society" : {
			 	"NAME": "Pet Society",
			 	"ABBR" : ["Pet Society", "PS", "PSociety", "Pet"],
			 	"Type" : "Digital Pet",
			 	"MODES": ["Single Player"]
			 },
			 "Arena of Valor" : {
			 	"NAME": "Arena of Valor",
			 	"ABBR" : ["AOV", "A of Valor"],
			 	"Type" : "Multiplayer online battle arena",
			 	"MODES": ["Ranked"]
			 },
			 "Mobile Legends: Bang Bang" : {
			 	"NAME": "Mobile Legends: Bang Bang",
			 	"ABBR" : ["Mobile Legends", "ML"],
			 	"Type" : "Multiplayer online battle arena",
			 	"MODES": ["Ranked"]
			 },	
			 "Candy Crush" : {
				"NAME": "Candy Crush",
			 	"ABBR" : ["Candy Crush", "CC", "CCrush"],
			 	"Type" : "Puzzle Video-game",
			 	"MODES": ["Single Player"]
			 },
			 "Clash of Clans" : {
			 	"NAME": "Clash of Clans",
			 	"ABBR" : ["CoC", "Clash of Clans", "C of CLans"],
			 	"Type" : "Strategy video game",
			 	"MODES": ["Multiplayer"]
			 },
			  "Fruit Ninja" : {
			  	"NAME": "Fruit Ninja",
			 	"ABBR" : ["Fruit Ninja", "FN", "FNinja"],
			 	"Type" : "Arcade Game",
			 	"MODES": ["Single Player"]
			 },
			  "Final Fantasy XV" : {
			  	"NAME": "Final Fantasy XV",
			 	"ABBR" : ["FFXV", "Final Fantasy", "FF"],
			 	"Type" : "Action role-playing game",
			 	"MODES": ["Single Player"]
			 },
			  "Harry Potter Hogwarts Mystery" : {
			  	"NAME": "Harry Potter Hogwarts Mystery",
			 	"ABBR" : ["Harry Potter Hogwarts Mystery", "HPHM"],
			 	"Type" : "Role-playing video game",
			 	"MODES": ["Single Player"]
			 },
			  "Plants vs Zombies" : {
			  	"NAME": "Plants vs Zombies",
			 	"ABBR" : ["PvZ", "Plants vs Zombies"],
			 	"Type" : "Tower Defense",
			 	"MODES": ["Single Player"]
			 },
			  "The Witcher Battle Arena" : {
			  	"NAME": "The Witcher Battle Arena",
			 	"ABBR" : ["The Witcher", "TWBA"],
			 	"Type" : "Multiplayer online battle arena",
			 	"MODES": ["Ranked"]
			 },
			  "Vain Glory" : {
			  	"NAME": "Vain Glory",
			 	"ABBR" : ["Vain Glory", "VG"],
			 	"Type" : "Multiplayer online battle arena",
			 	"MODES": ["Ranked"]
			 },
			  "NBA 2K18" : {
			  	"NAME": "NBA 2K18",
			 	"ABBR" : ["NBA 2K18", "NBA 2K"],
			 	"Type" : "Simulation Video Game",
			 	"MODES": ["Multiplayer"]
			 },
			 "NBA 2K17" : {
				"NAME": "NBA 2K18",
			 	"ABBR" : ["NBA 2K17"],
			 	"Type" : "Simulation Video Game",
			 	"MODES": ["Multiplayer"]
			 },
			 "Fallout 4" : {
			 	"NAME": "Fallout 4",
			 	"ABBR" : ["Fallout", "Fallout"],
			 	"Type" : "Action Role-playing Game",
			 	"MODES": ["Single Player"]
			 },
			 "Super Mario 4" : {
			 	"NAME": "Super Mario 4",
			 	"ABBR" : ["Super Mario 4", "Mario 4", "Super Mario"],
			 	"Type" : "Platform Game",
			 	"MODES": ["Single Player"]	
			 },
			 "God of War" : {
			 	"NAME": "God of War",
			 	"ABBR" : ["GoW", "God of War", "GodofWar"],
			 	"Type" : "Action-adventure Game",
			 	"MODES": ["Single Player"]
			 },
			  "Megaman" : {
			  	"NAME": "Megaman",
			 	"ABBR" : ["Megaman"],
			 	"Type" : "Action Game",
			 	"MODES": ["Single Player"]
			 },
			 "Tekken" : {
			 	"NAME": "Tekken",
			 	"ABBR" : ["Tekken"],
			 	"Type" : "Fighting Game",
			 	"MODES": ["Multiplayer"]
			 },
			 "Naruto Shippuden: Ninja Storm" : {
			 	"NAME": "Naruto Shippuden: Ninja Storm",
			 	"ABBR" : ["Naruto Shippuden: Ninja Storm"],
			 	"Type" : "Fighting Game",
			 	"MODES": ["Multiplayer"]
			 },
			 "Naruto" : {
			 	"NAME": "Naruto",
			 	"ABBR" : ["Naruto"],
			 	"Type" : "Fighting Game",
			 	"MODES": ["Multiplayer"]
			 },
			 "Diablo" : {
			 	"NAME": "Diablo",
			 	"ABBR" : ["Diablo"],
			 	"Type" : "Action role-playing game",
			 	"MODES": ["Multiplayer"]
			 },
			 "Mafia Wars" : {
			 	"NAME": "Mafia Wars",
			 	"ABBR" : ["Mafia Wars", "Mafia"],
			 	"Type" : "Role-playing Game",
			 	"MODES": ["Single Player"]
			 },
			 "Tetris Battle" : {
			 	"NAME": "Tetris Battle",
			 	"ABBR" : ["Tetris Battle","Tetris"],
			 	"Type" : "Puzzle Video-game",
			 	"MODES": ["Multiplayer"]
			 },
			 "Candy Crush Saga" : {
			 	"NAME": "Candy Crush Saga",
			 	"ABBR" : ["Candy Crush", "CC"],
			 	"Type" : "Puzzle Video-game",
			 	"MODES": ["Single Player"]
			 },
			 "Zynga Poker" : {
			 	"NAME": "Zynga Poker",
			 	"ABBR" : ["Poker"],
			 	"Type" : "Poker card game",
			 	"MODES": ["MultiPlayer"]
			 },
			 "Criminal Case" : {
			 	"NAME": "Criminal Case",
			 	"ABBR" : ["Criminal Case"],
			 	"Type" : "Puzzle Video-game",
			 	"MODES": ["Single Player"]
			 },
			 "8-Ball Pool" : {
			 	"NAME": "8-Ball Pool",
			 	"ABBR" : ["Pool"],
			 	"Type" : "Sports-Arcade",
			 	"MODES": ["MultiPlayer"]
			 },
			 "Angry Birds" : {
			 	"NAME": "Angry Birds",
			 	"ABBR" : ["Angry Birds"],
			 	"Type" : "Puzzle",
			 	"MODES": ["Single Player"]
			 },
			 "Ninja Saga" : {
			 	"NAME": "Ninja Saga",
			 	"ABBR" : ["Ninja Saga"],
			 	"Type" : "Action-adventure",
			 	"MODES": ["MultiPlayer"]
			 },
			 "Special Force" : {
			 	"NAME": "Special Force",
			 	"ABBR" : ["sf", "SF", "Special Force"],
			 	"Type" : "Multiplayer Online First Person Shooter",
			 	"MODES": ["MultiPlayer"]
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
		for k, v in self.dictionary.items():
			if k.lower() == key.lower():
				return v

	def lookupAbbr(self, key):
		for k, v in self.dictionary.items():
			for abbr in v['ABBR']:
				if abbr.lower() == key.lower():
					return v