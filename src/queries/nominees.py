import nltk
from src.helpers.load import load_json, get_movies
from src.helpers.clean import valid_tkn, bigrams

nominees_kw = []
nominees_sw = ["best", "award", "performance"]
gg_sw = ['golden', 'globes', 'goldenglobes', 'globe']
movies = set(get_movies(2013))
def find_nominee(award, data):
    nom_dict = {}
    nominees_sw.extend([word for word in award.split(' ')])

    for obj in data:
        if award in obj['text'].lower():  
            tokens = nltk.word_tokenize(obj['text'])
            # tokens = bigrams(nltk.word_tokenize(obj['text']), host_kw, host_sw + gg_sw)
            for tkn in tokens:
                tkn = tkn.lower()
                if valid_tkn(tkn, nominees_kw, nominees_sw + gg_sw):
                    if tkn not in nom_dict:
                        nom_dict[tkn] = 1
                    else:
                        nom_dict[tkn] += 1
    nom_lst = sorted(nom_dict.items(), key=lambda x: x[1], reverse=True)
    for nom in nom_lst:
        if nom[0].title() in movies:
            print(nom)
    return nom_lst