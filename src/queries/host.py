import nltk
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn
from src.helpers.find import find_name

# golden globes stopwords
gg_sw = ['golden', 'globes']

# host stopwords
host_sw = ['next', 'year', 'host']

host_keywords = []

def find_hosts(data, year):
    # host
    host_dict = {}

    for obj in data:
        if 'host' in obj['text']:
            tokens = nltk.word_tokenize(obj['text'])
            for tkn in tokens:
                tkn = tkn.lower()
                if valid_tkn(tkn, host_keywords) and not any(substr in tkn for substr in gg_sw + host_sw):
                    if tkn not in host_dict:
                        host_dict[tkn] = 1
                    else:
                        host_dict[tkn] += 1

    #host_keys = host_dict.keys()
    host_lst = sorted(host_dict.items(), key=lambda x: x[1], reverse=True)
    return find_name(host_lst, host_dict)

