import itertools
from src.helpers.load import load_imdb_data
# tries to find a name in a given list of tuples
def find_host_names(lst, name_dict):
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
                        full_names.append(name_tpl[0] + ' ' + last_name)
                        break
                except KeyError:
                    pass
    return full_names

def recur_ngram(names, dct, key, string):
    if key in set(string):
        return string
    if key not in dct:
        return string + [key]
    ngrams = []
    string.append(key)
    for child in dct[key]:
        if ' '.join(string) in names:
            return ' '.join(string)
        new_string = recur_ngram(names, dct, child, string)
    return new_string

# dct = {'robert': {'downey', 'el'}, 'downey': {'jr.'}, 'jr.': {'presenta'}, 'hoy': {'el'}, 'quien': {'se'}, 'la': {'trayectoria'}, 'se': {'lleva'}, 'lleva': {'hoy'}, 'codiciado': {'premio'}, 'presenta': {'jodie'}}
# key = 'robert'
# print(recur_ngram(load_imdb_data('name'), dct, key, []))
def find_ngram(tkns, names, optional, exclude_list):
    if len(tkns) < 2 and not optional:
        return tkns[0][0]
    if len(tkns) > 10:
        tkns = tkns[:10]
    bgm_map = {}

    for tkn in tkns:
        sp_tkn = tkn[0].split(' ')
        if len(sp_tkn) == 2: # if it's a bigram
            if sp_tkn[0] in bgm_map:
                bgm_map[sp_tkn[0]].add(sp_tkn[-1])
            else:
                bgm_map[sp_tkn[0]] = {sp_tkn[-1]}
    
    best_ngrams = set()

    for tkn in bgm_map:
        name = recur_ngram(names, bgm_map, tkn, [])
        if type(name) == str and name not in exclude_list:
            return name
        elif not optional:
            best_ngrams.add(' '.join(name))
    
    if optional:
        return False
    else:
        return tkns[0][0]

def find_generic(lst, exclude_list, type_set, award, optional=False, no_max=False):
    max = lst[0][1]
    top_tpls = []
    i = 0
    threshold = 0.5
    if no_max:
        threshold = 0
    while i < len(lst) and lst[i][1] >= max * threshold:
        # print(i)
        # if it exists somewhere else then remove it
        if lst[i][0] in exclude_list:
            lst.pop(i)
            if i == 0 and not len(lst):
                max = lst[0][1]
            continue

        top_tpls.append(lst[i])
        if lst[i][0] in type_set:
            return lst.pop(i)[0]
        i += 1
    
    # print("\nCould not find generic for award: " + award)
    # print(top_tpls)
    return find_ngram(top_tpls, type_set, optional, exclude_list)
    #defaulting

def find_name(lst, exclude_list, award, max=1):
    names_set = load_imdb_data('name')
    optional = False
    if max == 1:
        return find_generic(lst, exclude_list, names_set, award, optional, False)
    
    names = set()
    
    for x in range(max):
        name = find_generic(lst, exclude_list | names, names_set, award, optional, True)
        if name:
            names.add(name)
        else:
            return names
        if not len(lst):
            return names
        optional = True
    return names


def find_title(lst, exclude_list, award, max=1):
    titles_set = load_imdb_data('title')
    optional = False
    if max == 1:
        return find_generic(lst, exclude_list, titles_set, award)

    titles = set()
    for x in range(max):
        title = find_generic(lst, exclude_list | titles, titles_set, award, optional, True)
        if title:
            titles.add(title)
        if not len(lst):
            return titles
        optional = True
    return titles
