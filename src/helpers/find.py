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