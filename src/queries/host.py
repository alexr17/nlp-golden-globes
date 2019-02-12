import nltk
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, bigrams
from src.helpers.find import find_name

# golden globes stopwords
gg_sw = ['golden', 'globes', 'goldenglobes', 'globe']

# host stopwords
host_sw = ['next', 'year', 'host', 'hosts']

# host keywords
host_kw = []

def find_hosts(data):
    # host
    host_dict = {}

    for obj in data:
        if 'host' in obj['text']:
            tokens = nltk.word_tokenize(obj['text'])
            # tokens = bigrams(nltk.word_tokenize(obj['text']), host_kw, host_sw + gg_sw)
            for tkn in tokens:
                tkn = tkn.lower()
                if valid_tkn(tkn, host_kw, host_sw + gg_sw):
                    if tkn not in host_dict:
                        host_dict[tkn] = 1
                    else:
                        host_dict[tkn] += 1

    #host_keys = host_dict.keys()
    host_lst = sorted(host_dict.items(), key=lambda x: x[1], reverse=True)
    return find_name(host_lst, host_dict)

