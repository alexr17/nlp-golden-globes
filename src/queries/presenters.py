import nltk
import re
import time
from nltk.corpus import stopwords
from src.helpers.find import find_name
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, bigrams, trigrams
import json

presenters_kw = []
presenters_sw = ['wins', 'winning', "best", "award", "performance", 'wins', 'actress', 'actor', 'supporting', 'tv', 'drama', 'comedy', 'musical', 'motion', 'picture', 'movie', 'television', 'series']
gg_sw = ['golden', 'globes', 'goldenglobes', 'globe']
award_sw = ["best", "award", "performance", 'made', 'role', 'any']
media_sw = ["eonline", 'cnnshowbiz', 'cinema21']

def find_presenter(data, award_name):
    award_dict = {}
    award_lst = [tkn for tkn in re.sub('[^a-zA-Z. ]', '', award_name).split(' ') if valid_tkn(tkn, [], award_sw)]
    award_map = g_map(award_lst)

    for obj in data:
        bl = id_award(obj['text'].lower(), award_map)
        # if all(word in obj['text'].lower() for word in ['actor', 'miniseries', 'tv', 'movie']):
        if bl:
            tokens = bigrams(nltk.word_tokenize(obj['text'].lower()), presenters_kw, presenters_sw + gg_sw + media_sw)
            for tkn in tokens:
                if tkn not in award_dict:
                    award_dict[tkn] = 1
                else:
                    award_dict[tkn] += 1

    award_lst = sorted(award_dict.items(), key=lambda x: x[1], reverse=True)
    return find_name(award_lst, [])

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
    map = {'present': ['introduce']}
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

