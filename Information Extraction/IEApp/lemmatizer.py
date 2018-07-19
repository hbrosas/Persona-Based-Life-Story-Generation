import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

class Lemmatizer:
	nlp = spacy.load('en')
	feelings = ["acceptance", "admiration", "adoration", "affection", "afraid", "agitation", "agreeable", "aggressive", "aggravation", "agony", "alarm", "alienation", "amazement", "amusement", "anger", "angry", "anguish", "annoyance", "anticipation", "anxiety", "apprehension", "assertive", "assured", "astonishment", "attachment", "attraction", "awe", "disappointment", "disappointed"]

	lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)

	for f in feelings:
		lemma1 = lemmatizer(f, u'VERB')
		lemma2 = lemmatizer(f, u'NOUN')
		print("VERB: ", lemma1, " NOUN: ", lemma2)