# debug output
def top_keys(lst, min):
    for item in lst:
        if item[1] > min:
            print(item)

def find_key(lst, key):
    for item in lst:
        if key in lst:
            print(item)