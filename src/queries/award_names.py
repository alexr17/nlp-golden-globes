import nltk
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn
from src.helpers.clean import bigrams
from src.helpers.debug import top_keys
#from src.helpers.clean import join_ngrams
from src.helpers.clean import trigrams
from src.helpers.clean import merge_bigrams
import pprint
#from src.helpers.find import find_name

# golden globes stopwords
gg_sw = ['golden', 'globe', 'globes', 'goldenglobes']

# award stopwords
award_sw = ['year', 'show', 'award', 'awards']

# media stopwords
media_sw = ['eonline', 'cnnshowbiz']

# award keywords
award_kw = ['actor', 'actress', 'supporting']

def find_awards(data, year):
    award_dict = {}

    best_dict = {
        'nxt': {},
        'nxt_two': {},
        'nxt_three': {}
    }

    for obj in data:
        if 'best' in obj['text'].lower():
            # tokens = [nltk.bigrams(nltk.word_tokenize(s)) for s in nltk.sent_tokenize(obj['text'])]
            # tokens = bigrams(nltk.word_tokenize(obj['text']), award_kw, gg_sw + award_sw + media_sw)
            tokens = trigrams(nltk.word_tokenize(obj['text']), award_kw, gg_sw + award_sw + media_sw)

            #print(tokens)
            for i, tkn in enumerate(tokens):

                # if "best" in tkn[0]
                # tkn[1] == next_tkn[0]
                tkn = tkn.lower()
                if tkn not in award_dict:
                    award_dict[tkn] = 1
                else:
                    award_dict[tkn] += 1
    award_lst = sorted(award_dict.items(), key=lambda x: x[1], reverse=True)
    return award_lst
