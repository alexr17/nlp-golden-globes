# debug output
def top_keys(lst, min):
    for item in lst:
        if item[1] > min:
            print(item)