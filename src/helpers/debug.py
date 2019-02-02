# debug output
def top_keys(lst, min):
    for item in lst:
        if item[1] > min:
            print(item)

def find_key(lst, key):
    for item in lst:
        if key in item[0]:
            print(item)

def show_best(lst,min):
    awards = [x for i, x in enumerate(lst) if lst[i][0].split(" ")[0] == "best"]
    top_keys(awards, min)