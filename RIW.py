import re
import sys
import json
# import codecs
# import locale

from bs4 import BeautifulSoup
from urllib.request import urlopen


# print(sys.stdout.encoding)
# sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
# sys.stdout.write(line)
# print line


aROBOTS = 'robots'
aLINKS = 'links'


def main(argv):
	pages = []
	v_return = []   # an array of maps (for each page passed a map is created)
	if len(argv) > 0:
		if isinstance(argv, list):
			pages = argv
		else:
			pages = [argv]
	else:
		pages = sys.argv[1:]

	for p in pages:
		print("page : " + p + "\n")
		comp = p.split('//')
		path = comp[1] if len(comp) == 2 else comp[0]
		index = path.index('/')
		host = (comp[0] + '//' if len(comp) == 2 else '') + (comp[1][:index] if len(comp) == 2 else comp[0][:index])
		page = {}
		soup = BeautifulSoup(urlopen(p), "lxml")
		page["content"] = str(soup).encode('utf-8')
		title = soup.title.text
		# print("Page Title : " + title)
		page["title"] = title

		meta_array = soup("meta")
		# print(meta)

		meta_dictionary = {}
		# print("\nmetas : ")
		for m in meta_array:
			name = m.get("name")
			if name == "keywords" or name == "description" or name == "robots":
				meta_dictionary[name] = m["content"]
				# print("\t" + name + " : " + m["content"])

		page["meta"] = meta_dictionary

		links = []
		# print("\nlinks : ")
		ls = soup.find_all('a')
		for link in ls:
			href = link.get('href')
			if href and '?' not in href:
				if '#' not in href:
					if 'http' in href[:4]:
						links.append(href)
						# print("\t" + href)
					elif '//' in href[:2]:
						links.append((host[:host.index(':')] if 'http' in host[:4] else 'http:') + href)
					elif href[0] == '/':
						links.append(host + href)
					elif 'www' not in href[:3]:
						links.append(host + '/' + href)
				else:
					href = href[:href.index('#')]
					if href:
						if 'http' in href[:4]:
							links.append(href)
						# print("\t" + href)
						elif '//' in href[:2]:
							links.append((host[:host.index(':')] if 'http' in host[:4] else 'http:') + href)
						elif href[0] == '/':
							links.append(host + href)
						elif 'www' not in href[:3]:
							links.append(host + '/' + href)
		auxLinks = []
		auxLinks = [item for item in links if item not in auxLinks]
		page["a"] = auxLinks

		text = ""
		tags = soup.find_all()
		for t in tags:
			if not re.findall(re.compile("html|body|head|script|style"), t.name):
				text += t.text

		# print("page content : \n")
		# print(text)

		page["text"] = text.encode('utf-8')     # json.JSONEncoder().encode(text)
		"""
		with open(title + '_page.json', 'w') as outfile:
			json.dump(page, outfile)
		"""
		# print(page)
		v_return.append(page)

	# print("done :)")
	return v_return


if __name__ == "__main__":
	main(sys.argv[1:])

"""
hints :
	2 bools : indexAllowed, linksAllowed (din robots)
	meta.robots nu intra in file ("rules" what to do with with page)
	a nu intra in file ("input", pentru crawler din nou)

	se citeste meta.robots si setez flags, if (indexAllowed or linksAllowed) delete page

	1, 2, 3, 6 - indexare
	4 - reguli
	5 - crawler
"""