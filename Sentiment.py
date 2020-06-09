import json

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import os


def analyze(article):
	"""Run a sentiment analysis request on text within a passed filename."""
	client = language.LanguageServiceClient()

	document = types.Document(
		content=article,
		type=enums.Document.Type.PLAIN_TEXT)
	annotations = client.analyze_sentiment(document=document)

	return annotations


if __name__ == '__main__':
	files = os.listdir('.')
	for file in reversed(files):
		if not file[-5:] == '.json':
			files.remove(file)
	print(files)
	for file in files:
		fi = open(file, 'r', encoding='utf8')

		json_articles = fi.read()

		fi.close()

		articles = json.loads(json_articles)

		for article in articles:
			annotations = analyze(article['content'])

			article['score'] = annotations.document_sentiment.score
			article['magnitude'] = annotations.document_sentiment.magnitude

			print('Analyzed article with id: {}'.format(article['id']))

			fo = open(file, 'w', encoding='utf8')
			fo.write(json.dumps(articles, indent=4))
			fo.close()


