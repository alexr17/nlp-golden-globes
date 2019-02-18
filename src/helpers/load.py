import json
import requests
import configparser
import csv
import urllib
from urllib.parse import urlencode
import gzip
import shutil
import time
import unidecode


def load_json(year, path='./gg'):
    with open(path + year + '.json') as f:
        data = json.load(f)
    return data

def load_imdb_data(d_type):
    return set(line.strip() for line in open(f'./data/{d_type}s.txt'))

def write_to_file(arr, file_name):
    with open(file_name, 'w') as f_in:
        for e in arr:
            f_in.write(e + '\n')

def parse_tmdb(data, field):
    lst = []
    results = data['results']
    for result in results:
        lst.append(unidecode.unidecode(result[field].lower()))
    return lst

def parse_tmdb_data(key, params, tmdb_method):
    tmdb_url = "https://api.themoviedb.org/"
    data = []
    # print(f"{tmdb_url}{tmdb_method}?{urlencode(params)}")
    resp = requests.get(f"{tmdb_url}{tmdb_method}?{urlencode(params)}").json()
    pages = int(resp['total_pages'])

    data += parse_tmdb(resp, key)
    for i in range(2, pages+1):
        params['page'] = str(i)
        time.sleep(0.25)
        data += parse_tmdb(requests.get(f"{tmdb_url}{tmdb_method}?{urlencode(params)}").json(), key)
        print(len(data))
    params['page'] = '1'
    return data

# Generating the tmdb data for a range of years
# NOTE: only run this if it hasn't been generated yet
def generate_tmdb_data(years, vote_min=100, score_min=6):
    print("Getting list of movies, tv shows, and famous people from TMDB")

    config = configparser.ConfigParser()
    config.read('./config.ini')

    # people
    tmdb_method = "3/person/popular"
    params = {
        "api_key": config['api_keys']['tmdb']
    }

    if len(list(line.strip() for line in open('./data/names.txt'))) < 18000:
        people = parse_tmdb_data('name', params, tmdb_method)
        write_to_file(people, './data/names.txt')
        print("Done loading people")

    if len(list(line.strip() for line in open('./data/titles.txt'))) < 1400:
        return

    titles = []
    params = {
        "with_original_language": "en",
        "vote_count.gte": str(vote_min),
        "vote_average.gte": str(score_min),
        "api_key": config['api_keys']['tmdb']
    }

    # movies
    tmdb_method = f"3/discover/movie"
    movie_years = range(years[0], years[1])
    for year in movie_years:
        # print(year)
        params["primary_release_year"] = str(year)
        titles += parse_tmdb_data('title', params, tmdb_method)

    # tv
    tmdb_method = f"3/discover/tv"
    tv_years = range(years[0]-5, years[1])
    for year in tv_years:
        print(year)
        params["first_air_date_year"] = str(year)
        titles += parse_tmdb_data('name', params, tmdb_method)

    write_to_file(titles, './data/titles.txt')


# IMDB -- not currently being used
def parse_imdb_data(d_type):
    valid_roles = {
        'actor', 'actress'
    }
    min_birth = 1920
    min_title = 2010
    with open(f'./data/{d_type}.basics.tsv', 'r') as tsvin, open(f'./data/{d_type}s.txt', 'w') as type_out:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for i, row in enumerate(tsvin):
            if i % 100000 == 0:
                print(str(i) + ' lines parsed')
            if d_type == 'name' and row[4].split(',')[0] in valid_roles and len(row[1].split(' ')) > 1 and row[2].isdigit() and not row[3].isdigit() and int(row[2]) > min_birth and len(row[5].split(',')) == 4:
                type_out.write(row[1].lower()+'\n')
            elif d_type == 'title' and (row[1] == 'movie' or row[1] == 'tvseries') and ((row[5].isdigit() and int(row[5]) > min_title) or (row[6].isdigit() and int(row[6]) > min_title)):
                type_out.write(row[2].lower()+'\n')

def request_imdb_data(d_type):
    try:
        urllib.request.urlretrieve(f"https://datasets.imdbws.com/{d_type}.basics.tsv.gz", f"./data/{d_type}.basics.tsv.gz")
        with gzip.open(f"./data/{d_type}.basics.tsv.gz", 'rb') as f_in:
            with open(f"./data/{d_type}.basics.tsv", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except:
        print("Could not get data from imdb. Please make sure you have a working internet connection.")
