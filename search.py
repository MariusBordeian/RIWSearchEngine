import json
import sys
import os
import mmh3


def main(argv):
	input = ["book", "surprise", "and", "nightmare", "or", "caravans", "not", "pray"]
	actions = {"and" : "and", "or" : "or", "not" : "not"}
	result = []
	folderHashMap = {}
	wordsHashMap = {}
	indexDirect = {}
	indexReversed = {}
	if len(argv) > 0:
		# print("give something to search for!")
		input = argv

	with open('.\\output\\' + os.path.basename(os.path.abspath(os.curdir)) + '.folderHashMap', 'r') as infile:
		folderHashMap = json.load(infile)

	with open('.\\output\\' + os.path.basename(os.path.abspath(os.curdir)) + '.wordsHashMap', 'r') as infile:
		wordsHashMap = json.load(infile)
	
	with open('.\\output\\' + os.path.basename(os.path.abspath(os.curdir)) + '.indexDirect', 'r') as infile:
		indexDirect = json.load(infile)
	
	with open('.\\output\\' + os.path.basename(os.path.abspath(os.curdir)) + '.indexReversed', 'r') as infile:
		indexReversed = json.load(infile)

	if len(folderHashMap) > 0 and len(wordsHashMap) > 0 and len(indexDirect) > 0 and len(indexReversed) > 0 :
		size = len(input)
		for i in range(1, size):
			print(input[i])
			if input[i].lower() in actions and i < size:
				word_1 = mmh3.hash128(input[i-1])
				word_2 = mmh3.hash128(input[i+1])
				action = actions[input[i]]

			else:
				if input[i-1].lower() not in actions:
					pass
	else:
		print("sorry, have no data to search in.")


if __name__ == "__main__":
	main(sys.argv[1:])


"""
	index direct : <docId : { wordId : count}>
	index invers : <cuvId : { docId : count}>
"""