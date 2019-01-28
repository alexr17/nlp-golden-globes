import json
import requests
import configparser
from urllib.parse import urlencode

def load_json(year):
    with open('./data/gg'+year+'.json') as f:
        data = json.load(f)
    return data


# movie database stuff
# api keys
config = configparser.ConfigParser()
config.read('./config.ini')

tmdb_url = "https://api.themoviedb.org/"
tmdb_method = "3/discover/"

def get_movies(year, vote_min=100, score_min=6):
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
    #print(f"{tmdb_url}{tmdb_method}movie?{urlencode(params)}")
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

#print(get_movies(2013))