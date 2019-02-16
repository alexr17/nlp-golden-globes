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


def finesse_name(tpls):
    if len(tpls) < 3:
        return tpls[0][0]
    
    unigrams = {}
    ngrams = {}
    for tpl in tpls:
        if len(tpl[0].split(' ')) == 1:
            unigrams[tpl[0]] = tpl[1]
        else:
            ngrams[tpl[0]] = tpl[1]

    print(unigrams)
    print(ngrams)

def find_name_generic(lst, other_winners, type_set, award):
    max = lst[0][1]
    top_tpls = []
    i = 0
    while lst[i][1] > max * 0.5:

        # if it exists somewhere else then remove it
        if lst[i][0] in other_winners:
            lst.pop(i)
            continue

        top_tpls.append(lst[i])
        if lst[i][0] in type_set:
            return lst[i][0]
        i += 1
    
    print("\n\nCould not find name for award: " + award)
    print(top_tpls)
    # finesse_name(top_tpls)
    #defaulting
    return lst[0][0]

def find_name(lst, other_winners, award):
    names_set = load_imdb_data('name')
    return find_name_generic(lst, other_winners['name'] | other_winners['title'], names_set, award)


def find_title(lst, other_winners, award):
    titles_set = load_imdb_data('title')
    return find_name_generic(lst, other_winners['name'], titles_set, award)