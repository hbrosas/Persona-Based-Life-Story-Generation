import MySQLdb
from models.post import Post
from models.semanticrelation import SemanticRelation
import dateutil.parser

class Database:
	def connectDB(self):
		host = "localhost"
		user = "root"
		password = "p@ssword"
		database = "ieappdb"
		db = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
		cursor = db.cursor()
		return cursor

	def feedSemRel(self, relationid, term_1, term_2):
		host = "localhost"
		user = "root"
		password = "p@ssword"
		database = "ieappdb"
		db = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
		cursor = db.cursor()
		cursor.execute(("""	INSERT INTO semantic_ontology (relation_id,term_1,term_2) 
		                	VALUES(%s,%s,%s) 
		                	WHERE NOT EXISTS (
		                		SELECT * FROM semantic_ontology 
		                		WHERE relation_id = $s AND term_1 LIKE $s AND term_2 LIKE $s
		                	) LIMIT 1;"""), (int(relationid), term_1, term_2,int(relationid), term_1, term_2))
		db.commit()

	def findRelation(self, relation):
		relid = -1
		db = Database()
		cursor = db.connectDB()
		cursor.execute("SELECT * FROM relations WHERE relation LIKE '" + relation + "';")
		rows = cursor.fetchall()

		for row in rows:
			relid = row[0]

		return relid

	def searchSemRel(self, term):
		semrel = []
		db = Database()
		cursor = db.connectDB()
		cursor.execute("SELECT * FROM semantic_ontology WHERE term_1 LIKE '" + term + "' OR term_2 LIKE '" + term + "';")
		rows = cursor.fetchall()

		for row in rows:
			s = SemanticRelation(row[0], row[1], row[2], row[3] )
			semrel.append(s)

		return semrel

	def searchTerm(self, term):
		semrel = []
		db = Database()
		cursor = db.connectDB()
		cursor.execute("SELECT * FROM semantic_ontology WHERE term_1 LIKE '" + term + "';")
		rows = cursor.fetchall()

		for row in rows:
			s = SemanticRelation(row[0], row[1], row[2], row[3] )
			semrel.append(s)

		return semrel

	def getPosts(self):
		posts = []
		db = Database()
		cursor = db.connectDB()
		cursor.execute("SELECT * FROM labelled_posts;")
		rows = cursor.fetchall()

		for row in rows:
			self.getDateTime(row[3])
			p = Post(row[0], row[1], row[2], row[4], row[3])
			posts.append(p)

		return posts

	def getPostsByLabel(self, persona):
		posts = []
		db = Database()
		cursor = db.connectDB()
		cursor.execute("SELECT * FROM labelled_posts WHERE label = '" + persona + "';")
		rows = cursor.fetchall()

		for row in rows:
			self.getDateTime(row[3])
			p = Post(row[0], row[1], row[2], row[4], row[3])
			posts.append(p)

		return posts

	def getDateTime(self, timestamp):
		timestamp = timestamp[:-5]
		print(timestamp)
		# d = dateutil.parser.parse(timestamp)
