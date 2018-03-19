from normalizr import Normalizr

class Normalizer:

	def normalize(self, post):
		normie = Normalizr(language='en')
		normalizations = [
			'remove_extra_whitespaces',
			'remove_accent_marks',
			('replace_emojis', {'replacement': ''}),
			('replace_urls', {'replacement': ''}),
			# ('replace_punctuation', {'replacement': ''}),
			# ('replace_symbols', {'replacement': ''}),
		]

		post = normie.normalize(post, normalizations)
		return post