from googletrans import Translator

class TGENTranslator:

	def translateQuery(self, query):
		translator = Translator(service_urls=['translate.google.com'])
		translated = translator.translate(query, src='tl', dest='en')
		# print("English Form: ", translated.text)
		return translated.text