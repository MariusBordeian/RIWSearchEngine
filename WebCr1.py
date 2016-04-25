import index  # index.py
import RIW  # RIW.py
import sys
import os

# from bs4 import BeautifulSoup
from urllib.request import urlopen  # python 3!


class Queue:
	def __init__(self):
		self.items = []

	def __contains__(self, key):
		return key in self.items

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.insert(0, item)

	def pop(self):
		return self.items.pop()

	def size(self):
		return len(self.items)


pathToStore = "storage"
forbidden = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']


def main(argv):  # {
	q = Queue()
	storedPages = []

	if len(argv) > 0:
		if isinstance(argv, list):
			for a in argv:
				q.push(a)
		else:
			q.push(argv)
	else:
		q.push("https://en.wikipedia.org/wiki/String_theory")
		q.push("http://stackoverflow.com/questions/11227809/why-is-processing-a-sorted-array-faster-than-an-unsorted-array")

	while len(storedPages) < 100 and not q.isEmpty():  # {
		url = q.pop()

		if url in storedPages:
			continue

		urlLen = len(url)

		protocol = ''

		if ':' in url:
			protocol = url.split(':', 1)[0]
		else:
			continue

		if not protocol or 'http' not in protocol:
			continue

		try:
			page = RIW.main(url)[0]
		except:
			e = sys.exc_info()
			type = e[0]
			msg = e[1]
			print(type)
			print(msg)
			continue

		urlContent = page["content"].decode()
		urlText = page["text"].decode()
		urlLinks = page["a"]

		for link in urlLinks:
			if link not in storedPages and link not in q:
				q.push(link)

		if url[urlLen - 5:urlLen] != '.html':
			url += '.html'

		path_file = url.split('//', 2)
		path_file = path_file[1] if len(path_file) == 2 else path_file[0]

		indexOfFilenameStart = len(path_file) - 1 - path_file[::-1].index(
			'/') + 1  # last index of '/' + 1 is the start of the filename
		path_folder = pathToStore + '/' + protocol + '/' + path_file[:indexOfFilenameStart - 1]
		filename = path_file[indexOfFilenameStart:]

		for f in forbidden:
			if f in filename:
				continue

		if not os.path.exists(path_folder):
			os.makedirs(path_folder)

		path_file = path_folder + '/' + filename

		file_page = open(path_file, mode='w', encoding='utf-8')
		file_page.write(urlContent)
		file_page.close()

		file_page = open(path_file[:len(path_file)-4]+'txt', mode='w', encoding='utf-8')
		file_page.write(urlText)
		file_page.close()

		if os.path.exists(path_file) and os.path.exists(path_file[:len(path_file)-4]+'txt'):
			storedPages.append(url[:urlLen])
			print(len(storedPages))
	# } while not empty or 100

	# call index.py to index stored pages "./storage"
	index.main(pathToStore)
# } main


if __name__ == "__main__":
	main(sys.argv[1:])

"""
	./storage
			 /host
			 	  /./.
			 	  	  /./address.
			 	  	  			 /./.
			 	  					 /filename.html
"""
