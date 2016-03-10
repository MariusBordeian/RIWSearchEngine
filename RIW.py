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


class Page(object):
    def __init__(self, title):
        self.title = title


def main():
    pages = []
    if len(sys.argv) == 1:
        pages.append("http://forum.xda-developers.com/usercp.php")
    else:
        pages = sys.argv[1:]

    for p in pages:
        print("page : " + p + "\n")
        page = {}
        soup = BeautifulSoup(urlopen(p), "lxml")

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
            if href and '#' not in href and 'http' in href:
                links.append(href)
                # print("\t" + href)

        page["a"] = links

        text = ""
        tags = soup.find_all()
        for t in tags:
            if not re.findall(re.compile("html|body|head|script|style"), t.name):
                text += t.text

        # print("page content : \n")
        # print(text)

        page["text"] = json.JSONEncoder().encode(text)

        with open(title + '_page.json', 'w') as outfile:
            json.dump(page, outfile)

    print("done :)")


if __name__ == "__main__":
    main()

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