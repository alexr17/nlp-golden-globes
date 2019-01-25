import json

def load_json(year):
    with open('./data/gg'+year+'.json') as f:
        data = json.load(f)
    return data