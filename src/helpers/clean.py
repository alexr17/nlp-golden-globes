from nltk.corpus import stopwords
from src.helpers.debug import top_keys
import re
stopwords = set(stopwords.words('english'))
stopwords.remove('don')

# filter out token
def valid_tkn(tkn, valid_kw, invalid_kw):
    tkn = tkn.lower()
    if tkn in valid_kw:
        return True

    if tkn in invalid_kw:
        return False
    # stopwords
    if tkn in stopwords:
        return False

    # ampersand and twitter link
    twitter_stop = ['&amp;', 'rt', 'http']
    if '//t.co/' in tkn or tkn in twitter_stop:
        return False

    # special unicode character
    if any(ord(c) > 128 for c in tkn):
        return False

    regex = re.compile('[^a-zA-Z]')
    tkn = regex.sub('', tkn)
    if len(tkn) < 1:
        return False
    return True

def unigrams(tokens, valid_kw, invalid_kw):
    unigrams = []
    for tkn in tokens:
        if valid_tkn(tkn, valid_kw, invalid_kw):
            unigrams.append(tkn)
    return unigrams

def bigrams(tokens, valid_kw, invalid_kw):
    prev = False
    bigrams = []
    for tkn in tokens:
        if valid_tkn(tkn, valid_kw, invalid_kw):
            if prev:
                bigrams.append(prev + ' ' + tkn)
            prev = tkn
    return bigrams

def trigrams(tokens, valid_kw, invalid_kw):
    prev1 = False
    prev2 = False
    trigrams = []
    for i in range(2, len(tokens)):
        if valid_tkn(tokens[i], valid_kw, invalid_kw):
            if prev1 and prev2:
                trigrams.append(prev1 + ' ' + prev2 + ' ' + tokens[i])
            prev1 = prev2
            prev2 = tokens[i]
    return trigrams


def merge_bigrams(lst):
    lst1 = [x[0].split(" ")[0] for x in lst]
    #motion, best, supporting, best"
    lst2 = [x[0].split(" ")[1] for x in lst]
    # picture, supporting, actor, best
    lst_of_words = {}
    for i, element in enumerate(lst):
        word = ""
        if lst1[i] == "best":
            if lst2[i] in lst1:
                word = lst1[i] + " " + lst2[i] + " " + lst2[lst1.index(lst2[i])]
                if word in lst_of_words:
                    lst_of_words[word] +=1
                else:
                    lst_of_words[word] = 1

    return lst_of_words


def join_ngrams(lst):
    # lst : [("name name"), 23]
    threshold = 0.8
    minimum = 10
    if not lst:
        return lst

    updated_lst = []
    for i in range(len(lst)):
        if lst[i][1] < minimum:
            break
        curr = lst[i]
        j = i + 1
        while j < len(lst) and curr[1]/lst[j][1] > threshold:
            ngram = []
            bigram1 = curr[0].split(" ")
            bigram2 = lst[j][0].split(" ")
            if bigram1[-1] == bigram2[0]:
                ngram = [bigram1[0], bigram1[-1], bigram2[-1]]
                occurence = lst[j][1]
                updated_lst.append((" ".join(ngram), occurence))
            elif bigram1[0] == bigram2[-1]:
                ngram = [bigram1[-1], bigram1[0], bigram2[0]]
                occurence = lst[j][1]
                updated_lst.append((" ".join(ngram), occurence))
            j += 1


    return updated_lst #sorted(updated_lst, key=lambda x: x[1], reverse=True)

