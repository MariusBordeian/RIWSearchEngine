import sys
import os
import dnsClient


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.insert(0,item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def main(argv): # {
	q = Queue()
	storedPages = []
	ipMap = {}			# used in bonus implementation
	if len(argv) > 0:
		for a in argv:
			q.put(a)
	else:
		q.put("https://en.wikipedia.org/wiki/String_theory")

	while not q.isEmpty() or len(storedPages) == 100: # {
		url = q.pop()

		if url in storedPages:
			continue

		urlComponenets = url.replace('//', '/', 1).split('/', 2)
		urlComponenetsCount = len(urlComponenets)

		if not 'http' in protocol or not (1 < urlComponenetsCount < 4):
			continue

		protocol = urlComponenets[0]
		host = urlComponenets[1]
		address = urlComponenets[2] if urlComponenetsCount == 3 else '/'

		if address[0] != '/':
			address = '/' + address

		"""
		if host not in ipMap:
			name = host
			host = dnsClient.main([host])[0]		# self implementation for bonus part
			ipMap[name] = host
		else:
			host = ipMap[host]
		"""

		if not host:
			continue

	# } while not empty or 100

	# call index.py to index stored pages
	
# } main


if __name__ == "__main__":
	main(sys.argv[1:])
