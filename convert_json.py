import os
import json
import xlsxwriter


files = os.listdir('.')
for file in reversed(files):
	if not file[-5:] == '.json':
		files.remove(file)

for file in files:
	fi = open(file, 'r', encoding='utf8')
	json_articles = fi.read()
	articles = json.loads(json_articles)
	workbook = xlsxwriter.Workbook(file.replace('json', 'xlsx'))
	worksheet = workbook.add_worksheet()
	worksheet.write(0, 0, 'Name')
	worksheet.write(0, 1, 'Date')
	worksheet.write(0, 2, 'Author')
	worksheet.write(0, 3, 'Word Count')
	worksheet.write(0, 4, 'Sentence Count')
	worksheet.write(0, 5, 'Score')
	worksheet.write(0, 6, 'Magnitude')
	worksheet.write(0, 7, 'First Sentence')

	for i in range(1, len(articles)+1):
		worksheet.write(i, 0, articles[i - 1]['name'])
		worksheet.write(i, 1, articles[i - 1]['date'])
		worksheet.write(i, 2, articles[i - 1]['author'])
		worksheet.write(i, 3, len(articles[i - 1]['content'].split(' ')))
		worksheet.write(i, 4, articles[i - 1]['content'].count('.'))
		worksheet.write(i, 5, articles[i - 1]['score'])
		worksheet.write(i, 6, articles[i - 1]['magnitude'])
		temp_end_first_sentence = articles[i - 1]['content'].find('.')
		final_end_first_sentence = articles[i - 1]['content'].find('.')
		if temp_end_first_sentence == -1:
			worksheet.write(i, 7, articles[i - 1]['content'])
		else:
			while True:
				if articles[i - 1]['content'][temp_end_first_sentence - 2] == ' ':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence - 2] == '.':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence + 1: temp_end_first_sentence + 4].lower() == 'com':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence - 2: temp_end_first_sentence].lower() == 'jr':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence - 2: temp_end_first_sentence].lower() == 'mr':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence - 2: temp_end_first_sentence].lower() == 'ms':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence - 3: temp_end_first_sentence].lower() == 'mrs':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence - 2: temp_end_first_sentence].lower() == 'dr':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence - 4: temp_end_first_sentence].lower() == 'prof':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence - 3: temp_end_first_sentence].lower() == 'p.m':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence - 2: temp_end_first_sentence].lower() == 'pm':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if articles[i - 1]['content'][temp_end_first_sentence - 2: temp_end_first_sentence].lower() == 'no':
					temp_end_first_sentence = articles[i - 1]['content'].find('.', temp_end_first_sentence + 1)
				if temp_end_first_sentence == final_end_first_sentence:
					break
				else:
					final_end_first_sentence = temp_end_first_sentence
					print(temp_end_first_sentence)
					print(articles[i - 1]['content'])
			worksheet.write(i, 7, articles[i-1]['content'][:final_end_first_sentence + 1])

	workbook.close()
