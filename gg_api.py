import json
from src.queries.humor import find_jokes
from src.queries.host import find_hosts
from src.queries.award_names import find_awards
from src.queries.nominees import find_nominee
from src.queries.winners import find_winner, eval_winner_tweet, generate_winners_map, winners_id_award, generate_winners_sw
from src.queries.presenters import find_presenter, eval_presenter_tweet, generate_presenters_map, presenters_id_award, generate_presenters_sw
from src.helpers.load import load_json, generate_tmdb_data
from src.helpers.clean import join_ngrams
from src.queries.red_carpet import find_best_dressed, find_worst_dressed, top_dressed
from src.helpers.debug import top_keys, find_key

import time
'''Version 0.1'''


OFFICIAL_AWARDS_1315 = [
    'cecil b. demille award',
    'best motion picture - drama',
    'best performance by an actress in a motion picture - drama',
    'best performance by an actor in a motion picture - drama',
    'best motion picture - comedy or musical',
    'best performance by an actress in a motion picture - comedy or musical',
    'best performance by an actor in a motion picture - comedy or musical',
    'best animated feature film',
    'best foreign language film',
    'best performance by an actress in a supporting role in a motion picture',
    'best performance by an actor in a supporting role in a motion picture',
    'best director - motion picture',
    'best screenplay - motion picture',
    'best original score - motion picture',
    'best original song - motion picture',
    'best television series - drama',
    'best performance by an actress in a television series - drama',
    'best performance by an actor in a television series - drama',
    'best television series - comedy or musical',
    'best performance by an actress in a television series - comedy or musical',
    'best performance by an actor in a television series - comedy or musical',
    'best mini-series or motion picture made for television',
    'best performance by an actress in a mini-series or motion picture made for television',
    'best performance by an actor in a mini-series or motion picture made for television',
    'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
    'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television'
]

OFFICIAL_AWARDS_1819 = [
    'best motion picture - drama',
    'best motion picture - musical or comedy',
    'best performance by an actress in a motion picture - drama',
    'best performance by an actor in a motion picture - drama',
    'best performance by an actress in a motion picture - musical or comedy',
    'best performance by an actor in a motion picture - musical or comedy',
    'best performance by an actress in a supporting role in any motion picture',
    'best performance by an actor in a supporting role in any motion picture',
    'best director - motion picture',
    'best screenplay - motion picture',
    'best motion picture - animated',
    'best motion picture - foreign language',
    'best original score - motion picture',
    'best original song - motion picture',
    'best television series - drama',
    'best television series - musical or comedy',
    'best television limited series or motion picture made for television',
    'best performance by an actress in a limited series or a motion picture made for television',
    'best performance by an actor in a limited series or a motion picture made for television',
    'best performance by an actress in a television series - drama',
    'best performance by an actor in a television series - drama',
    'best performance by an actress in a television series - musical or comedy',
    'best performance by an actor in a television series - musical or comedy',
    'best performance by an actress in a supporting role in a series, limited series or motion picture made for television',
    'best performance by an actor in a supporting role in a series, limited series or motion picture made for television',
    'cecil b. demille award'
]


#
# lst = find_worst_dressed(data, '2013')
# lst1 = find_best_dressed(data, '2013')
# print(top_dressed(lst1, lst))
# print('---------------')
# top_keys(lst1, 10)

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    return load_json(year, 'results/')['host']


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here

    return load_json(year, 'results/')['award_names']


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    OFFICIAL_AWARDS = []
    if year in ['2013', '2015']:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
    else:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819

    nominees_obj = {}
    for award in OFFICIAL_AWARDS:
         nominees_obj[award] = ''
    return nominees_obj


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return load_json(year, 'results/')['winners']


def get_presenters(year):
    '''Best, worst, and polarized dressed as a dictionary with at most 2
    people per category.Polarized dressed means they were mixed reviews on whether they were
    considered best or worst dressed
    '''
    # Your code here
    return load_json(year, 'results/')['presenters']

def get_redcarpet(year):
    '''
    Best, worst, and polarized dressed with at most 2 people per
    category. Polarized dressed means that there were obvious conflicting
    opinions on whether the person was best or worst dressed.
    '''
    # Your code here
    return load_json(year, 'results/')['presenters']


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    generate_tmdb_data([2010, 2019])
    return False

