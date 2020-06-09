fi = open("Divorce - NYT.html", 'r', encoding='utf8')

content = fi.read()
depth = 0
i = 0

while i < len(content):
	if content[i] == '<' and content[i+1] == '!':
		i += 1
		continue
	if content[i] == '<' and content[i+1] != '/':
		while content[i-1] == '\t' or content[i-1] == '\n' or content[i-1] == ' ':
			content = content[:i-1] + content[i:]
			i -= 1
		content = content[:i] + '\n' + ('\t' * depth) + content[i:]
		i += depth + 1
		depth += 1
	if content[i] == '<' and content[i+1] == '/':
		depth -= 1
		content = content[:i] + '\n' + '\t' * depth + content[i:]
		i += depth + 1
	if content[i] == '/' and content[i+1] == '>':
		depth -= 1
	i += 1

fo = open('test.html', 'w', encoding='utf8')

fo.write(content)
