import nltk
import re
import time
from nltk.corpus import stopwords
from src.helpers.find import find_name, find_title
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, unigrams, bigrams, trigrams
from src.helpers.debug import top_keys
import json

winners_kw = []
winners_sw = {'movie', 'tv','miniseries', 'win', 'wins', 'goes'}
gg_sw = {'golden', 'globes', 'goldenglobes', 'globe'}
award_sw = {"best", "award", "performance", 'made', 'role', 'any', '-'}
media_sw = {"eonline", 'cnnshowbiz', 'cinema21'}
debug_awards = {}#{"best motion picture - comedy or musical",'best motion picture - drama','best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television'}

def generate_winners_sw(awards):
    return set((' '.join(awards)).split(' ')) | winners_sw

def generate_awards_map(awards):
    awards_map = {}
    for award in awards:
        award_lst = [tkn for tkn in re.sub('[^a-zA-Z. ]', '', award).split(' ') if valid_tkn(tkn, [], award_sw)]
        awards_map[award] = g_map(award_lst)
    return awards_map

def find_winner(winner_dict, award, other_winners):    
    
    winner_lst = sorted(winner_dict.items(), key=lambda x: x[1], reverse=True)
    if award in debug_awards:
        print("\n\n\nTop keys for: " + award)
        top_keys(winner_lst, 50)
    # people
    if any(word in award for word in {'actress', 'actor', 'director', 'award'}):
        winner = find_name(winner_lst, other_winners, award)
        other_winners['name'].add(winner)
    else: # titles
        winner = find_title(winner_lst, other_winners, award)
        other_winners['title'].add(winner)
    return winner

def eval_winner_tweet(tweet, dicts, maps, keys, sw):
    # tokens = bigrams(tweet.split(' '), winners_kw, winners_sw + gg_sw + media_sw + list(map.keys()))
    tokens = nltk.word_tokenize(tweet)
    bgms = bigrams(tokens, winners_kw, sw | gg_sw | media_sw)
    ugms = unigrams(tokens, winners_kw, sw | gg_sw | media_sw)
    for key in keys:
        # TODO: fix this so it has an overarching list of keys for the awards (perhaps write a method?)
        for bgm in bgms:
            if bgm not in dicts[key]:
                dicts[key][bgm] = 1
            else:
                dicts[key][bgm] += 1

        # DON'T ADD UNIGRAMS TO AWARDS WITH PEOPLE AS WINNERS PEOPLE DON'T HAVE ONE WORD IN THEIR NAMES
        if not any(word in key for word in ['actress', 'actor', 'director', 'award']):
            for ugm in ugms:
                if ugm not in dicts[key]:
                    dicts[key][ugm] = 1
                else:
                    dicts[key][ugm] += 1

def id_award(tweet, award_map):
    for award_key in award_map['include']:
        # if not then check if the child keys are
        if not any(rel_key in tweet for rel_key in ([award_key] + award_map['include'][award_key])):

            # did not pass test
            return False

    for award_key in award_map['exclude']:
         
        if any(rel_key in tweet for rel_key in ([award_key] + award_map['exclude'][award_key])):

            return False
    return True

def g_map(lst):
    map = {
        'include': {},
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

