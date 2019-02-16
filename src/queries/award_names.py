import nltk
import re
from collections import Counter
from nltk import ngrams
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn
from src.helpers.clean import bigrams
from src.helpers.clean import join_ngrams
from src.helpers.debug import top_keys
#from src.helpers.clean import join_ngrams
from src.helpers.clean import trigrams
from src.helpers.clean import merge_bigrams
import pprint
#from src.helpers.find import find_name

list_of_awards = set(line.strip() for line in open('./data/award_kw.txt'))

# golden globes stopwords
gg_sw = ['golden', 'globe', 'globes', 'goldenglobes']

# list of televsion, movie, and music

# award stopwords
award_sw = ['year', 'show', 'award', 'awards', 'wins', 'best']

# media stopwords
media_sw = ['eonline', 'cnnshowbiz']

# award keywords
award_kw = ['actor', 'actress', 'supporting']

answer = {}


def find_awards(data):
    award_dict = {}

    best_dict = {
        'nxt': {},
        'nxt_two': {},
        'nxt_three': {}
    }
#     >>> from collections import Counter
# >>> from nltk import ngrams
# >>> bigtxt = open('big.txt').read()
# >>> ngram_counts = Counter(ngrams(bigtxt.split(), 2))
# >>> ngram_counts.most_common(10)




    for obj in data:
        text = obj['text'].lower()
        #award_regex = r"(best(?=\s[a-z])(?:\s([z-z]\w+|in|a|by an|\s-\s))+)"
        #match = re.search(award_regex, text)
        if "best" in text:#match != None:
            text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

            tokens = [tkn for tkn in text.split(" ") if valid_tkn(tkn, award_kw, award_sw + gg_sw + media_sw)]
            tokens = [tkn for tkn in tokens if tkn in list_of_awards]

            # ngrams of 4
            ngrams4 = zip(*[tokens[i:] for i in range(4)])
            ngrams4 = ["best "+" ".join(ngram) for ngram in ngrams4]

            # ngrams of 5
            ngrams5 = zip(*[tokens[i:] for i in range(5)])
            ngrams5 = ["best "+" ".join(ngram) for ngram in ngrams5]

            # ngrams of 6
            ngrams6 = zip(*[tokens[i:] for i in range(6)])
            ngrams6 = ["best "+" ".join(ngram) for ngram in ngrams6]

            # ngrams of 7
            ngrams7 = zip(*[tokens[i:] for i in range(7)])
            ngrams7 = ["best "+" ".join(ngram) for ngram in ngrams6]

            ngrams = ngrams4 + ngrams5 + ngrams6 + ngrams7

            for tkn in ngrams:
                # if "best" in tkn[0]
                # tkn[1] == next_tkn[0]
                if tkn not in award_dict:
                    award_dict[tkn] = 1
                else:
                    award_dict[tkn] += 1
    award_lst = sorted(award_dict.items(), key=lambda x: x[1], reverse=True)
    return award_lst
