import nltk
import re
import time
from nltk.corpus import stopwords
from src.helpers.find import find_name, find_title
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, bigrams, trigrams
from src.helpers.debug import top_keys
import json

presenters_kw = {}
presenters_sw = {'movie', 'tv','miniseries', 'win', 'wins', 'goes', 'present', 'presenting', 'presented', 'mejor', 'actriz'}
gg_sw = {'golden', 'globes', 'goldenglobes', 'globe', '@goldenglobes', '#goldenglobes'}
award_sw = {"best", "award", "performance", 'made', 'role', 'any', '-'}
media_sw = {"eonline", 'cnnshowbiz', 'cinema21', 'vanityfair'}
debug_awards = {}

def generate_presenters_sw(awards):
    return set((' '.join(awards)).split(' ')) | presenters_sw

def find_presenter(presenter_dict, award, other_presenters, winner):
    if not len(presenter_dict):
        print("Could not find a presenter for: " + award)
        return ['etaoin shrdlu']
    presenter_lst = sorted(presenter_dict.items(), key=lambda x: x[1], reverse=True)
    if award in debug_awards:
        print("\n\nTop keys for: " + award)
        top_keys(presenter_lst, 0)
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
