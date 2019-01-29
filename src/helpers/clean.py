from nltk.corpus import stopwords
import re
stopwords = set(stopwords.words('english'))

# filter out token
def valid_tkn(tkn, valid_kw):

    if tkn in valid_kw:
        return True
    # stopwords
    if tkn in stopwords:
        return False

    # ampersand and twitter link
    twitter_stop = ['&amp;', '//t.co/', 'rt', 'http']
    if any(substr in tkn for substr in twitter_stop):
        return False

    # special unicode character
    if any(ord(c) > 128 for c in tkn):
        return False

    regex = re.compile('[^a-zA-Z]')
    tkn = regex.sub('', tkn)
    if len(tkn) < 2:
        return False
    return True

def bigrams(tokens, valid_kw, invalid_kw):
    prev = tokens[0]
    bigrams = []
    for i in range(1, len(tokens)):
        if valid_tkn(tokens[i], valid_kw) and tokens[i] not in invalid_kw:
            bigrams.append(prev + ' ' + tokens[i])
            prev = tokens[i]
    return bigrams

def trigrams(tokens, valid_kw, invalid_kw):
    prev1 = tokens[0]
    prev2 = tokens[1]
    trigrams = []
    for i in range(2, len(tokens)):
        if valid_tkn(tokens[i], valid_kw) and tokens[i] not in invalid_kw:
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



