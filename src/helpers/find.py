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

def find_name_generic(lst, exclude_list, type_set, award, optional=False, no_max=False):
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
            if i == 0:
                max = lst[0][1]
            continue

        top_tpls.append(lst[i])
        if lst[i][0] in type_set:
            return lst.pop(i)[0]
        i += 1
    
    # print("\nCould not find name for award: " + award)
    # print(top_tpls)
    # finesse_name(top_tpls)
    #defaulting
    if optional:
        return False
    return lst.pop(0)[0]

def find_name(lst, exclude_list, award, max=1):
    names_set = load_imdb_data('name')
    optional = False
    if max == 1:
        return find_name_generic(lst, exclude_list, names_set, award, optional, False)
    
    names = set()
    
    for x in range(max):
        name = find_name_generic(lst, exclude_list, names_set, award, optional, True)
        if name:
            names.add(name)
        if not len(lst):
            return names
        optional = True
    return names


def find_title(lst, exclude_list, award, max=1):
    titles_set = load_imdb_data('title')
    if max == 1:
        return find_name_generic(lst, exclude_list, titles_set, award)