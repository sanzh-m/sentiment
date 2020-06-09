import os
import re
import json
import datetime
from calendar import month_name
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
	def error(self, message):
		pass

	def __init__(self):
		super().__init__()
		self.reading_article = False
		self.name_read = False
		self.author_read = False
		self.date_read = False
		self.article_started = False
		self.word_count_read = False
		self.previous_tag = ''
		self.current_name = ''
		self.current_author = ''
		self.current_date = ''
		self.current_article = ''
		self.p = re.compile('[a-zA-Z0-9]{25}')
		self.article_count = 0
		self.h1_count = 0
		self.articles = []

	def handle_starttag(self, tag, attrs):
		if tag == 'h1' or tag == 'b':
			if self.reading_article and not self.author_read and self.previous_tag == 'h1':
				self.name_read = False
			elif not self.reading_article and not self.article_started and not self.author_read and not self.date_read:
				self.reading_article = True
				self.h1_count += 1
			else:
				raise Exception('Problem, chief')
			print('starting read')
		self.previous_tag = tag

	def handle_data(self, data):
		if self.reading_article:
			if not self.name_read:
				self.current_name += data + ' '
				self.name_read = True
				print('got the name - ' + self.current_name)
			else:
				if not self.author_read:
					if data.startswith('By '):
						self.current_author = data.replace('By ', '', 1)
						if ' words' in self.current_author:
							if '; ' in self.current_author:
								words = self.current_author.split(' ')
								self.current_author = self.current_author[:self.current_author.index(';')]
								current_index = words.index('words')
								if words.count('words') == 1 and words[current_index - 1].replace(',', '').isnumeric():
									self.word_count_read = True
								elif words.count('words') > 1:
									while 'words' in words[current_index + 1:]:
										if words[current_index - 1].replace(',', '').isnumeric():
											self.word_count_read = True
											break
										else:
											current_index = 2 + words[current_index + 1:].index('words')
									if not self.word_count_read:
										if words[current_index - 1].replace(',', '').isnumeric():
											self.word_count_read = True
							else:
								words = self.current_author.split(' ')
								current_index = words.index('words')
								if words.count('words') == 1 and words[current_index - 1].replace(',', '').isnumeric():
									self.current_author = ' '.join(words[:current_index - 1])
									self.word_count_read = True
								elif words.count('words') > 1:
									while 'words' in words[current_index + 1:]:
										if words[current_index - 1].replace(',', '').isnumeric():
											self.word_count_read = True
											break
										else:
											current_index = 2 + words[current_index + 1:].index('words')
									if not self.word_count_read:
										if words[current_index - 1].replace(',', '').isnumeric():
											self.word_count_read = True
						self.author_read = True
					elif 'words' in data:
						self.current_author = 'No Author'
						self.author_read = True
						words = data.split(' ')
						current_index = words.index('words')
						if words.count('words') == 1 and words[current_index - 1].replace(',', '').isnumeric():
							self.word_count_read = True
						elif words.count('words') > 1:
							while 'words' in words[current_index + 1:]:
								if words[current_index - 1].replace(',', '').isnumeric():
									self.word_count_read = True
									break
								else:
									current_index = 2 + words[current_index + 1:].index('words')
							if not self.word_count_read:
								if words[current_index - 1].replace(',', '').isnumeric():
									self.word_count_read = True
						if len([i for i in words if i in month_name]):
							pass
				elif self.author_read and not self.word_count_read:
					if ' words' in data:
						words = data.split(' ')
						current_index = words.index('words')
						if words.count('words') == 1 and words[current_index - 1].replace(',', '').isnumeric():
							self.word_count_read = True
						elif words.count('words') > 1:
							while 'words' in words[current_index + 1:]:
								if words[current_index - 1].replace(',', '').isnumeric():
									self.word_count_read = True
									break
								else:
									current_index = 2 + words[current_index + 1:].index('words')
							if not self.word_count_read:
								if words[current_index - 1].replace(',', '').isnumeric():
									self.word_count_read = True
						if len([i for i in words if i in month_name]):
							pass
				elif self.word_count_read and not self.date_read:
					if 'words' not in data:
						date = data.split(' ')[0] + ' ' + data.split(' ')[1] + ' ' + data.split(' ')[2]
						self.current_date = datetime.datetime.strptime(date, '%d %B %Y').strftime('%d/%m/%Y')
						self.date_read = True
				elif self.date_read and not self.article_started:
					if 'copyright' in data.lower() or '©' in data:
						self.article_started = True
				elif self.article_started:
					words = data.split(' ')
					if len(words) > 1 and words[-2] == 'Document' and self.p.match(words[-1]):
						self.articles.append({
							'id': self.article_count, 'name': self.current_name,
							'content': self.current_article, 'author': self.current_author,
							'date': self.current_date
						})
						self.reading_article = False
						self.name_read = False
						self.article_started = False
						self.date_read = False
						self.author_read = False
						self.word_count_read = False
						self.current_name = ''
						self.current_article = ''
						self.current_author = ''
						self.current_date = ''
						self.article_count += 1
					else:
						self.current_article += ' ' + data
				else:
					raise Exception('Problem, chief, i\'m working on this data - ' + data)


files = os.listdir('.')
years = []
NYT12_13 = []
NYT13_14 = []
WP12_13 = []
WP13_14 = []
Divorce_NYT = ''
Divorce_WP = ''
for file in reversed(files):
	if not file[-5:] == '.html':
		files.remove(file)

for file in files:
	if 'NYT' in file and '12-13' in file:
		NYT12_13.append(file)
	elif 'NYT' in file and '13-14' in file:
		NYT13_14.append(file)
	elif 'WP' in file and '12-13' in file:
		WP12_13.append(file)
	elif 'WP' in file and '13-14' in file:
		WP13_14.append(file)
	elif 'NYT' in file and 'Divorce' in file:
		Divorce_NYT = file
	elif 'WP' in file and 'Divorce' in file:
		Divorce_WP = file

years.append(NYT12_13)
years.append(NYT13_14)
years.append(WP12_13)
years.append(WP13_14)

for year in years:
	year_name = year[0][:3].replace(' ', '') + year[0][year[0].find(' ') + 1: year[0].find(' ') + 6]
	parser = MyHTMLParser()

	for part in year:
		print(part)
		fi = open(part, 'r', encoding='utf8')
		content = fi.read()
		parser.feed(content)

	json_articles = json.dumps(parser.articles, indent=4)
	del parser
	fo = open(year_name + '.json', 'w', encoding='utf8')

	fo.write(json_articles)

	fo.close()

parser = MyHTMLParser()

print(Divorce_NYT)
fi = open(Divorce_NYT, 'r', encoding='utf8')
content = fi.read()
parser.feed(content)

json_articles = json.dumps(parser.articles, indent=4)
del parser
fo = open('Divorce_NYT' + '.json', 'w', encoding='utf8')

fo.write(json_articles)

fo.close()

parser = MyHTMLParser()

print(Divorce_WP)
fi = open(Divorce_WP, 'r', encoding='utf8')
content = fi.read()
parser.feed(content)

json_articles = json.dumps(parser.articles, indent=4)
del parser
fo = open('Divorce_WP' + '.json', 'w', encoding='utf8')

fo.write(json_articles)

fo.close()
