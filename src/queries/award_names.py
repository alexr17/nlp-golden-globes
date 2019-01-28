import nltk
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn
from src.helpers.clean import bigrams
import pprint
#from src.helpers.find import find_name

# golden globes stopwords
gg_sw = ['golden', 'globe', 'globes', 'goldenglobes']

# award stopwords
award_sw = ['year', 'show', 'award', 'awards']

# award keywords
award_kw = ['award', 'best', 'actor', 'actress', "supporting"]
def find_awards(data, year):
    award_dict = {}

    best_dict = {
        'nxt': {},
        'nxt_two': {},
        'nxt_three': {}
    }

    for obj in data:
        if 'best' in obj['text'].lower():
            # if 'award for best' in obj['text'].lower():
            #     pprint.pprint(obj['text'])
            # tokens = nltk.word_tokenize(obj['text'])
            # tokens = [nltk.bigrams(nltk.word_tokenize(s)) for s in nltk.sent_tokenize(obj['text'])]
            tokens = bigrams(nltk.word_tokenize(obj['text']), award_kw, gg_sw + award_sw)
            #print(tokens)
            for i, tkn in enumerate(tokens):
                tkn = tkn.lower()
                if valid_tkn(tkn, award_kw) and not tkn in gg_sw + award_sw:
                    if tkn not in award_dict:
                        award_dict[tkn] = 1
                    else:
                        award_dict[tkn] += 1

                    if tkn is 'best':
                        try:
                            tkn_j = tokens[i+1]
                            if tkn_j not in best_dict['nxt']:
                                best_dict['nxt'][tkn_j] = 1
                            else:
                                best_dict['nxt'][tkn_j] += 1
                            tkn_j += ' ' + tokens[i+2]
                            if tkn_j not in best_dict['nxt_two']:
                                best_dict['nxt_two'][tkn_j] = 1
                            else:
                                best_dict['nxt_two'][tkn_j] += 1
                            tkn_j += ' ' + tokens[i+3]
                            if tkn_j not in best_dict['nxt_three']:
                                best_dict['nxt_three'][tkn_j] = 1
                            else:
                                best_dict['nxt_three'][tkn_j] += 1
                        except IndexError:
                            continue
    #award_keys = award_dict.keys()
    award_lst = sorted(award_dict.items(), key=lambda x: x[1], reverse=True)
    return award_lst
    #return find_name(award_lst, award_dict)
