import spacy
import re

class LikedPagesEvents:

	nlp = spacy.load('en')

	foodieCateg = ["Agriculture Company", "Company", "Food & Beverage Company", "Retail Company", "Tobacco Company", "Non-Governmental Organization", "Non-Profit Organization", "Organization", "Retail Company", "App Page", "Brand", "Food & Beverage Company", "Chef"]

	sportsCateg = ["Community Organization", "Community Services", "Company", "Non-Governmental Organization", "Non-Profit Organization", "Organization", "Retail Company", "App Page", "Brand", "Amateur Sports Team", "School Sports Team", "Sports League", "Sports Team", "Stadium", "Arena & Sports Venue", "Athlete", "Coach",]

	fanCateg = ["Automotive Company", "Biotechnology Company", "Cargo & Freight Company", "Community Organization", "Community Services", "Company", "Health/Beauty", "Non-Governmental Organization", "Non-Profit Organization", "Organization", "Political Organization", "Political Party", "Retail Company", "Telecommunication Company", "Tobacco Company", "Travel Company", "App Page", "Appliances", "Baby Goods/Kids Goods", "Bags/Luggage", "Brand", "Building Materials", "Camera/Photo", "Cars", "Clothing (Brand)", "Commercial Equipment", "Furniture", "Home Décor", "Household Supplies", "Jewelry/Watches"," Kitchen/Cooking", "Office Supplies", "Patio/Garden", "Pet Supplies", "Pharmaceuticals", "Phone/Tablet", "Product/Service", "Software", "Tools/Equipment", "Vitamins/Supplements", "Website", "Wine/Spirits", "Actor", "Artist", "Author", "Band", "Blogger", "Chef", "Comedian", "Dancer", "Entrepreneur", "Fashion Model", "Fictional Character", "Film Director", "Fitness Model", "Government Official", "Journalist", "Motivational Speaker", "Movie Character", "Musician", "News Personality", "Pet", "Photographer", "Political Candidate", "Politician", "Producer", "Public Figure", "Scientist", "Teacher", "Video Creator", "Writer", "Album", "Book", "Book Series", "Book Store", "Concert Tour", "Festival", "Fictional Character", "Library", "Literary Arts", "Magazine", "Movie", "Movie Character", "Movie Theater", "Movie/Television Studio", "Music Award", "Music Chart", "Music Video", "Performance & Event Venue", "Performance Art", "Performing Arts", "Podcast", "Radio Station", "Record Label", "Show", "Song", "Theatrical Play", "Theatrical Productions", "TV Channel", "TV Network", "TV Show", "TV/Movie Award"]

	gamerCateg = ["Community Organization", "Community Services", "Company", "Computer Company", "Internet Company", "Non-Governmental Organization", "Non-Profit Organization", "Organization", "Retail Company", "App Page", "Board Game", "Brand", "Computers (Brand)", "Electronics", "Games/Toys", "Phone/Tablet", "Product/Service", "Software", "Video Game", "Amateur Sports Team", "Sports League", "Sports Team", "Stadium", "Arena & Sports Venue", "School Sports Team", "Athlete", "Coach",]


	def extractLikedPages(self, data, persona):
		assertions = []
		ctr = 1

		for d in data:
			pageName = self.getPageName(d.liked_page)
			category = d.category

			if persona == "The Fangirl/Fanboy":
				if category in self.fanCateg:
					assertions.append(
						{
							"TYPE" : "likes",
							"VALUES" : {
								"PAGE" : pageName,
								"CATEGORY" : category,
								"PERSONA" : persona
							}
						}
					)

			elif persona == "The Foodie":
				if category in self.foodieCateg:
					assertions.append(
						{
							"TYPE" : "likes",
							"VALUES" : {
								"PAGE" : pageName,
								"CATEGORY" : category,
								"PERSONA" : persona
							}
						}
					)

			elif persona == "The Gamer":
				if category in self.gamerCateg:
					assertions.append(
						{
							"TYPE" : "likes",
							"VALUES" : {
								"PAGE" : pageName,
								"CATEGORY" : category,
								"PERSONA" : persona
							}
						}
					)

			elif persona == "The Sports Fanatic":
				if category in self.sportsCateg:
					assertions.append(
						{
							"TYPE" : "likes",
							"VALUES" : {
								"PAGE" : pageName,
								"CATEGORY" : category,
								"PERSONA" : persona
							}
						}
					)

			print("EXTRACTING PAGE: ", ctr, " of ", len(data))
			ctr += 1

		return assertions

	def getPageName(self, page):
		doc = self.nlp(page)
		page = ""

		for sent in doc.sents:
			result = re.search("He likes (.*)", sent.text)
			if result is not None:
				page = result.group(1)
			break

		return page

	def extractEvents(self, data, persona):
		assertions = []
		ctr = 1

		for d in data:
			event, rsvp = self.getEventDetails(d.original_event)
			if not event == "" and not rsvp == "":
				assertions.append(
					{
						"TYPE" : "events",
						"VALUES" : {
							"EVENT" : event,
							"RSVP" : rsvp,
							"PERSONA" : persona
						}
					}
				)

			print("EXTRACTING EVENT: ", ctr, " of ", len(data))
			ctr += 1

		return assertions

	def getEventDetails(self, page):
		doc = self.nlp(page)
		str = page.split('. ')
		event = ""
		rsvp = ""

		result = re.search("He is (.*) in (.*)", str[0])
		if result is not None:
			rsvp = result.group(1)
			event = result.group(2)

		return event, rsvp

	# foodieCateg = ["New American Restaurant", "American Restaurant",  "Burmese Restaurant",  "Cambodian Restaurant",  "Chinese Restaurant",  "Filipino Restaurant",  "Himalayan Restaurant",  "Japanese Restaurant",  "Korean Restaurant",  "Malaysian Restaurant",  "Mongolian Restaurant",  "Nepalese Restaurant",  "Singaporean Restaurant",  "Taiwanese Restaurant",  "Thai Restaurant", "Vietnamese Restaurant", "Bar & Grill", "Dive Bar", "Gastropub", "Gay Bar", "Sports Bar", "Tapas Bar & Restaurant", "Wine Bar", "Chicken Wings", "Cantonese Restaurant",  "Brewery", "Butcher", "Candy Store", "Convenience Store", "Cupcake Shop", "Deli", "Ethnic Grocery Store", "Farmers Market", "Fruit & Vegetable Store", "Grocery Store", "Health Food Store", "Liquor Store", "Market", "Meat Shop", "Specialty Grocery Store", "Bakery", "Beer Garden", "Brewery", "Cafe", "Cafeteria", "Coffee Shop", "Cupcake Shop", "Donuts & Bagels", "Farmers Market", "Food Stand", "Frozen Yogurt Shop", "Ice Cream Parlor", "Restaurant", "Restaurant Wholesale", "Salad Bar", "Smoothie & Juice Bar", "Sports Bar", "Tea Room", "Hot Dog Stand",  "Afghani Restaurant", "African Restaurant", "American Restaurant", "Argentine Restaurant", "Asian Fusion Restaurant", "Asian Restaurant", "Bar & Grill", "Barbecue Restaurant", "Basque Restaurant", "Belgian Restaurant", "Brazilian Restaurant", "Breakfast & Brunch Restaurant", "British Restaurant", "Buffet Restaurant", "Burger Restaurant", "Cafe", "Cajun & Creole Restaurant", "Canadian Restaurant", "Caribbean Restaurant", "Chicken Restaurant", "Continental Restaurant", "Crêperie", "Cuban Restaurant", "Deli", "Dessert Restaurant", "Dim Sum Restaurant", "Diner", "Drive In Restaurant", "Ethiopian Restaurant", "Family Style Restaurant", "Fast Food Restaurant", "Fine Dining Restaurant", "Fish & Chips Shop", "Fondue Restaurant", "French Restaurant", "Gastropub", "German Restaurant", "Gluten-Free Restaurant", "Greek Restaurant", "Halal Restaurant", "Hawaiian Restaurant", "Health Food Restaurant", "Hot Dog Joint", "Hungarian Restaurant", "Indian Restaurant", "Indonesian Restaurant", "International Restaurant", "Irish Restaurant", "Italian Restaurant", "Kosher Restaurant", "Late Night Restaurant", "Latin American Restaurant", "Lebanese Restaurant", "Live & Raw Food Restaurant", "Mediterranean Restaurant", "Mexican Restaurant",  "Middle Eastern Restaurant", "Modern European Restaurant", "Moroccan Restaurant", "Pakistani Restaurant", "Persian Restaurant", "Peruvian Restaurant", "Pizza Place", "Polish Restaurant", "Polynesian Restaurant", "Portuguese Restaurant", "Russian Restaurant", "Sandwich Shop", "Scandinavian Restaurant", "Seafood Restaurant", "Soul Food Restaurant", "Soup Restaurant", "Southern Restaurant", "Southwestern Restaurant", "Spanish Restaurant", "Steakhouse", "Take Out Restaurant", "Tapas Bar & Restaurant", "Tex-Mex Restaurant", "Turkish Restaurant", "Vegetarian & Vegan Restaurant", "Pho Restaurant", "Restaurant Wholesale", "Ramen Restaurant", "Sushi Restaurant"]

	# sportsCateg = ["Race Track", "Sports Venue & Stadium", "Sports Promoter", "Race Cars", "Ski & Snowboard School", "Sports Instruction", "Sportswear", "Shoe Store",  "Auditorium", "Beach", "Boating", "Fishing", "Island", "Mountain", "Surfing Spot", "Water Park", "Sporting Goods Store", "Archery", "Batting Cage", "Boat Rental", "Cheerleading", "Driving Range", "Fitness Center", "Golf Course", "Gun Range", "Gym", "Hot Air Balloons", "Hunting and Fishing", "Ice Skating", "Martial Arts", "Miniature Golf", "Mountain Biking", "Outdoor Recreation", "Paintball", "Personal Trainer", "Physical Fitness", "Pool & Billiards", "Racquetball Court", "Rafting", "Recreation Center", "Recreation Center", "Rock Climbing", "Scuba Diving", "Ski & Snowboard School", "Ski Resort", "Sky Diving", "Sports Center", "Sports Club", "Sports Instruction", "Swimming Pool", "Tennis", "Yoga & Pilates"]

	# fanCateg = ["Amusement", "Amusement Park Ride", "Art Gallery", "Bowling Alley", "Casino", "Circus", "Comedy Club", "Concert Venue", "Movie Theatre", "Museum", "Newspaper", "Orchestra", "Performance Venue", "Race Track", "Rodeo", "Social Club", "Symphony", "Theatre", "Theme Park", "Ticket Sales", "Tourist Attraction", "Zoo & Aquarium", "Advertising Agency", "Architect", "Art Restoration", "Artistic Services", "Broadcasting & Media Production", "Entertainment Service", "Fashion Designer", "Graphic Design", "Image Consultant", "Market Research Consultant", "Marketing Consultant", "Modeling Agency", "Movie & Television Studio", "Music Production", "Photographer", "Photographic Services & Equipment", "Public Relations", "Publisher", "Screen Printing & Embroidery", "Trophies & Engraving", "Web Design", "Web Development", "Accessories Store", "Bridal Shop", "Children's Clothing Store", "Costume Shop", "Formal Wear", "Men's Clothing Store", "Swimwear", "Women's Clothing Store", "Automation Services", "Biotechnology", "Commercial & Industrial Equipment", "Elevator Services", "Engineering Service", "Fire Protection", "Gas & Chemical Service", "Ice Machines", "Manufacturing", "Mattress Manufacturing", "Mattress Wholesale", "Metals", "Petroleum Services", "Plastics", "Refrigeration", "Robotics", "Storage Service", "Textiles", "Vending Machine Service", "Warehouse", "Outlet Store", "Pawn Shop", "Rent to Own Store", "Thrift or Consignment Store", "Bands & Musicians", "Bartending Service", "Caterer", "DJ", "Entertainer", "Event Planner", "Event Venue", "Party Supplies", "Wedding Planning", "Furniture Repair", "Collectibles Store", "Cultural Gifts Store", "Seasonal Store",  "Laser Hair Removal", "Appliances", "Blinds & Curtains", "Cabinets & Countertops", "Carpenter", "Carpet & Flooring Store", "Carpet Cleaner", "Cleaning Service", "Concrete Contractor", "Construction Service & Supply", "Contractor", "Damage Restoration Service", "Deck & Patio", "Electrician", "Excavation & Wrecking", "Fireplaces", "Fireproofing", "Garage Door Services", "Garden Center", "Gardener", "Glass Service", "Hardware & Tools Service", "Hardware Store", "Heating, Ventilating & Air Conditioning", "Home Cleaning", "Home Decor", "Home Inspection", "Home Security", "Home Theater Store", "Home Window Service", "Housewares", "Interior Designer", "Kitchen Construction", "Kitchen Supplies", "Landscaping", "Lighting Fixtures", "Locksmith", "Masonry", "Mattresses & Bedding", "Mobile Homes", "Mover", "Painter", "Paving & Asphalt Service", "Pest Control", "Plumber", "Portable Building Service", "Portable Toilet Rentals", "Property Management", "Roofer", "Sewer Service", "Solar Energy Service", "Storage", "Surveyor", "Swimming Pool Maintenance", "Tools Service", "Upholstery Service", "Wallpaper", "Well Water Drilling Service", "Art Museum", "History Museum", "Modern Art Museum", "Musical Instrument Store", "Adult Entertainment","Bar","Dance Club","Hookah Lounge","Jazz Club","Karaoke","Lounge","Night Club","Pub", "Arts & Marketing","Automotive","Business Services","Cable & Satellite Service","Commercial & Industrial","Event Planning","Financial Services","Law Practice","Lifestyle Services","Medical & Health","Outdoor Services","Pet Service","Real Estate","Repair Service","Research Service","Safety & First Aid Service","Security","Spa, Beauty & Personal Care","Supply & Distribution Services", "Antiques & Vintage", "Arts & Crafts Supply Store", "Bank", "Big Box Retailer", "Bike Shop", "Book Store", "Camera Store", "Clothing Store", "Comic Book Store", "Computers & Electronics", "Convenience Store", "Cosmetics & Beauty Supply", "Department Store", "Discount Store", "Drugstore", "Dry Cleaner", "DVD & Video Store", "Eye Wear", "Fireworks Retailer", "Florist", "Food & Grocery", "Furniture Store", "Gift Shop", "Gun Store", "Home Improvement", "Jewelry Store", "Laundromat", "Luggage Service", "Mobile Phone Shop", "Music Store", "Office Supplies", "Other", "Outdoor Equipment Store", "Party Center", "Pet Store", "Shopping District", "Shopping Mall", "Signs & Banner Service", "Sporting Goods Store", "Toy Store", "Wholesale & Supply Store", "Winery & Vineyard", "Aromatherapy", "Barber Shop", "Beauty Salon", "Cosmetics & Beauty Supply", "Day Spa", "Esthethics", "Hair Removal", "Hair Replacement", "Hair Salon", "Hairpieces & Extensions", "Health Spa", "Makeup Artist", "Massage", "Medical Spa", "Nail Salon", "Skin Care", "Spa", "Tanning Salon", "Tattoo & Piercing", "Teeth Whitening", "Wig Store", "Museum", "Cruise Excursions", "Eco Tours", "Rental Shop", "Tour Company", "Tour Guide", "Tourist Information", "Public Figure"]

	# gamerCateg = ["Arcade", "Go Karting", "Laser Tag", "Entertainment Service", "Cyber Cafe", "Internet Cafe", "Video Games", "Video Game", "Electronics Store", "Computer Store", "Games/Toys"]