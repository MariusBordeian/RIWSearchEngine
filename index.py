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
        if os.path.splitext(path)[1] == '.txt': # extention to filter files on 
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

    for line in f:
        for c in line:
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
    """
    with open(f.name + '.wordsHashMap', 'w') as outfile:
        json.dump(wordsHashMap, outfile) # """
    return wordsHashMap


def main(argv):
    input = [os.curdir]
    files = []
    folderHashMap = {}
    wordsHashMap = {}
    indexDirect = {}
    indexReversed = {}
    if len(argv) > 0:
        input = argv

    for i in input:
        item = os.path.abspath(i)
        if not os.path.exists(item + '\\output'):
            os.mkdir(item + '\\output')

        files = getFiles(item)
        folderHashMap = hashFiles(files)
        
        for (fileKey, value) in folderHashMap.items():
            lemmatized = lemmatizeFile(value)
            for (wordKey, wordValue) in lemmatized.items():
                if wordKey not in indexReversed:
                    indexReversed[wordKey] = [[fileKey, lemmatized[wordKey][1]]]
                else:
                    indexReversed[wordKey] += [[fileKey, lemmatized[wordKey][1]]]
                    indexReversed[wordKey].sort(key=lambda x: x[1], reverse=True)
                if fileKey not in indexDirect:
                    indexDirect[fileKey] = [[wordKey, lemmatized[wordKey][1]]]
                else:
                    indexDirect[fileKey] += [[wordKey, lemmatized[wordKey][1]]]
                    # indexDirect[fileKey].sort(key=lambda x: x[1], reverse=True)
                wordsHashMap[wordKey] = lemmatized[wordKey][0]

        # dumping to json files needed info
        print(os.path.basename(item) + '.folderHashMap')
        with open('.\\output\\' + os.path.basename(item) + '.folderHashMap', 'w') as outfile:
            json.dump(folderHashMap, outfile)

        print(os.path.basename(item) + '.wordsHashMap')
        with open('.\\output\\' + os.path.basename(item) + '.wordsHashMap', 'w') as outfile:
            json.dump(wordsHashMap, outfile)

        print(os.path.basename(item) + '.indexDirect')
        with open('.\\output\\' + os.path.basename(item) + '.indexDirect', 'w') as outfile:
            json.dump(indexDirect, outfile)

        print(os.path.basename(item) + '.indexReversed')
        with open('.\\output\\' + os.path.basename(item) + '.indexReversed', 'w') as outfile:
            json.dump(indexReversed, outfile)
        

if __name__ == "__main__":
    main(sys.argv[1:])


"""
    index direct : <docId : { wordId : count}>
    index invers : <cuvId : { docId : count}>
"""