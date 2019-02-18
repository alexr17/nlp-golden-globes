import nltk
import re
import time
from nltk.corpus import stopwords
from src.helpers.find import find_name, find_title
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, unibigrams, bigrams, trigrams
from src.helpers.debug import top_keys
import json

winners_kw = []
winners_sw = {'movie', 'tv','miniseries', 'win', 'wins', 'goes', 'winner', 'won'}
gg_sw = {'golden', 'globes', 'goldenglobes', 'globe'}
media_sw = {"eonline", 'cnnshowbiz', 'cinema21'}
debug_awards = {}#{"best motion picture - comedy or musical",'best motion picture - drama','best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television'}

def generate_winners_sw(awards):
    return set((' '.join(awards)).split(' ')) | winners_sw


def find_winner(winner_dict, award, other_winners):    
    
    winner_lst = sorted(winner_dict.items(), key=lambda x: x[1], reverse=True)
    if award in debug_awards:
        print("\n\n\nTop keys for: " + award)
        top_keys(winner_lst, 50)
    # people
    if any(word in award for word in {'actress', 'actor', 'director', 'award'}):
        winner = find_name(winner_lst, other_winners['name'] | other_winners['title'], award)
        other_winners['name'].add(winner)
    else: # titles
        winner = find_title(winner_lst, other_winners['name'], award)
        other_winners['title'].add(winner)
    return winner

def eval_winner_tweet(tweet, dicts, keys, sw, awards_map):
    # tokens = bigrams(tweet.split(' '), winners_kw, winners_sw + gg_sw + media_sw + list(map.keys()))
    tokens = nltk.word_tokenize(tweet)
    
    gms = unibigrams(tokens, winners_kw, sw | gg_sw | media_sw)
    for key in keys:
        if any(word in key for word in {'actress', 'actor', 'director', 'award'}):
            tkns = gms['bi']
        else:
            tkns = gms['uni'] | gms['bi']
        for bgm in tkns:
            if bgm not in dicts[key]:
                dicts[key][bgm] = 1
            else:
                dicts[key][bgm] += 1

def g_map(lst):
    map = {
        'include': {
            
        },
        'exclude': {}
    }
    for e in lst:
        # actor keywords
        if e == 'actress':
            map['include'][e] = ['actriz']
        elif e == 'television' or e == 'series':
            map['include']['television'] = ['series', 'tv', 'show']
        elif e == 'motion' or e == 'picture':
            map['include']['motion'] = ['picture', 'movie']
        elif e == 'miniseries':
            map['include'][e] = ['mini-series', 'mini']
        elif e == 'comedy' or e == 'musical':
            map['include']['comedy'] = ['musical']
        else:
            map['include'][e] = []

    # if map generated for best actor and not supporting actor, then exclude supporting from search
    if 'supporting' not in map['include'] and any(word in map['include'] for word in ['actress', 'actor']):
        map['exclude']['supporting'] = []

    # if non-actor award, exclude actor/actress from results
    if not any(word in map['include'] for word in ['actress', 'actor']):
        map['exclude']['actress'] = ['actriz', 'actor']
    return map

