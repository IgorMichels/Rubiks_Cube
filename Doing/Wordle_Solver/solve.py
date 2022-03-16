import re
import numpy as np
from random import choice
from itertools import product
from nltk.corpus import words
from Levenshtein import distance

def preprocessing():
	dict_words = {}
	for word in words.words():
		if len(word) not in dict_words:
			dict_words[len(word)] = [word.lower()]
		else:
			dict_words[len(word)].append(word.lower())
	
	return dict_words

def initial_guess(word_list):
	points = np.zeros((len(word_list)))
	for i, word in enumerate(word_list):
		if 'a' in word:
			points[i] += 1
		
		if 'e' in word:
			points[i] += 1
		
		if 'i' in word:
			points[i] += 1
		
		if 'o' in word:
			points[i] += 1
		
		if 'u' in word:
			points[i] += 1
		
	max_point = np.max(points)
	positions = np.where(points == max_point)
	suggestions = []
	for pos in positions:
		suggestions += [word_list[pos[0]]]
	
	return choice(suggestions)

def make_choice(word_list):
	distances = np.zeros((len(word_list), len(word_list)))
	for i in range(len(word_list)):
		for j in range(len(word_list)):
			distances[i, j] = distance(word_list[i], word_list[j])
			
	distances += distances.T
	distances = np.sum(distances, axis = 1)
	min_distance = np.min(distances)
	positions = np.where(distances == min_distance)
	suggestions = []
	for pos in positions:
		suggestions += [word_list[pos[0]]]
	
	return choice(suggestions)

def choose_word(word_list, have = {}, not_have = [' '], form = None):
	if form == None:
		n = str(len(word_list[0]))
		form = '\S{' + n + '}'
	
	suggests = []
	word_list = [word for word in re.findall(form, ' '.join(word_list))]
	if word_list == []:
		return None
	
	if ' ' not in not_have:
		not_have.append(' ')
	
	for word in word_list:
		out = False
		for letter in have.keys():
			if letter in not_have:
				not_have.remove(letter)
			
			if word.count(letter) < have[letter]:
				out = True
		
		for letter in not_have:
			if letter in word:
				out = True
		
		if not out:
			suggests += [word]
	
	if suggests == []:
		return None
	
	return make_choice(suggests)

def play():
	n = int(input('How many letters have the word?\n'))
	t = int(input('How many turns do you have?\n'))
	words = preprocessing()
	words = words[n]
	turns = 0
	have = {}
	not_have = []
	form = '.' * n
	while turns < t:
		signal = ''
		while not signal.startswith('y'):
			if signal.startswith('n'):
				words.remove(guess)
			
			if turns == 0:
				# guess = choose_word(words, have = have, not_have = not_have, form = form)
				guess = initial_guess(words)
			else:
				guess = choose_word(words, have = have, not_have = not_have, form = form)
			
			print()
			print(f'My guess is the word: {guess}')
			print()
			
			signal = input('Did this guess work? [y/n]\n').lower()
		
		included = []
		for pos, letter in enumerate(guess):
			ans = input(f'The letter {letter} is in the secret word? [y/n]\n').lower()
			if ans.startswith('n'):
				not_have.append(letter)
			else:
				if letter in included:
					have[letter] += 1
				else:
					have[letter] = 1
					included.append(letter)
				
				ans = input('Is this letter in its real position? [y/n]\n')
				if ans.startswith('y'):
					form = form[:pos] + letter + form[pos + 1:]
		
		words.remove(guess)
		if '.' not in form:
			return form
		
		turns += 1

play()
