import sys
import json


def main(argv):
    words = {}
    word = ""

    for path in argv:
        f = open(path)
        while 1:
            c = f.read(1)
            if c:
                if ('A' <= c <= 'Z') or ('a' <= c <= 'z'):
                    word += c
                else:
                    if word:
                        if word in words:
                            words[word] += 1
                        else:
                            words[word] = 1
                    word = ""
            else:
                break

    with open('data.json', 'w') as outfile:
        json.dump(words, outfile)


if __name__ == "__main__":
    main(sys.argv[1:])