def generate_awards_map(awards):
    map = {}
    for award in awards:
        map[award] = {
            'person': any(word in award for word in ['actress', 'actor', 'director', 'award'])
        }
    return map


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    # load data
    try:
        data['2019'] = load_json('2019')
        data['2018'] = load_json('2018')
    except FileNotFoundError as e:
        print("File not found")
        # raise FileNotFoundError('\nIt looks like you haven\'t put the data for 2018 and 2019 into the /data/ directory.\n\nPlease do so the code can run properly.')
    data = {}
    data['2015'] = load_json('2015')
    data['2013'] = load_json('2013')

    lst = find_awards(data['2013'])

    debug = {'aziz ansari', 'jason bateman'}
    # 2013/2015
    winners_sw = generate_winners_sw(OFFICIAL_AWARDS_1315)
    presenters_sw = generate_presenters_sw(OFFICIAL_AWARDS_1315)
    winners_map = generate_winners_map(OFFICIAL_AWARDS_1315)
    presenters_map = generate_presenters_map(OFFICIAL_AWARDS_1315)
    awards_map = generate_awards_map(OFFICIAL_AWARDS_1315)
    results = {}
    times = {}

    for year in ['2013', '2015']:
        times[year] = {}
        times[year] = {
            'total': 0,
            'tweet_count': 0,
            'winners': {
                'id_award': 0,
                'eval_tweet': 0,
                'find': 0,
            },
            'presenters': {
                'id_award': 0,
                'eval_tweet': 0,
                'find': 0,
            }
        }
        t_total = time.time()
        # hosts
        results[year] = {'host': find_hosts(data[year])}

        # winners
        results[year]['winners'] = {}
        winner_dicts = {}

        results[year]['presenters'] = {}
        presenter_dicts = {}

        # set the empty dicts
        for award in awards_map:
            winner_dicts[award] = {}
            presenter_dicts[award] = {}

        # iterate through each tweet
        for obj in data[year]:
            times[year]['tweet_count'] += 1
            tweet = obj['text'].lower()
            # if any(word in tweet for word in debug):
            #     print(tweet)

            # list of award dicts that WE WANT to add the tweet to
            valid_award_keys = {
                'winner': [],
                'presenter': []
            }
            for award in awards_map:
                # if the tweet corresponds to an award, add its dict to the list
                t = time.time()
                if winners_id_award(tweet, winners_map[award]):
                    valid_award_keys['winner'].append(award)
                times[year]['winners']['id_award'] += (time.time() - t)

                t = time.time()
                if presenters_id_award(tweet, presenters_map[award]):
                    valid_award_keys['presenter'].append(award)
                times[year]['presenters']['id_award'] += (time.time() - t)

            t = time.time()
            if len(valid_award_keys['winner']):
                eval_winner_tweet(tweet, winner_dicts, valid_award_keys['winner'], winners_sw, awards_map)
            times[year]['winners']['eval_tweet'] += (time.time() - t)


            t = time.time()
            if len(valid_award_keys['presenter']):
                eval_presenter_tweet(tweet, presenter_dicts, valid_award_keys['presenter'], presenters_sw)
            times[year]['presenters']['eval_tweet'] += (time.time() - t)

        t = time.time()
        other_winners = {
            'name': set(),
            'title': set()
        }
        print("\n\n\nFinding Awards")

        other_winners = {
            'name': set(),
            'title': set()
        }
        for award in awards_map:
            results[year]['winners'][award] = find_winner(winner_dicts[award], award, other_winners)
        times[year]['winners']['find'] += (time.time() - t)


        t = time.time()
        other_presenters = set()
        print("\n\n\nFinding Presenters")
        for award in presenters_map:
            # print(presenters_map[award])
            results[year]['presenters'][award] = find_presenter(presenter_dicts[award], award, other_presenters, results[year]['winners'][award])
        times[year]['presenters']['find'] += (time.time() - t)


       # write results to file
        with open('results/' + year +'.json', 'w') as outfile:
            outfile.write(json.dumps(results[year], indent=4))

        times[year]['total'] += time.time() - t_total

    # printing time data
    print(json.dumps(times, indent=4))


    #pre_ceremony()
    #pre_ceremony(False)
    data = load_json('2013')
    lst = find_awards(data)
    # for l in lst:
    #     print(l)
    results2013 = load_json('2013', 'results/')
    results2013['award_names'] = lst
    with open('results/' + '2013' +'.json', 'w') as outfile:
        outfile.write(json.dumps(results2013, indent=4))

    data = load_json('2015')
    lst = find_awards(data)
    results2015 = load_json('2015', 'results/')
    results2015['award_names'] = lst
    with open('results/' + '2015' +'.json', 'w') as outfile:
        outfile.write(json.dumps(results2015, indent=4))
    #top_keys(lst, 100)
    #print(get_presenters('2013'))
    #print(get_hosts('2013'))
    #print(get_hosts('2015'))
    # get_winner('2013')
    return False



if __name__ == '__main__':
    main()
