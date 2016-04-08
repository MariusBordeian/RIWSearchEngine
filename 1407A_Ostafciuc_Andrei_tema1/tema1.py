from bs4 import BeautifulSoup
import mmh3
import json
import nltk
import os
import sys


stopWords = []
exceptions = []
tags = {'NN': 'n', 'NNS': 'n', 'NNP': 'n', 'NNPS': 'n'}


def getFiles(path):
	files = []
	path = os.path.abspath(path)
	if os.path.isfile(path):
		extension = os.path.splitext(path)[1].lower()
		if extension == '.html' or extension == '.htm' or extension == '.txt': # extension to filter files on
			files.append(path)
	else:
		content = os.listdir(path)
		for f in content:
			local = getFiles(path + '\\' + f)
			for l in local:
				files.append(l)
	return files


def hashFiles(files):
	fileMap = {}
	for f in files:
		fileMap[mmh3.hash64(f)[0]] = f
	return fileMap


def lemmatizeText(text):
	processedWords = {}
	wordsHashMap = {}
	words = {}
	word = ""

	for c in text:
		if ('a' <= c <= 'z') or ('A' <= c <= 'Z') or (c == '\'') or (c == '-') or (c == '_'):
			word += c
		else:
			if word:
				word = word.lower()
				if word not in processedWords:
					if word in exceptions:
						if word in words:
							words[word] += 1
						else:
							words[word] = 1
						wordsHashMap[mmh3.hash64(word)[0]] = [word, words[word]]
					else:
						if len(word) > 3 and word not in stopWords:
							tag = nltk.pos_tag([word])              # !!! WARNING : takes A LOT OF TIME !!!
							if tag[0][1] in tags:
								if word in words:
									words[word] += 1
								else:
									words[word] = 1
								wordsHashMap[mmh3.hash64(word)[0]] = [word, words[word]]
					processedWords[word] = word
				else:
					if word in words:
						words[word] += 1
						wordsHashMap[mmh3.hash64(word)[0]] = [word, words[word]]
			word = ""
	return wordsHashMap


def main(argv):
	input = argv

	folderHashMap = {}
	wordsHashMap = {}
	indexDirect = {}
	indexReversed = {}

	if len(argv) != 4:
		print("working with default parameters\ntema_1.py <dir_HTML> <dir_exceptions> <dir_stops> <dir_output>")
		input = ['input\\HTML','input\\exceptions','input\\stopwords','output']
		print(input)

	dir_HTML, dir_exceptions, dir_stops, dir_output = input

	if not (os.path.exists(dir_HTML) and os.path.exists(dir_exceptions) and os.path.exists(dir_stops)):
		return 1

	if not os.path.exists(dir_output):
		os.mkdir(dir_output)

	exception_files = getFiles(dir_exceptions)
	stop_files = getFiles(dir_stops)
	html_files = getFiles(dir_HTML)

	for e in exception_files:
		aux = json.load(open(e, 'r'))
		global exceptions
		exceptions += [item for item in aux if item not in exceptions]
	exceptions = [x.lower() for x in exceptions]

	for s in stop_files:
		aux = json.load(open(s, 'r'))
		global stopWords
		stopWords += [item for item in aux if item not in stopWords]
	stopWords = [x.lower() for x in stopWords]

	folderHashMap = hashFiles(html_files)

	for (fileKey, value) in folderHashMap.items():
		soup = BeautifulSoup(open(value,"r"), "lxml")
		lemmatized = lemmatizeText(soup.text)
		for (wordKey, wordValue) in lemmatized.items():
			if wordKey not in indexReversed:
				indexReversed[wordKey] = [[fileKey, lemmatized[wordKey][1]]]
			else:
				indexReversed[wordKey] += [[fileKey, lemmatized[wordKey][1]]]
				indexReversed[wordKey].sort(key=lambda x: x[1], reverse=True)
			if fileKey not in indexDirect:
				indexDirect[fileKey] = [[wordKey, lemmatized[wordKey][1]]]
			else:
				indexDirect[fileKey] += [[wordKey, lemmatized[wordKey][1]]]
				# indexDirect[fileKey].sort(key=lambda x: x[1], reverse=True)
			wordsHashMap[wordKey] = lemmatized[wordKey][0]

	currentDirName = os.path.basename(os.path.abspath('.'))
	# dumping to json files needed info
	print(currentDirName + '.folderHashMap')
	with open(dir_output + '\\' + currentDirName + '.folderHashMap', 'w') as outfile:
		json.dump(folderHashMap, outfile)

	print(currentDirName + '.wordsHashMap')
	with open(dir_output + '\\' + currentDirName + '.wordsHashMap', 'w') as outfile:
		json.dump(wordsHashMap, outfile)

	print(currentDirName + '.indexDirect')
	with open(dir_output + '\\' + currentDirName + '.indexDirect', 'w') as outfile:
		json.dump(indexDirect, outfile)

	print(currentDirName + '.indexReversed')
	with open(dir_output + '\\' + currentDirName + '.indexReversed', 'w') as outfile:
		json.dump(indexReversed, outfile)


if __name__ == "__main__":
	main(sys.argv[1:])


"""
	tema_1.py <dir_HTML> <dir_exceptions> <dir_stops> <dir_output>
"""