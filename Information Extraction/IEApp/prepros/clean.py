# This function contains the main process of data pre-processing

from prepros.spellcheck import SpellChecker
from prepros.emojiremove import EmojiRemove
from prepros.dictionaries.apostrophe_dic import ApostropheDictionary
from prepros.dictionaries.slang_dic import SlangDictionary
from context.npextractor import NPExtractor
from context.translator import TGENTranslator
from context.googlesearch import GoogleSearch
import spacy
import html.parser
import itertools
import re

"""
	From  Source: https://www.analyticsvidhya.com/blog/2014/11/text-data-cleaning-steps-python/ (Not all)
	FINAL METHOD:
	1. Escape HTML Characters
	2. Spell Correction for Tagalog Words
		- if it does not have an entity yet, search through semantic ontology and get if it has any entity
	3. Lowercase everything first because of lookup dictionary
	4. Google Translate
	5. Apostrophe Lookup
	8. Removal of Punctuations except “.”, “,”, ”?”
	9. Removal of Expressions. Ex. Haha, Hehe, Huhu
	10. Split Attached Words
	11. Slang Lookup
	12. Standardizing words
	13. Grammar Checking
	*14. Spelling Correction for English Words
"""

class Clean:

	nlp = spacy.load('en')
	gsearch = GoogleSearch()
	profile = None
	sc = SpellChecker()
	aposdic = ApostropheDictionary()
	slangdic = SlangDictionary()
	translator = TGENTranslator()

	def cleanData(self, posts, profile):
		self.profile = profile
		cleaned_posts = []
		ctr = 0
		for p in posts:
			p = self.extractElements(p)
			if p is not None:
				# Comment this
				# if not p.story == "":
				# 	print("CLEANED STORY: ", p.story)
					
				if not p.post == "":
					p.post = self.translate(p.post)
					# Comment this
					# print("CLEANED POST: ", p.post)

				if not p.sentiment == "":
					p = self.clean(2, p)
					# Comment this
					# print("CLEANED SENTIMENT: ", p.sentiment)

				# print("POST: ", p.original_post)
				# print("STORY: ", p.story)
				# print("SHARED POST CAPTION: ", p.post)
				# print("SENTIMENT: ", p.sentiment)

				cleaned_posts.append(p)
			ctr += 1
			print("PRE-PROCESSING: ", ctr, " of ", len(posts))
			
		return cleaned_posts

	def extractElements(self, p):
		post = p.original_post

		hashtags = [i[1:] for i in post.split() if i.startswith("#")]
		mentions = [i[1:] for i in post.split() if i.startswith("@")]

		post = re.sub('#([A-Za-z0-9_]+)', '', post)
		post = re.sub('@([A-Za-z0-9_]+)', '', post)

		# print("Hashtags: ", hashtags)
		# print("Mentions: ", mentions)

		# print("Post: ", post)

		# Get Story, Post, Sentiment
		p.story, p.post, p.sentiment = self.dividePost(post)
		p.hashtags = hashtags
		p.mentions = mentions

		if p.story == "1" and p.post == "0" and p.sentiment == "1":
			return None
		else:
			# Get Tokens with Name Entity
			# nlp = spacy.load('en')
			person = []
			doc = self.nlp(p.sentiment)
			for ent in doc.ents:
				if ent.label_ == "PERSON":
					if self.gsearch.isPerson(ent.text):
						person.append(ent.text)

			# print("PERSON: ", person)
			p.person = person

			# print("Story: ", p.story)
			# print("Post: ", p.post)
			# print("Sentiment: ", p.sentiment)

			return p

	def clean(self, level, post):
		text = post.sentiment

		#1 Escape HTML Characters
		html_parser = html.parser.HTMLParser()
		text = html_parser.unescape(text)

		#2 Standardize
		text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
		# print("STANDARDIZED: ", text)

		#3 Removal of Expression. Ex. Haha, Hehe, Huhu
		text = re.sub('(a*ha+h[ha]*|(?:l+o+)+l+|e*he+h[he]*|i*hi+h[hi]*|o*ho+h[ho]*|u*hu+h[hu]*)', '', text)
		text = re.sub('(A*HA+H[HA]*|(?:L+O+)+L+|E*HE+H[HE]*|I*HI+H[HI]*|O*HO+H[HO]*|U*HU+H[HU]*)', '', text)
		# print("Removed Expressions: ", text)

		# Remove New Line
		text = EmojiRemove.removeNewLine(text)
		# print("Removed New Lines: ", text)

		# Remove Emoticons
		text = EmojiRemove.remove_emoji(text)
		# print("Removed Emojis: ", text)

		# Remove Special Characters
		text = EmojiRemove.remove_specialChars(text)
		# print("Removed Special Characters: ", text)

		fromIsApos = False
		fromIsHyphen = 0
		hyphenPattern = re.compile(u"-([A-Za-z0-9_]+)")
		doc = self.nlp(text)
		text = ""

		for x in range(0, len(doc)):
			if fromIsApos or fromIsHyphen > 0:
				# Ignore next token
				fromIsApos = False
				fromIsHyphen -= 1
			else:
				if not x >= len(doc)-1:
					key = doc[x].text + doc[x+1].text
					# print("Apos Key: ", key)
					# Apostrophe Lookup
					isApos = self.aposdic.lookup(key.lower())

					if not isApos == None:
						text += isApos + " "
						fromIsApos = True

				if not x > (len(doc)-3) and not fromIsApos:
					key2 = doc[x].text + doc[x+1].text + doc[x+2].text
					# Hyphen Lookup
					if re.match(hyphenPattern, (doc[x+1].text + doc[x+2].text)):
						# print((doc[x+1].text + doc[x+2].text))
						text += key2 + " "
						fromIsHyphen = 2
					else:
						text += doc[x].text + " "
				else:
					if not fromIsApos:
						text += doc[x].text + " "
		
		# print("Apostrophe & Hyphen Lookup: ", text)

		#4 Slang Lookup
		text = self.slangdic.replace(text.lower())
		# print("Slang Lookup: ", text)

		# Remove URLS and Emails
		text = EmojiRemove.removeExtras(text)
		# print("Removed URLs and Emails: ", text)

		# Whitespaces
		text = EmojiRemove.removeWhitespaces(text)
		# print("Removed Whitespaces: ", text)

		# Spell Correct
		text = self.sc.spell(text, post)

		# Google Translate
		text = self.translator.translateQuery(text)

		post.sentiment = text
		# print("CLEANED SENTIMENT: ", text)

		# Language Check
		# tool = language_check.LanguageTool('en-US')
		# matches = tool.check(post) 
		# print(language_check.correct(post, matches))

		return post

	def translate(self, query):
		# Google Translate
		query = ''.join(''.join(s)[:2] for _, s in itertools.groupby(query))
		query = re.sub('(a*ha+h[ha]*|(?:l+o+)+l+|e*he+h[he]*|i*hi+h[hi]*|o*ho+h[ho]*|u*hu+h[hu]*)', '', query)
		query = re.sub('(A*HA+H[HA]*|(?:L+O+)+L+|E*HE+H[HE]*|I*HI+H[HI]*|O*HO+H[HO]*|U*HU+H[HU]*)', '', query)
		query = EmojiRemove.removeNewLine(query)
		query = EmojiRemove.remove_emoji(query)
		return self.translator.translateQuery(query)

	def dividePost(self, post):
		name = self.profile.name
		storyPattern = re.compile(u"^(%s shared)|^(%s is)|^(%s added)|^(%s was)|^(%s updated)" % (name, name, name, name, name))
		postPattern = re.compile(u"^(The post says)|^(%s the post says)|^(\s+The post says)")
		sentPattern = re.compile(u"^(He says)|^(he says)|^( he says)")

		story = ""
		posttxt = ""
		sentiment = ""

		try:
			# nlp = spacy.load('en')
			doc = self.nlp(post)

			level = -1
			for s in doc.sents:
				if re.match(storyPattern, s.text):
					level = 0
				elif re.match(postPattern, s.text):
					level = 1
				elif re.match(sentPattern, s.text):
					level = 2
				else:
					if level == -1:
						sentiment += s.text + " "

				if level == 0:
					story += s.text + " "
				elif level == 1:
					posttxt += s.text + " "
				elif level == 2:
					sentiment += s.text + " "

			posttxt = postPattern.sub(r'', posttxt)
			posttxt = EmojiRemove.removeNewLine(posttxt)
			sentiment = sentPattern.sub(r'', sentiment)
			sentiment = EmojiRemove.removeNewLine(sentiment)
			sentiment = sentiment.replace("the post says", "")
			sentiment = sentiment.replace("he says", "")

			return story, posttxt, sentiment
		except:
			return "1", "0", "1"


		



	