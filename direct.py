import os
import sys
import mmh3
import json

def getFiles(path):
	files = []
	path = os.path.abspath(path)
	if os.path.isfile(path): 
		files.append(path)
	else:
		content = os.listdir(path)
		for f in content:
			local = getFiles(path + '\\' + f)
			for l in local:
				files.append(l)
	return files

def indexFiles(files):
	fileMap = {}
	for f in files:
		fileMap[mmh3.hash128(f)] = f
	return fileMap

def main(argv):
	input = [os.path.abspath(os.curdir)]
	files = []
	filesMap = {}
	if len(argv) > 0:
		input = argv

	for thing in input:
		files = getFiles(thing)
		filesMap = indexFiles(files)

		print(os.path.basename(thing) + '.filesMap')
		with open(os.path.basename(thing)+'.filesMap', 'w') as outfile:
			json.dump(filesMap, outfile)

	"""
	for f in files:
		print(f)
	# ""
	for i,f in indexFiles(files).items():
		print(str(i) + ' : ' + f)
	# """

if __name__ == "__main__":
   main(sys.argv[1:])