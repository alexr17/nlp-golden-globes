import nltk
import re
import time
from nltk.corpus import stopwords
from src.helpers.find import find_name, find_title
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, bigrams, trigrams
from src.helpers.debug import top_keys
import json

presenters_kw = []
presenters_sw = {'movie', 'tv','miniseries', 'win', 'wins', 'goes', 'present', 'presenting', 'presented', 'mejor', 'actriz'}
gg_sw = {'golden', 'globes', 'goldenglobes', 'globe', '@goldenglobes', '#goldenglobes'}
award_sw = {"best", "award", "performance", 'made', 'role', 'any', '-'}
media_sw = {"eonline", 'cnnshowbiz', 'cinema21', 'vanityfair'}
debug_awards = {'best performance by an actress in a motion picture - comedy or musical','best performance by an actress in a supporting role in a motion picture','best performance by an actress in a television series - comedy or musical'}

def generate_presenters_sw(awards):
    return set((' '.join(awards)).split(' ')) | presenters_sw

def find_presenter(presenter_dict, award, other_presenters, winner):
    if not len(presenter_dict):
        print("Could not find a presenter for: " + award)
        return ['aeiouprst']
    presenter_lst = sorted(presenter_dict.items(), key=lambda x: x[1], reverse=True)
    # if award in debug_awards:
    #     print("\n\nTop keys for: " + award)
    #     top_keys(presenter_lst, 0)
    presenters = find_name(presenter_lst, {winner}, award, 2)
    other_presenters = other_presenters | presenters
    return list(presenters)

def eval_presenter_tweet(tweet, dicts, keys, sw):
    tokens = nltk.word_tokenize(tweet)
    bgms = bigrams(tokens, presenters_kw, sw | gg_sw | media_sw)
    for key in keys:
        # TODO: fix this so it has an overarching list of keys for the awards (perhaps write a method?)
        for bgm in bgms:
            if bgm not in dicts[key]:
                dicts[key][bgm] = 1
            else:
                dicts[key][bgm] += 1

def g_map(lst):
    map = {
        'include': {
            'present': ['introduc', 'award best']
        },
        'exclude': {
            'host': []
        }
    }
    for e in lst:
        # actor keywords
        if e == 'actress':
            map['include'][e] = ['actriz']
        elif e == 'television' or e == 'series':
            map['include']['television'] = ['series', 'tv']
        elif e == 'motion' or e == 'picture':
            map['include']['motion'] = ['picture', 'movie']
        elif e == 'miniseries':
            map['include'][e] = ['mini-series', 'mini']
        elif e == 'comedy' or e == 'musical':
            map['include']['comedy'] = ['musical']
        elif e == 'drama':
            map['include']['drama'] = ['dramático']
        else:
            map['include'][e] = []

    # if map generated for best actor and not supporting actor, then exclude supporting from search
    if 'supporting' not in map['include'] and any(word in map['include'] for word in ['actress', 'actor']):
        map['exclude']['supporting'] = []

    # if non-actor award, exclude actor/actress from results
    if not any(word in map['include'] for word in ['actress', 'actor']):
        map['exclude']['actress'] = ['actriz', 'actor']
    
    # if non movie award:
    # if 'motion' in map['include'] and 'television' not in map['include']:
    #     map['exclude']['television'] = ['tv', 'series', 'miniseries', 'show']
    # elif 'motion' not in map['include'] and 'television' in map['include']:
    #     map['exclude']['motion'] = ['picture', 'movie']
    return map

