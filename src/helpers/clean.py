from nltk.corpus import stopwords
from src.helpers.debug import top_keys
import re
stopwords = set(stopwords.words('english'))
stopwords.remove('don')
stopwords.remove('will')

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

def unibigrams(tokens, valid_kw, invalid_kw):
    valid_movie_kw = {'the', 'in', 'on', 'of', 'this'}
    prev = False
    grams = {
        'uni': set(),
        'bi': set()
    }
    for tkn in tokens:
        if valid_tkn(tkn, valid_kw | valid_movie_kw, invalid_kw):
            if prev:
                grams['bi'].add(prev + ' ' + tkn)
            if tkn not in valid_movie_kw:
                grams['uni'].add(tkn)
            prev = tkn
    return grams

def bigrams(tokens, valid_kw, invalid_kw):
    prev = False
    bigrams = set()
    for tkn in tokens:
        if valid_tkn(tkn, valid_kw, invalid_kw):
            if prev:
                bigrams.add(prev + ' ' + tkn)
            prev = tkn
    return bigrams
    # tokens = [tkn for tkn in tokens if valid_tkn(tkn, valid_kw, invalid_kw)]
    # # ngrams of 2
    # ngrams = zip(*[tokens[i:] for i in range(2)])
    # return [" ".join(ngram) for ngram in ngrams]

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


def join_ngrams(lst, minimum):
    # lst : [("name name"), 23]
    threshold = 0.8
    if not lst:
        return lst

    flag = True
    counter = 0
    updated_lst = lst
    while flag:
        #updated_lst = []
        # if counter == 1:
        #     break
        flag = False
        for i in range(len(lst)):
            if i >= len(lst):
                break
            if lst[i][1] < minimum:
                break
            curr = lst[i]
            # ["robert downey", "downey jr"]
            j = i+1
            while j < len(lst) and curr[1]/lst[j][1] > threshold:
                bigram1 = curr[0].split(" ")
                bigram2 = lst[j][0].split(" ")
                if bigram1[1:] == bigram2[:-1]:
                    ngram = bigram1 + [bigram2[-1]]
                    occurence = lst[j][1] + 100
                    updated_lst.append((" ".join(ngram), occurence))
                    flag = True
                    check_merge = True
                # elif bigram1[-1] == bigram2[0]:
                #     ngram = bigram1 + bigram2[1:]
                #     occurence = lst[j][1]
                #     lst[j] = (" ".join(ngram), occurence, True)
                #     #updated_lst.append((" ".join(ngram), occurence))
                #     flag = True
                #     check_merge = True
                # elif bigram1[0] == bigram2[-1]:
                #     ngram = [bigram1[-1], bigram1[0], bigram2[0]]
                #     occurence = lst[j][1]
                #     updated_lst.append((" ".join(ngram), occurence))
                j += 1
            # print(lst)
            # print(curr)
            # print('----')

            # if check_merge and len(curr) < 3:
            #     lst.remove(curr)

        # if updated_lst:
        #     lst = updated_lst
        # else: break




    return sorted(lst, key=lambda x: x[1], reverse=True)

