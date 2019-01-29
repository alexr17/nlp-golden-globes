from nltk.corpus import stopwords
from src.helpers.debug import top_keys
import re
stopwords = set(stopwords.words('english'))

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
    if len(tkn) < 2:
        return False
    return True

def bigrams(tokens, valid_kw, invalid_kw):
    prev = False
    bigrams = []
    for i in range(len(tokens)):
        if valid_tkn(tokens[i], valid_kw, invalid_kw):
            if prev:
                bigrams.append(prev + ' ' + tokens[i])
            prev = tokens[i]
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



def join_ngrams(tpls):
    ngrams = []
    coeff = 0.5
    min = 50
    for idx, tpl in enumerate(tpls):
        
        inc = 1
        while len(tpls) > idx + inc and tpls[idx + inc][1] > min and tpls[idx + inc][1] > tpl[1] * coeff:
            top = tpl[0].split(' ')
            bot = tpls[idx + inc][0].split(' ')
            if top[1] == bot[0]: #join
                ngrams.append((' '.join(top) + ' ' + ' '.join(bot[1:]), tpls[idx + inc][1] + tpl[1]))
            #print(tpls[idx + inc])
            inc += 1
    #top_keys(ngrams, 100)
