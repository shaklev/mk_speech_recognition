with open('dic_words.txt', 'r') as dic:
	word_array = [];
	for word in dic:
		if word not in word_array:
			word_array.append(word)

with open ('new_words.txt', 'w') as words:
	for i in word_array:
		words.write(i)