import nltk
from nltk import word_tokenize
import re
import os
import io

# Alternative you can execute this command in the terminal: cat sentences.txt | tr ' ' '\n' | sort | uniq > words.txt

def separate_unique_words():
	unique = []
	with open ('sentences.txt', 'r') as f:
		content = f.read()
		# content = re.sub(r'[^\w\s]','',content).lower()

		words = word_tokenize(content)

		for i in words:
			if i not in unique:
				unique.append(i)
	return unique		

unique = separate_unique_words()


for w in unique:
	print(w)
	with io.open('separate_words.txt', 'w', encoding='utf-8') as f:
		print(w)
		f.write(w + '\n')	