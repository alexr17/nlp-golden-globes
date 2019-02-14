import nltk
import re
import time
from nltk.corpus import stopwords
from src.helpers.find import find_name_with_db, find_title
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, unigrams, bigrams, trigrams
from src.helpers.debug import top_keys
import json

winners_kw = {}
gg_sw = {'golden', 'globes', 'goldenglobes', 'globe'}
award_sw = {"best", "award", "performance", 'made', 'role', 'any', '-'}
media_sw = {"eonline", 'cnnshowbiz', 'cinema21'}

def generate_winners_sw(awards):
    return set((' '.join(awards)).split(' ') + ['movie', 'tv','miniseries'])

def generate_awards_map(awards):
    awards_map = {}
    for award in awards:
        award_lst = [tkn for tkn in re.sub('[^a-zA-Z. ]', '', award).split(' ') if valid_tkn(tkn, [], award_sw)]
        awards_map[award] = g_map(award_lst)
    return awards_map

def find_winner(winner_dict, award):

    winner_lst = sorted(winner_dict.items(), key=lambda x: x[1], reverse=True)
    # print("Top keys for: " + award)
    # top_keys(winner_lst, 50)
    if any(word in award for word in ['actress', 'actor', 'director', 'award']): # name award
        winner = find_name_with_db(winner_lst)
    else:
        winner = find_title(winner_lst)
    return winner

def eval_winner_tweet(tweet, dicts, maps, keys, sw):
    # tokens = bigrams(tweet.split(' '), winners_kw, winners_sw + gg_sw + media_sw + list(map.keys()))
    tokens = nltk.word_tokenize(tweet)
    bgms = bigrams(tokens, winners_kw, sw | gg_sw | media_sw)
    tkns = unigrams(tokens, winners_kw, sw | gg_sw | media_sw)
    for key in keys:
        # TODO: fix this so it has an overarching list of keys for the awards (perhaps write a method?)
        for bgm in bgms:
            if bgm not in dicts[key]:
                dicts[key][bgm] = 1
            else:
                dicts[key][bgm] += 1

def id_award(tweet, award_map):
    for award_key in award_map:

        # check if the parent key is the string
        if award_key not in tweet:

            # if not then check if the child keys are
            if not any(rel_key in tweet for rel_key in award_map[award_key]):

                # did not pass test
                return False

    return True

def g_map(lst):
    map = {}
    for e in lst:
        # actor keywords
        if e == 'actress':
            map[e] = ['actriz']
        elif e == 'television' or e == 'series':
            map['television'] = ['series', 'tv', 'show']
        elif e == 'motion' or e == 'picture':
            map['motion'] = ['picture', 'movie']
        elif e == 'miniseries':
            map[e] = ['mini-series', 'mini']
        elif e == 'comedy' or e == 'musical':
            map['comedy'] = ['musical']
        else:
            map[e] = []

    return map

