import json
import sys
import os
import mmh3


def main(argv):
	input = ["python", "IT"]
	actions = ["and", "or", "not"]
	result = []
	folderHashMap = {}
	wordsHashMap = {}
	indexDirect = {}
	indexReversed = {}
	if len(argv) > 0:
		# print("give something to search for!")
		argv = [x.lower() for x in argv]
		input = argv

	for i in range(1, len(input)):
		if input[i] in actions and input[i-1] in actions:
			return 1										# jet!

	currentDirName = os.path.basename(os.path.abspath(os.curdir))
	
	print('file : ' + '.\\output\\' + currentDirName + '.folderHashMap')
	with open('.\\output\\' + currentDirName + '.folderHashMap', 'r') as infile:
		folderHashMap = json.load(infile)

	print('file : ' + '.\\output\\' + currentDirName + '.wordsHashMap')
	with open('.\\output\\' + currentDirName + '.wordsHashMap', 'r') as infile:
		wordsHashMap = json.load(infile)

	print('file : ' + '.\\output\\' + currentDirName + '.indexDirect')
	with open('.\\output\\' + currentDirName + '.indexDirect', 'r') as infile:
		indexDirect = json.load(infile)

	print('file : ' + '.\\output\\' + currentDirName + '.indexReversed\n')
	with open('.\\output\\' + currentDirName + '.indexReversed', 'r') as infile:
		indexReversed = json.load(infile)

	if len(folderHashMap) > 0 and len(wordsHashMap) > 0 and len(indexDirect) > 0 and len(indexReversed) > 0 :
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
						input.insert(i, "and")
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
				
				if action == "and":
					if f1_len > f2_len:
						result = [item for item in files_2 if item in files_1]
					else:
						result = [item for item in files_1 if item in files_2]
				elif action == "or":
					if f1_len > f2_len:
						aux = files_1
						result = [item for item in files_2 if item not in aux]
						result += aux
					else:
						aux = files_2
						result = [item for item in files_1 if item not in aux]
						result += aux
				elif action == "not":
					result = [item for item in files_1 if item not in files_2]
				else:
					print("what the ???\nsomthing is definitely wrong here!")

				print(input[0] + " " + input[1] + " " + input[2])
				for r in result:
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
							
							if action == "and":
								if f1_len > f2_len:
									result = [item for item in files_2 if item in files_1]
								else:
									result = [item for item in files_1 if item in files_2]
							elif action == "or":
								if f1_len > f2_len:
									aux = files_1
									result = [item for item in files_2 if item not in aux]
									result += aux
								else:
									aux = files_2
									result = [item for item in files_1 if item not in aux]
									result += aux
							elif action == "not":
								result = [item for item in files_1 if item not in files_2]
							else:
								print("what the ???\nsomthing is definitely wrong here!")
							
							print("previous " + input[i] + " " + input[i+1])
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
	else:
		print("sorry, have no data to search in.")

	print("Files for \"" + str(input) + "\" query : ")
	for r in result:
		print(folderHashMap[str(r)])


if __name__ == "__main__":
	main(sys.argv[1:])


"""
	index direct : <docId : { wordId : count}>
	index invers : <cuvId : { docId : count}>
"""
