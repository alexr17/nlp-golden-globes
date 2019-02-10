import nltk
from nltk.corpus import stopwords
from src.helpers.find import find_name_with_db
from src.helpers.load import load_json, get_movies
from src.helpers.clean import valid_tkn, bigrams

stopwords = set(stopwords.words('english'))
stopwords.add('-')

winners_kw = ['wins', 'win']
winners_sw = ["best", "award", "performance"]
gg_sw = ['golden', 'globes', 'goldenglobes', 'globe']


def find_winner(award, data):
    award_dict = {}

    award_lst = award.split(" ")
    award_lst = [x for x in award_lst if x not in stopwords and x not in winners_sw]
    award = " ".join(award_lst)

    winners_sw.extend([word for word in award.split(' ')])

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

def clean_award_name(award):
    tokens = nltk.word_tokenize(award)
    print(tokens)