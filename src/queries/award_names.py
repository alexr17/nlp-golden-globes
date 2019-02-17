import nltk
import re
import difflib
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


# Used intersection of tweet set and tweet indexing from the following project:
# https://github.com/brownrout/EECS-337-Golden-Globes/blob/master/gg_api.py
def find_awards(data):
    all_awards = {}
    similar_names = {}
    award_tweets = []
    bigrams_dict = {}
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
        temp1 = []
        #print(tweet[start:end+1])
        for word in tweet[start:end+1]:
            if word in list_of_awards and word not in helper_words:
                temp1.append(word)
            if word in list_of_awards or word in helper_words:
                temp.append(word)

        award = ' '.join(sorted(set(temp), key=lambda x: tweet.index(x)))
        temp1 = ' '.join(sorted(set(temp1), key=lambda x: tweet.index(x)))

        # print(award)
        # print('----')

        if temp1 in similar_names:
            similar_names[temp1].append(award)
        else:
            similar_names[temp1] = [award]

        if award in all_awards:
            all_awards[award] += 1
        else:
            all_awards[award] = 1

        # Find common phrases
        tokens = sorted(set(temp1.split(" ")), key=lambda x: tweet.index(x))
        bigrams = [[tokens[i]] + [tokens[i+1]] for i in range(len(tokens)-1)]
        bigrams = [" ".join(ngram) for ngram in bigrams]
        for tkn in bigrams:
            if tkn not in bigrams_dict:
                 bigrams_dict[tkn] = 1
            else:
                 bigrams_dict[tkn] += 1

    bigrams_lst = sorted(bigrams_dict.items(), key=lambda x: x[1], reverse=True)

    common_phrases = [x[0] for x in bigrams_lst if x[1] > 50]
    #common_phrases = ["motion picture", "supporting role", "best performance", "television series", "original score", "original song"]


    new_award_lst = []
    for key in similar_names:
        max_score = 0
        max_award = ""
        for award in similar_names[key]:
            if all_awards[award] > max_score:
                max_score = all_awards[award]
                max_award = award
        #new_award_lst.append(max_award)
        if [phrase in max_award for phrase in common_phrases].count(True) > 1:
            new_award_lst.append(max_award)

    new_award_lst = [x for x in new_award_lst if x.split(" ")[0] == "best"]
    threshold = 0.85
    removed_awards = []
    for i, x in enumerate(new_award_lst):
        x1 = set([a for a in x.split(" ")])
        for j, y in enumerate(new_award_lst[i+1:]):
            y1 = set([a for a in y.split(" ")])
            if len(x1.intersection(y1)) >= threshold*len(x1):
                if not ('actor' in x and 'actress' in y or 'actor' in y and 'actress' in x):
                    if not ('actor' in x and 'actor' not in y or 'actress' in x and 'actress' not in y):
                        removed_awards.append(x)

    removed_awards = set(removed_awards)
    for a in removed_awards:
        if a in new_award_lst:
            new_award_lst.remove(a)
    return new_award_lst



# def get_phrases(bigrams):
#     updated_lst = []
#     for i in range(len(bigrams)):
#         curr = bigrams[i]
#         j = i+1
#         while j < len(bigrams):
#             bigram1 = curr.split(" ")
#             bigram2 = bigrams[j].split(" ")
#             if bigram1[-1] == bigram2[0]:
#                 ngram = bigram1 + [bigram2[-1]]
#                 updated_lst.append(" ".join(ngram))
#             if bigram1[0] == bigram2[-1]:
#                 ngram = bigram2 + [bigram1[-1]]
#                 updated_lst.append(" ".join(ngram))
#             j += 1
#     return updated_lst

# def award_set(bigrams):
#     all_awards = []
#     for i, bigram1 in enumerate(bigrams):
#         ngram = bigram1.split(" ")
#         for j, bigram2 in enumerate(bigrams):
#             if bigram2 == bigram1:
#                 continue
#             bigram = bigram2.split(" ")
#             if ngram[-1] == bigram[0]:
#                ngram += bigram[1:]
#             elif ngram[0] == bigram[-1]:
#                 ngram = [bigram[0]] + ngram
#         ngram = " ".join(ngram)
#         flag = False
#         for award in all_awards:
#             if ngram in award:
#                 flag = True
#                 break
#         if not flag:
#             all_awards.append(ngram)

#     return all_awards

