import sys
import json
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

processedWords = {}

# words as they are no processing over it should be done
# eg.: 13 noiembrie as is (ofera semnificatie), 13 nu este exceptie
exceptions = []

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

tags = {'VB': 'v', 'VBP': 'v', 'VBN': 'v', 'VBG': 'v', 'VBD': 'v', 'VBZ': 'v',
        'NN': 'n', 'NNS': 'n', 'NNP': 'n', 'NNPS': 'n'}


def main(argv):
    wnl = WordNetLemmatizer()
    if len(sys.argv) == 2:
        f = open(argv[1])
    else:
        f = open('debug.txt')
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
                        else:
                            if word not in stopWords:
                                tag = nltk.pos_tag([word])
                                if tag[0][1] in tags:
                                    t = tags[tag[0][1]]
                                    canonical = wnl.lemmatize(word, t)
                                    if canonical in words:
                                        words[canonical] += 1
                                    else:
                                        words[canonical] = 1
                        processedWords[word] = canonical
                    else:
                        if word in words:
                                words[word] += 1
                        else:
                            words[word] = 1
                word = ""
        else:
            break

    with open('data' + '_' + f.name + '.json', 'w') as outfile:
        json.dump(words, outfile)


if __name__ == "__main__":
    main(sys.argv)

"""

"""