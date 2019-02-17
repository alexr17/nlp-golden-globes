import nltk
import re
from collections import Counter
from nltk import ngrams
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn
from src.helpers.clean import bigrams
from src.helpers.clean import join_ngrams
from src.helpers.debug import top_keys
#from src.helpers.clean import join_ngrams
from src.helpers.clean import trigrams
from src.helpers.clean import merge_bigrams
import pprint
#from src.helpers.find import find_name

#list_of_awards = [line.strip() for line in open('./data/award_kw.txt')]
list_of_awards = ['best', 'motion', 'picture', 'drama', 'performance', 'actress', 'actor', 'comedy', 'musical', 'animated', 'feature', 'film', 'foreign', 'language', 'supporting', 'role', 'director', 'screenplay', 'orginal', 'score', 'song', 'television', 'series',  'mini-series', 'mini']
helper_words = ['by','an','in', 'a', 'for','-',':','or']
# golden globes stopwords
gg_sw = ['golden', 'globe', 'globes', 'goldenglobes']

# list of televsion, movie, and music

# award stopwords
award_sw = ['year', 'show', 'award', 'awards', 'wins', 'best']

# media stopwords
media_sw = ['eonline', 'cnnshowbiz']

# award keywords
award_kw = ['actor', 'actress', 'supporting']

answer = {}

# https://github.com/brownrout/EECS-337-Golden-Globes/blob/master/gg_api.py
def see_awards(data):
    all_awards = []
    award_tweets = []
    for obj in data:
        text = obj['text'].lower()
        if len(set(list_of_awards).intersection(set(text.split(" ")))) > 4:
            award_tweets.append(text)

    for tweet in award_tweets:
        tweet = tweet.split(" ")
        start = len(tweet) - 1
        end = len(tweet) - 1
        # for word in list_of_awards:
        #     if word in tweet:
        #         index = tweet.index(word)
        #         if index < start:
        #             start = index
        flag = False
        for i, word in enumerate(tweet):
            if word in list_of_awards and not flag:
                start = i
                flag = True
            if word in list_of_awards:
                end = i

        temp = []
        #print(tweet[start:end+1])
        for word in tweet[start:end+1]:
            if word in list_of_awards or word in helper_words:
                temp.append(word)
        award = ' '.join(sorted(set(temp), key=lambda x: tweet.index(x)))
        # print(award)
        # print('----')

        if award not in all_awards:
            all_awards.append(award)
#
    all_awards = list(set(all_awards))
    all_awards = [x for x in all_awards if x.split(" ")[0] == 'best']
    for x in all_awards:
        x1 = set([a for a in x.split(" ") if a not in helper_words])
        for y in all_awards:
            y1 = set([a for a in y.split(" ") if a not in helper_words])
            if len(x1.intersection(y1)) > 4:
                all_awards.remove(y)
    return all_awards



def award_set(bigrams):
    all_awards = []
    threshold = 0.8
    minimum = 100
    bigrams = [x for x in bigrams if x[1] > minimum]
    for i, bigram1 in enumerate(bigrams):
        ngram = bigram1[0].split(" ")
        for j, bigram2 in enumerate(bigrams):
            if bigram2 == bigram1:
                continue
            bigram = bigram2[0].split(" ")
            if ngram[-1] == bigram[0]:
               ngram += bigram[1:]
            elif ngram[0] == bigram[-1]:
                ngram = [bigram[0]] + ngram
        ngram = " ".join(ngram)
        flag = False
        for award in all_awards:
            if ngram in award:
                flag = True
                break
        if not flag:
            all_awards.append(ngram)

    return all_awards






def find_awards(data):
    return see_awards(data)
    award_dict = {}

    best_dict = {
        'nxt': {},
        'nxt_two': {},
        'nxt_three': {}
    }
#     >>> from collections import Counter
# >>> from nltk import ngrams
# >>> bigtxt = open('big.txt').read()
# >>> ngram_counts = Counter(ngrams(bigtxt.split(), 2))
# >>> ngram_counts.most_common(10)




    for obj in data:
        text = obj['text'].lower()
        #award_regex = r"(best(?=\s[a-z])(?:\s([z-z]\w+|in|a|by an|\s-\s))+)"
        #match = re.search(award_regex, text)
        if "best" in text:#match != None:
            text = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', text)

            tokens = [tkn for tkn in text.split(" ") if valid_tkn(tkn, award_kw, award_sw + gg_sw + media_sw)]
            tokens = [tkn for tkn in tokens if tkn in list_of_awards]


            # ngrams of 2
            ngrams = zip(*[tokens[i:] for i in range(2)])
            ngrams = [" ".join(ngram) for ngram in ngrams]


            # # ngrams of 4
            # ngrams4 = zip(*[tokens[i:] for i in range(4)])
            # ngrams4 = ["best "+" ".join(ngram) for ngram in ngrams4]

            # # ngrams of 5
            # ngrams5 = zip(*[tokens[i:] for i in range(5)])
            # ngrams5 = ["best "+" ".join(ngram) for ngram in ngrams5]

            # # ngrams of 6
            # ngrams6 = zip(*[tokens[i:] for i in range(6)])
            # ngrams6 = ["best "+" ".join(ngram) for ngram in ngrams6]

            # # ngrams of 7
            # ngrams7 = zip(*[tokens[i:] for i in range(7)])
            # ngrams7 = ["best "+" ".join(ngram) for ngram in ngrams6]

            #ngrams = ngrams4 + ngrams5 + ngrams6 + ngrams7

            for tkn in ngrams:
                # if "best" in tkn[0]
                # tkn[1] == next_tkn[0]
                if tkn not in award_dict:
                    award_dict[tkn] = 1
                else:
                    award_dict[tkn] += 1
    award_lst = sorted(award_dict.items(), key=lambda x: x[1], reverse=True)
    return award_set(award_lst)
    # return award_set([
    #     ("motion picture", 1000),
    #     ("actor motion", 1000),
    #     ("supporting actor", 1000),
    #     ("picture drama", 1000),
    #     ("picture comedy", 1000),
    #     ("comedy musical", 1000),
    #     # ("motion picture", 100),
    #     # ("motion picture", 100),
    #     # ("motion picture", 100),

    # ])
