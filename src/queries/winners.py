import nltk
import re
import time
from nltk.corpus import stopwords
from src.helpers.find import find_name_with_db, find_title
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, bigrams, trigrams
import json

winners_kw = []
winners_sw = ['wins', 'winning', "best", "award", "performance", 'wins', 'actress', 'actor', 'supporting', 'tv', 'drama', 'comedy', 'musical', 'motion', 'picture', 'movie', 'television', 'series']
gg_sw = ['golden', 'globes', 'goldenglobes', 'globe']
award_sw = ["best", "award", "performance", 'made', 'role', 'any', '-']
media_sw = ["eonline", 'cnnshowbiz', 'cinema21']

def generate_awards_map(awards):
    awards_map = {}
    for award in awards:
        award_lst = [tkn for tkn in re.sub('[^a-zA-Z. ]', '', award).split(' ') if valid_tkn(tkn, [], award_sw)]
        awards_map[award] = g_map(award_lst)
    return awards_map

def find_winner(winner_dict, award):    

    winner_lst = sorted(winner_dict.items(), key=lambda x: x[1], reverse=True)
    if any(word in award for word in ['actress', 'actor', 'director', 'award']): # name award
        winner = find_name_with_db(winner_lst)
    else:
        winner = find_title(winner_lst)
    return winner

def eval_winner_tweet(tweet, dct, map):
    bl = id_award(tweet, map)
    # if all(word in obj['text'].lower() for word in ['actor', 'miniseries', 'tv', 'movie']):
    if bl:
        tokens = bigrams(nltk.word_tokenize(tweet), winners_kw, winners_sw + gg_sw + media_sw + list(map.keys()))
        for tkn in tokens:
            if tkn not in dct:
                dct[tkn] = 1
            else:
                dct[tkn] += 1

def id_award(string, award_map):
    for award_key in award_map:

        # check if the parent key is the string
        if award_key not in string:

            # if not then check if the child keys are
            if not any(rel_key in string for rel_key in award_map[award_key]):

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

