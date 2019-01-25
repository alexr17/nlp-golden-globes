# debug output
def top_keys(lst, min, keys):
    for item in lst:
        if item[1] > min:
            print(item)