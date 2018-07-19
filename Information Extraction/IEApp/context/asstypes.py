
class AssTypeInfo:

	def getAssertion(self, persona, data):
		assertions = []
		if persona == "The Foodie":
			assertions = self.foodie(data, assertions)
		elif persona == "The Fangirl/Fanboy":
			assertions = self.fangirlboy(data, assertions)

		return assertions

	def fangirlboy(self, data, assertions):
		for d in data:
			if d["Person"] is not None and d["Fandom"] is not None and d["FanOf"] is not None and d["Type"] is not None:
				assertions.append({
					'type' : "fandom",
					'values' : {
						"Person" 			: d["Person"],
						"FanOf" 			: d["FanOf"],
						"Fandom"			: d["Fandom"],
						"Type"		 		: d["Type"]
					},
					'persona' : "The Fangirl/Fanboy",
				})
			if d["Person"] is not None and d["FanOf"] is not None and d["Type"] is not None and d["Action"] is None: 
				assertions.append({
					'type' : "shared_about",
					'values' : {
						"Person" 			: d["Person"],
						"FanOf" 			: d["FanOf"],
						"Type"		 		: d["Type"],
						"Tagged_Friends"	: d["Tagged_Friends"],
						"Organization"		: d["Organization"],
						"Location"			: d["Location"]
					},
					'persona' : "The Fangirl/Fanboy",
				})
			if d["Person"] is not None and d["FanOf"] is not None and d["Type"] is not None and d["Action"] is not None: 
				assertions.append({
					'type' : "activity",
					'values' : {
						"Person" 			: d["Person"],
						"FanOf" 			: d["FanOf"],
						"Action" 			: d["Action"],
						"Type"		 		: d["Type"],
						"Tagged_Friends"	: d["Tagged_Friends"],
						"Organization"		: d["Organization"],
						"Location"			: d["Location"]
					},
					'persona' : "The Fangirl/Fanboy",
				})
			if d["Person"] is not None and d["FanOf"] is not None and d["Type"] is not None and d["Description"] is not None: 
				assertions.append({
					'type' : "describes",
					'values' : {
						"Person" 			: d["Person"],
						"FanOf" 			: d["FanOf"],
						"Description"		: d["Description"],
						"Type"		 		: d["Type"],
						"Tagged_Friends"	: d["Tagged_Friends"],
						"Organization"		: d["Organization"],
						"Location"			: d["Location"]
					},
					'persona' : "The Fangirl/Fanboy",
				})
			if d["Person"] is not None and d["FanOf"] is not None and d["Type"] is not None and d["Sentiment"] is not None: 
				assertions.append({
					'type' : "sentiment",
					'values' : {
						"Person" 			: d["Person"],
						"FanOf" 			: d["FanOf"],
						"Sentiment"			: d["Sentiment"],
						"Type"		 		: d["Type"],
					},
					'persona' : "The Fangirl/Fanboy",
				})

		return assertions

	def foodie(self, data, assertions):
		for d in data:
			if not d['Description'] == "" and d['Description'] is not None and (d['Food'] is not None or len(d['Organization']) != 0):
				assertions.append({
					'type' : "food_describe",
					'values' : {
						"Person" 			: d['Person'],
						"Food" 				: d['Food'],
						"Description" 		: d['Description'],
						"Organization" 		: d['Organization'],
						"Type" 				: d['Type'],
						"Location" 			: d['Location']
					},
					'persona' : "The Foodie",
					'date' : d['Date'],
					'time' : d['Time']
				})
			if not d['Action'] == "" and d['Action'] is not None and (d['Food'] is not None or len(d['Organization']) != 0):
				assertions.append({
					'type' : "food_activity",
					'values' : {
						"Person" 			: d['Person'],
						"Food" 				: d['Food'],
						"Action" 			: d['Action'],
						"Organization" 		: d['Organization'],
						"Type" 				: d['Type'],
						"Tagged_Friends" 	: d['Tagged_Friends'],
						"Location" 			: d['Location'],
						'date' : d['Date'],
						'time' : d['Time']
					},
					'persona' : "The Foodie"
				})
			if not d['Sentiment'] == "" and d['Sentiment'] is not None and (d['Food'] is not None or len(d['Organization']) != 0):
				assertions.append({
					'type' : "food_sentiment",
					'values' : {
						"Person" 			: d['Person'],
						"Food" 				: d['Food'],
						"Type" 				: d['Type'],
						"Sentiment" 		: d['Sentiment'],
						"Sentiment_Class" 	: d['Sentiment_Class'],
						'date' : d['Date'],
						'time' : d['Time']
					},
					'persona' : "The Foodie"
				})
		return assertions

	def getChecklist(self, persona):
		if persona == "The Foodie":
			return 	{
				"Person" 			: None,
				"Food" 				: None,
				"Description" 		: None,
				"Action" 			: None,
				"Organization" 		: None,
				"Type" 				: None,
				"Tagged_Friends" 	: None,
				"Location" 			: None,
				"Sentiment" 		: None,
				"Sentiment_Class" 	: None,
				"Date"				: None,
				"Time"				: None
			}
		elif persona == "The Sports Fanatic":
			return 	{
				"Person" 			: None,
				"Sport" 			: None,
				"Team" 				: None,
				"FanOf" 			: None,
				"Achievement"	 	: None,
				"Activity"			: None,
				"Event"				: None,
				"Tagged_Friends" 	: None,
				"Location" 			: None,
				"Sentiment" 		: None,
				"Sentiment_Class" 	: None,
				"Date"				: None,
				"Time"				: None
			}
		elif persona == "The Fangirl/Fanboy":
			return 	{
				"Person" 			: None,
				"FanOf" 			: None,
				"Description"		: None,
				"Action"			: None,
				"Event"				: None,
				"Tagged_Friends" 	: None,
				"Location" 			: None,
				"Organization" 		: None,
				"Sentiment" 		: None,
				"Date"		 		: None,
				"Type"		 		: None,
				"Time"				: None,
				"Fandom"			: None,
			}
		elif persona == "The Gamer":
			return 	{
				"Person" 			: None,
				"Game" 				: None,
				"Type"		 		: None,	
				"FanOf" 			: None,
				"Activity"			: None,
				"Event"				: None,
				"Tagged_Friends" 	: None,
				"Location" 			: None,
				"Sentiment" 		: None,
				"Sentiment_Class" 	: None,
				"Date"				: None,
				"Time"				: None
			}