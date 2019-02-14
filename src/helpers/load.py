import json
import requests
import configparser
import csv
import urllib
from urllib.parse import urlencode
import gzip
import shutil

def load_json(year, path='data/gg'):
    with open(path + year + '.json') as f:
        data = json.load(f)
    return data

valid_roles = {
    'actor', 'actress'
}

def load_imdb_data(d_type):
    return set(line.strip() for line in open(f'./data/{d_type}s.txt'))

def parse_imdb_data(d_type):
    min_birth = 1920
    min_title = 2010
    with open(f'./data/{d_type}.basics.tsv', 'r') as tsvin, open(f'./data/{d_type}s.txt', 'w') as type_out:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for i, row in enumerate(tsvin):
            if i % 10000 == 0:
                print(i)
            if d_type == 'name' and row[4].split(',')[0] in valid_roles and len(row[1].split(' ')) > 1 and row[2].isdigit() and not row[3].isdigit() and int(row[2]) > min_birth and len(row[5].split(',')) == 4:
                type_out.write(row[1]+'\n')
            elif d_type == 'title' and (row[1] == 'movie' or row[1] == 'tvseries') and ((row[5].isdigit() and int(row[5]) > min_title) or (row[6].isdigit() and int(row[6]) > min_title)):
                type_out.write(row[2]+'\n')

def request_imdb_data(d_type):
    try:
        urllib.request.urlretrieve(f"https://datasets.imdbws.com/{d_type}.basics.tsv.gz", f"./data/{d_type}.basics.tsv.gz")
        with gzip.open(f"./data/{d_type}.basics.tsv.gz", 'rb') as f_in:
            with open(f"./data/{d_type}.basics.tsv", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except:
        print("Could not get data from imdb. Please make sure you have a working internet connection.")


# TODO: implement load_movies and add file writing to parse movies 
def load_movies():
    raise Exception("not implemented yet")

def parse_movies(years,vote_min=100, score_min=6):

    config = configparser.ConfigParser()
    config.read('./config.ini')

    tmdb_url = "https://api.themoviedb.org/"
    tmdb_method = "3/discover/"

    for year in years:
        params = {
            "sort_by": "vote_average.desc",
            "with_original_language": "en",
            "primary_release_year": str(year-1),
            "vote_count.gte": str(vote_min),
            "vote_average.gte": str(score_min),
            "api_key": config['api_keys']['tmdb'],
            "page": "1"
        }
        data = requests.get(f"{tmdb_url}{tmdb_method}movie?{urlencode(params)}").json()
        pages = int(data['total_pages'])
        movies = parse_tmdb(data, 'title')
        for i in range(2, pages+1):
            params['page'] = str(i)
            movies += parse_tmdb(requests.get(f"{tmdb_url}{tmdb_method}movie?{urlencode(params)}").json(), 'title')

    return movies
    

def parse_tmdb(data, field):
    lst = []
    results = data['results']
    for result in results:
        lst.append(result[field])
    return lst