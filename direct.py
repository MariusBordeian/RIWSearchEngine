import json
import mmh3
import os
import sys

# import nltk
# from nltk.stem.wordnet import WordNetLemmatizer

processedWords = {}

# words as they are no processing over it should be done
# eg.: 13 noiembrie as is (ofera semnificatie), 13 nu este exceptie
exceptions = []

tags = {'VB': 'v', 'VBP': 'v', 'VBN': 'v', 'VBG': 'v', 'VBD': 'v', 'VBZ': 'v',
        'NN': 'n', 'NNS': 'n', 'NNP': 'n', 'NNPS': 'n'}

# cuvinte zgomot (useless words w/ no semnification)
stopWords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost",
             "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount",
             "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as",
             "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand",
             "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but",
             "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail",
             "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere",
             "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except",
             "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty",
             "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have",
             "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him",
             "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into",
             "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made",
             "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move",
             "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine",
             "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
             "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out",
             "over", "own", "part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed",
             "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six",
             "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still",
             "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence",
             "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin",
             "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together",
             "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
             "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where",
             "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while",
             "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without",
             "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", "st", "nd", "rd", "th"]


# returns only html files from given directory
def getFiles(path):
    files = []
    path = os.path.abspath(path)
    if os.path.isfile(path):
        if os.path.splitext(path)[1] == '.txt':
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
        fileMap[mmh3.hash128(f)] = f
    return fileMap


def lemmatizeFile(file):
    f = open(file, 'r')
    # wnl = WordNetLemmatizer()
    wordsHashMap = {}
    words = {}
    word = ""

    while 1:
        c = f.read(1)
        if c:
            if ('a' <= c <= 'z') or ('A' <= c <= 'Z') or (c == '\''):
                word += c
            else:
                if word:
                    word = word.lower()
                    if word not in processedWords:
                        canonical = word
                        if word in exceptions:
                            if word in words:
                                words[word] += 1
                            else:
                                words[word] = 1
                            wordsHashMap[mmh3.hash128(word)] = [word, words[word]]
                        else:
                            if word not in stopWords:
                                # tag = nltk.pos_tag([word])
                                if 1:  # tag[0][1] in tags:
                                    # t = tags[tag[0][1]]
                                    canonical = word  # wnl.lemmatize(word, t)
                                    if canonical in words:
                                        words[canonical] += 1
                                    else:
                                        words[canonical] = 1
                                    wordsHashMap[mmh3.hash128(canonical)] = [canonical, words[canonical]]
                        processedWords[word] = canonical
                    else:
                        if word in words:
                            words[word] += 1
                        else:
                            words[word] = 1
                        wordsHashMap[mmh3.hash128(word)] = [word, words[word]]
                word = ""
        else:
            break
    """
    with open(f.name + '.wordsHashMap', 'w') as outfile:
        json.dump(wordsHashMap, outfile) # """
    return wordsHashMap


def main(argv):
    input = [os.path.abspath(os.curdir)]
    files = []
    folderHashMap = {}
    filesWordsMap = {}
    indexMap = {}  # direct index ???
    indexMap2 = {}
    if len(argv) > 0:
        input = argv

    for thing in input:
        if not os.path.exists(thing + '\\output'):
            os.mkdir(thing + '\\output')

        files = getFiles(thing)
        folderHashMap = hashFiles(files)
        print(os.path.basename(thing) + '.folderHashMap')
        with open('.\\output\\' + os.path.basename(thing) + '.folderHashMap', 'w') as outfile:
            json.dump(folderHashMap, outfile)
        # """
        for (key, value) in folderHashMap.items():
            lemmatized = lemmatizeFile(value)
            filesWordsMap[key], indexMap[key] = lemmatized, lemmatized.keys()
            for wordKey in lemmatized.keys():
                if wordKey not in indexMap2:
                    indexMap2[wordKey] = [[key, lemmatized[wordKey][1]]]
                else:
                    indexMap2[wordKey] += [[key, lemmatized[wordKey][1]]]
            # TODO : sort indexMap2[wordKey] by number of word occurrences per file!

        print(os.path.basename(thing) + '.filesWordsMap')
        with open('.\\output\\' + os.path.basename(thing) + '.filesWordsMap', 'w') as outfile:
            json.dump(filesWordsMap, outfile)

        print(os.path.basename(thing) + '.indexMap')
        with open('.\\output\\' + os.path.basename(thing) + '.indexMap', 'w') as outfile:
            json.dump(indexMap, outfile)

        print(os.path.basename(thing) + '.indexMap2')
        with open('.\\output\\' + os.path.basename(thing) + '.indexMap2', 'w') as outfile:
            json.dump(indexMap2, outfile)
        """
        for (key, value) in folderHashMap.items():
            print(os.path.basename(value) + '.wordsMap')
            with open('.\\output\\' + os.path.basename(value) + '.wordsMap', 'w') as outfile:
                json.dump(filesWordsMap[key], outfile)
        # ""
        for f in files:
            print(f)
        # ""
        for (i, f) in hashFiles(files).items():
            print(str(i) + ' : ' + f)
        # """


if __name__ == "__main__":
    main(sys.argv[1:])
