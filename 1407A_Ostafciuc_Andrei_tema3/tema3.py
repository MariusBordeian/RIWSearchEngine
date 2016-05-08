import json
import sys
import os
import mmh3
import collections


folderHashMap = {}
wordsHashMap = {}
indexReversed = {}


def BooleanReduce(input):
	if len(input) > 1:
		# remove and operations on 0 position
		for i in range(0, len(input)):
			if i == 0 and input[i] in actions:
				input.pop(0)
				i = 0
			else:
				break
		
		if len(input) > 1:
			# add missing operations
			for i in range(1, len(input)):
				if input[i] not in actions and input[i-1] not in actions:
					input.insert(i, "or")
					i += 2

			action = input[1]
			# array of arrays like [[f1, nrOfOccurancies1], [f2, nrOfOccurancies2], ...]
			wordKey1=str(mmh3.hash64(input[0])[0])
			wordKey2=str(mmh3.hash64(input[2])[0])
			if wordKey1 in indexReversed:
				files_1 = [item[0] for item in indexReversed[wordKey1]]  
			else:
				files_1=[]
				action="or"

			if wordKey2 in indexReversed:	
				files_2 = [item[0] for item in indexReversed[wordKey2]]
			else:
				files_2=[]
				action="or"

			f1_len = len(files_1)
			f2_len = len(files_2)
			
			if f1_len > f2_len:
				aux = files_1
				result = [item for item in files_2 if item not in aux]
				result += aux
			else:
				aux = files_2
				result = [item for item in files_1 if item not in aux]
				result += aux
			
			print("files for : " + input[0])
			for r in files_1:
				print(folderHashMap[str(r)])
			print("\n")

			print("files for : " + input[2])
			for r in files_2:
				print(folderHashMap[str(r)])
			print("\n")

			size = len(input)
			if size > 3:
				for i in range(3, size-1): 
					if input[i].lower() in actions and input[i+1] not in actions:
						action = input[i]
						# array of arrays like [[f1, nrOfOccurancies1], [f2, nrOfOccurancies2], ...]
						files_1 = result
						wordKey2=str(mmh3.hash64(input[i+1])[0])
						if wordKey2 in indexReversed:
							files_2 = [item[0] for item in indexReversed[wordKey2]]
						else:
							files_2=[]
							action="or"

						f1_len = len(files_1)
						f2_len = len(files_2)
						
						if f1_len > f2_len:
							aux = files_1
							result = [item for item in files_2 if item not in aux]
							result += aux
						else:
							aux = files_2
							result = [item for item in files_1 if item not in aux]
							result += aux
						
						print("previous result " + input[i] + " " + input[i+1])
						for r in result:
							print(folderHashMap[str(r)])
						print("\n")
		else:
			if input[0] not in actions:
				key = str(mmh3.hash64(input[0])[0])
				if key in indexReversed:
					result = [item[0] for item in indexReversed[key]]
	else:
		if input[0] not in actions:
			key = str(mmh3.hash64(input[0])[0])
			if key in indexReversed:
				result = [item[0] for item in indexReversed[key]]
	return result


def loadDatabase():
	currentDirName = os.path.basename(os.path.abspath(os.curdir))
	
	if not os.path.exists('.\\output\\' + currentDirName + '.folderHashMap') or not os.path.exists('.\\output\\' + currentDirName + '.wordsHashMap') or not os.path.exists('.\\output\\' + currentDirName + '.indexReversed'):
		print('sorry, could not find any database to search into!\ncheck : ' + '>.\\output\\' + currentDirName + '< .folderHashMap, .wordsHashMap and .indexReversed')
		return 1

	print('file : ' + '.\\output\\' + currentDirName + '.folderHashMap')
	with open('.\\output\\' + currentDirName + '.folderHashMap', 'r') as infile:
		folderHashMap = json.load(infile)

	print('file : ' + '.\\output\\' + currentDirName + '.wordsHashMap')
	with open('.\\output\\' + currentDirName + '.wordsHashMap', 'r') as infile:
		wordsHashMap = json.load(infile)

	print('file : ' + '.\\output\\' + currentDirName + '.indexReversed\n')
	with open('.\\output\\' + currentDirName + '.indexReversed', 'r') as infile:
		indexReversed = json.load(infile)


def DocumentsVectors(documents):
	D = {}

	for d in documents:
		D[d] = VectorQuery(d)

	return D


def VectorQuery(query):
	q = 0
	aux = []

	for word in query:
		if word != 'or':
			aux.append(word)

	# calculate d for aux query as a document		
	# d = { key : tf(key, d) * idf(key) }

	return q


def similaritateCosinus(d, q):
	# cos(d, q)
	return 0


def main(argv):
	input = ["function", "AP_MPMQ_NOT_SUPPORTED"]
	result = {}
	D = {}

	if len(argv) > 0:
		input = argv
	else:
		print("will run on sample, as no args were passed! : " + str(input) + "\n")

	input = [x.lower() for x in input]

	for i in range(1, len(input)):
		if input[i] in actions and input[i-1] in actions:
			return 1										# jet!

	if loadDatabase() == 1:
		return 1

	if len(folderHashMap) > 0 and len(wordsHashMap) > 0 and len(indexReversed) > 0 :
		files = BooleanReduce(input)
		D = DocumentsVectors(files)
		q = VectorQuery(input)

		for k,d in D:
			result[k] = similaritateCosinus(d, q)

		result = collections.OrderedDict(sorted(result.items()))
	else:
		print("sorry, have no data to search in.")

	print("Files for \"" + str(input) + "\" query : ")
	for r in result.items():
		print(folderHashMap[str(r)])


if __name__ == "__main__":
	main(sys.argv[1:])


"""
	index direct : <docId : { wordId : count}>
	index invers : <cuvId : { docId : count}>
"""
