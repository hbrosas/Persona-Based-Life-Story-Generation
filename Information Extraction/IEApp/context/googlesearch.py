from google import google
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

class GoogleSearch:

	def search(self, query):
		search_results = google.search(query)
		description = ""
		for result in search_results:
			description = description + " " + result.name + " " + result.description
		freq = self.tf_idf(description)
		return freq

	def dataCleaning(self, description):
		nopunc = [char for char in description if char not in string.punctuation]
		nopunc = ''.join(nopunc)
		return [word for word in nopunc.split() if word.lower() not in stop_words.ENGLISH_STOP_WORDS]

	def stemming_tokenizer(self, text):
		stemmer = PorterStemmer()
		return [stemmer.stem(w) for w in word_tokenize(text)]

	def feature_extraction(self, train_texts):
		# TfidfVectorizer is equivalent to CountVectorizer followed by TfidfTransformer.
		tfidf_vectorizer = TfidfVectorizer(analyzer= self.stemming_tokenizer, ngram_range=(1, 2))
		train_texts_tfidf = tfidf_vectorizer.fit_transform(train_texts)
		return train_texts_tfidf, tfidf_vectorizer

	def get_most_common_terms(self, train_texts):
		count_vectorizer = CountVectorizer()
		train_texts_count = count_vectorizer.fit_transform(train_texts)
		occ = np.asarray(train_texts_count.sum(axis=0)).ravel().tolist()
		counts_df = pd.DataFrame({'term': count_vectorizer.get_feature_names(), 'occurrences': occ})

		sortedValues = counts_df.sort_values(by='occurrences', ascending=False).head(10)
		return sortedValues['term']

	# Main Function for Term Frequency
	def tf_idf(self, description):
		description = self.dataCleaning(description)
		count_vectorizer = self.get_most_common_terms(description)

		termFreq = []
		for x in range(0, 10):
			termFreq.append(count_vectorizer.iloc[x])

		print("TERMS: ", termFreq)
		return termFreq





