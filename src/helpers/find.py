from src.helpers.load import load_imdb_data 
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
                        full_names.append(name_tpl[0] + ' ' + last_name)
                        break
                except KeyError:
                    pass
    return full_names

def find_name_with_db(lst, other_winners, award):
    names_set = load_imdb_data('name')
    max = lst[0][1]
    tpls = []
    for tpl in lst:
        if tpl[1] > max * 0.5 and tpl[0] not in other_winners['name'] + other_winners['title'] and tpl[0] in names_set:
            # print("returning from find_name: " + tpl[0])
            return tpl[0]
        elif tpl[1] < max * 0.5:
            break
        tpls.append(tpl)
    print("\n\n\nCould not find name for award: " + award)
    print(tpls)
    return lst[0][0]

# def find_name_without_db(lst, other_winners):
#     dct = {}
#     for tpl in lst:
#         dct[tpl[0]] = len(tpl[0].split(' '))
    
#     for key in dct:



def find_title(lst, other_winners, award):
    titles_set = load_imdb_data('title')
    max = lst[0][1]
    tpls = []
    for tpl in lst:
        tpls.append(tpl)
        # if tpl[0] == 'jessica chastain':
        #     print(tpl[0].title() in names_set)
        if tpl[1] > max * 0.5 and tpl[0] not in other_winners['name'] and tpl[0] in titles_set:
            # print("returning from find_title: " + tpl[0])
            return tpl[0]
        elif tpl[1] < max * 0.5:
            break
        tpls.append(tpl)
    print("\n\n\nCould not find title for award: " + award)
    print(tpls)
    return lst[0][0]