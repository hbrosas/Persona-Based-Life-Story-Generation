from google import google
from googleapiclient.discovery import build
from yboss import YBoss
import string
import pandas as pd
import collections
import string
from sklearn.feature_extraction import stop_words
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import Normalizer
from context.conceptnet import ConceptNet
from pws import Google
from pws import Bing
import pprint
import time


class GoogleSearch:

	 # pip install py-web-search

	def searchWeb(self, query):
		print(Google.search(query="hello world", num=5, start=0, sleep=True, country_code="jp"))
		# print(Bing.search('hello world', 5, 0))

	# API KEY: AIzaSyCNzfgpu7wlRH1JtDKdPzjKYYQmMDYOmPA
	# SEARCH ENGINE ID: 009245651788415609720:3p8uar0xazs
	# pip install --upgrade google-api-python-client

	def searchGoogleAPI(self, query):
		service = build("customsearch", "v1", developerKey="AIzaSyCNzfgpu7wlRH1JtDKdPzjKYYQmMDYOmPA")

		res = service.cse().list(
		      q=query,
		      cx='009245651788415609720:3p8uar0xazs',
		    ).execute()

		pprint.pprint(res)

	def search(self, query):
		search_results = google.search(query)
		time.sleep(10)
		description = ""
		for result in search_results:
			description = description + " " + result.name + " " + result.description
		freq = self.tf_idf(description)
		# print("Freq: ", freq)
		return freq

	def isPerson(self, query):
		result = self.search(query)
		if not result is None:
			if "people" in result:
				return True
			else:
				return False

	def getFood(self, mentions):
		if not mentions is None:
			for m in mentions:
				terms = self.search(str(m))
				print("Mention: ", str(m))
				print("Terms: ", terms)


	################################################################################

	def dataCleaning(self, description):
		nopunc = [char for char in description if char not in string.punctuation]
		nopunc = ''.join(nopunc)
		return [word for word in nopunc.split() if word.lower() not in stop_words.ENGLISH_STOP_WORDS]

	def stemming_tokenizer(self, text):
		stemmer = PorterStemmer()
		return [stemmer.stem(w) for w in word_tokenize(text)]

	def feature_extraction(self, train_texts):
		# TfidfVectorizer is equivalent to CountVectorizer followed by TfidfTransformer.
		tfidf_vectorizer = TfidfVectorizer(analyzer= self.stemming_tokenizer, ngram_range=(1, 4))
		train_texts_tfidf = tfidf_vectorizer.fit_transform(train_texts)
		return train_texts_tfidf, tfidf_vectorizer

	def get_most_common_terms(self, train_texts):
		count_vectorizer = CountVectorizer()
		try:
			train_texts_count = count_vectorizer.fit_transform(train_texts)
			occ = np.asarray(train_texts_count.sum(axis=0)).ravel().tolist()
			counts_df = pd.DataFrame({'term': count_vectorizer.get_feature_names(), 'occurrences': occ})

			sortedValues = counts_df.sort_values(by='occurrences', ascending=False).head(30)
			return sortedValues['term']
		except:
			return None

	# Main Function for Term Frequency
	def tf_idf(self, description):
		description = self.dataCleaning(description)
		count_vectorizer = self.get_most_common_terms(description)

		if not count_vectorizer is None:
			try:
				termFreq = []
				for x in range(0, 30):
					termFreq.append(count_vectorizer.iloc[x])

				# print("TERMS: ", termFreq)
				return termFreq
			except:
				return None
		else:
			return None





