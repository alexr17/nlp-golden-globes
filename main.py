import json
import nltk
import math
import re
from nltk.corpus import stopwords
from debug import top_keys

stopwords = set(stopwords.words('english'))
year = '2015'
with open('./data/gg'+year+'.json') as f:
    data = json.load(f)

# print(len(data))
# filter out token
def valid_tkn(word):
    # stopwords
    if word in stopwords:
        return False

    # ampersand and twitter link
    twitter_stop = ['&amp;', '//t.co/', 'rt', 'http']
    if any(substr in word for substr in twitter_stop):
        return False

    # special unicode character
    if r'\u' in word:
        return False
    regex = re.compile('[^a-zA-Z]')
    word = regex.sub('', word)
    if len(word) < 2:
        return False
    return True

# golden globes stopwords
gg_sw = ['golden', 'globes']

# host
host_dict = {}
host_sw = ['next', 'year', 'host']
for obj in data:
    if 'host' in obj['text']:
        tokens = nltk.word_tokenize(obj['text'])
        for tkn in tokens:
            tkn = tkn.lower()
            if valid_tkn(tkn) and not any(substr in tkn for substr in gg_sw + host_sw):
                if tkn not in host_dict:
                    host_dict[tkn] = 1
                else:
                    host_dict[tkn] += 1

# tries to find a name in a given list of tuples
def find_name(lst, name_dict):
    # gets the first names
    # print(lst)
    name_tpls = [lst[0]]
    for tpl in lst[1:]:
        if tpl[1]/lst[0][1] > .8: #similar frequency
            name_tpls.append(tpl)
        else:
            break

    # find last name(s)
    full_names = []
    for name_tpl in name_tpls:
        #matches = [s for s in keys if name in s]
        for tpl in lst[len(name_tpls):]:
            if name_tpl[0] in tpl[0]:
                last_name = tpl[0][len(name_tpl[0]):]
                try:
                    if name_dict[last_name]/name_tpl[1] > .25:
                        full_names.append(name_tpl[0].capitalize() + ' ' + last_name.capitalize())
                        break
                except KeyError:
                    pass
    return full_names

#host_keys = host_dict.keys()
host_lst = sorted(host_dict.items(), key=lambda x: x[1], reverse=True)
host_text = "The host(s) for the " + year + " Golden Globes are "
print(host_text + " and ".join(find_name(host_lst, host_dict)))
