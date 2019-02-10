import nltk
import re
from nltk.corpus import stopwords
from src.helpers.find import find_name_with_db
from src.helpers.load import load_json, get_movies
from src.helpers.clean import valid_tkn, bigrams

winners_kw = ['don']
winners_sw = ["best", "award", "performance", 'wins', 'actress', 'actor', 'supporting', 'tv', 'drama', 'comedy', 'musical', 'motion', 'picture', 'movie', 'television', 'series']
gg_sw = ['golden', 'globes', 'goldenglobes', 'globe']
award_sw = ["best", "award", "performance", 'by', 'an', 'in', 'a', 'or']

def find_winner(data, award_name):
    award_dict = {}
    # award_lst = [x for x in re.sub('[^a-zA-Z]', ' ', award_name).split(' ') if x not in stopwords and x not in award_sw]
    award_lst = [x for x in award_name.split(' ') if x not in award_sw]
    print(award_lst)
    # regex = g_regex(award_lst)
    for obj in data:
        if all(word in obj['text'].lower() for word in award_lst):
            
            tokens = bigrams(nltk.word_tokenize(obj['text']), winners_kw, winners_sw + gg_sw)
            for tkn in tokens:
                tkn = tkn.lower()
                if tkn not in award_dict:
                    award_dict[tkn] = 1
                else:
                    award_dict[tkn] += 1
    award_lst = sorted(award_dict.items(), key=lambda x: x[1], reverse=True)
    return find_name_with_db(award_lst)

def g_regex(lst):
    regex = ['(win)', '(best)']
    for e in lst:
        # actor keywords
        if e == 'actress':
            # add spanish
            regex += ['(actriz)', '(actress)']
        elif e == 'television':
            regex += ['(television)', '(tv)']
        elif e == 'picture':
            regex += ['(motion picture)', '(movie)']
        else:
            regex.append('(' + e + ')')

    return '|'.join(regex)
        
