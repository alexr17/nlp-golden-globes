import nltk
import re
import time
from nltk.corpus import stopwords
from src.helpers.find import find_name, find_title
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, unibigrams, bigrams, trigrams
from src.helpers.debug import top_keys
import json

nominees_kw = []
nominees_sw = {'movie', 'tv','miniseries', 'win', 'wins', 'goes', 'winner', 'won', 'lose', 'lost', 'nominated', 'nominee', 'present'}
gg_sw = {'golden', 'globes', 'goldenglobes', 'globe'}
award_sw = {"best", "award", "performance", 'made', 'role', 'any', '-'}
media_sw = {"eonline", 'cnnshowbiz', 'cinema21'}
debug_awards = {"best motion picture - comedy or musical",'best motion picture - drama','best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television'}

def generate_nominees_sw(awards):
    return set((' '.join(awards)).split(' ')) | nominees_sw

def find_nominee(nominee_dict, award, other_nominees, other_winners):    
    if not len(nominee_dict):
        print("Could not find a nominee for: " + award)
        return []

    nominee_lst = sorted(nominee_dict.items(), key=lambda x: x[1], reverse=True)
    print("\n\n\nTop keys for nominees for: " + award)
    top_keys(nominee_lst, 0)
    print(other_winners)
    if any(word in award for word in {'actress', 'actor', 'director', 'award'}):
        nominees = find_name(nominee_lst, other_nominees['name'] | other_nominees['title'] | other_winners, award, 4)
        other_nominees['name'] = other_nominees['name'] | nominees
    else: # titles
        nominees = find_title(nominee_lst, other_nominees['name'] | other_winners, award, 4)
        other_nominees['title'] = other_nominees['name'] | nominees
    return list(nominees)

def eval_nominee_tweet(tweet, dicts, keys, sw, awards_map):
    # tokens = bigrams(tweet.split(' '), winners_kw, winners_sw + gg_sw + media_sw + list(map.keys()))
    tokens = nltk.word_tokenize(tweet)
    
    gms = unibigrams(tokens, nominees_kw, sw | gg_sw | media_sw)
    for key in keys:
        if awards_map[key]['person']:
            tkns = gms['bi']
        else:
            tkns = gms['uni'] | gms['bi']
        for bgm in tkns:
            if bgm not in dicts[key]:
                dicts[key][bgm] = 1
            else:
                dicts[key][bgm] += 1