import json
from src.queries.host import find_hosts
from src.queries.award_names import find_awards
from src.queries.nominees import find_nominee
from src.queries.winners import find_winner, eval_winner_tweet, generate_awards_map, id_award, generate_winners_sw
from src.queries.presenters import find_presenter
from src.helpers.load import load_json, load_names
from src.helpers.clean import join_ngrams
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

data = {}


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
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    OFFICIAL_AWARDS = []
    if year in ['2013', '2015']:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
    else:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819

    presenters_obj = {}
    for award in OFFICIAL_AWARDS:
        presenters_obj[award] = ''#find_presenter(data[year], award)
    return presenters_obj


def pre_ceremony(raise_except=True):
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here

    # load data
    try:
        data['2019'] = load_json('2019')
        data['2018'] = load_json('2018')
    except FileNotFoundError as e:
        if raise_except:
            raise FileNotFoundError('\nIt looks like you haven\'t put the data for 2018 and 2019 into the /data/ directory.\n\nPlease do so the code can run properly.')
    data['2015'] = load_json('2015')
    data['2013'] = load_json('2013')
    times = {}
    results = {}

    # 2013/2015
    winners_sw = generate_winners_sw(OFFICIAL_AWARDS_1315)
    awards_map = generate_awards_map(OFFICIAL_AWARDS_1315)
    for year in ['2013', '2015']:
        times[year] = {}
        times[year]['host'] = {
            'total': 0,
            'count': 0
        }

        # hosts
        t = time.time()
        results[year] = {'host': find_hosts(data[year])}
        times[year]['host']['total'] += time.time() - t
        times[year]['host']['count'] += 1

        times[year]['winners'] = {
            'total': 0,
            'count': 0
        }

        # winners
        results[year]['winners'] = {}
        winner_dicts = {}

        # set the empty dicts
        for award in awards_map:
            winner_dicts[award] = {}

        # iterate through each tweet
        for obj in data[year]:
            tweet = obj['text'].lower()
            t = time.time()
            # list of award dicts that WE WANT to add the tweet to
            valid_award_keys = []
            for award in awards_map:
                # if all(word in obj['text'].lower() for word in ['actor', 'miniseries', 'tv', 'movie']):
                # if the tweet corresponds to an award, add its dict to the list
                if id_award(tweet, awards_map[award]):
                    valid_award_keys.append(award)

            # if we have valid award keys
            if len(valid_award_keys):
                eval_winner_tweet(obj['text'].lower(), winner_dicts, awards_map, valid_award_keys, winners_sw)

            times[year]['host']['total'] += time.time() - t
            times[year]['host']['count'] += 1

        for award in awards_map:
            results[year]['winners'][award] = find_winner(winner_dicts[award], award)

        # write results to file
        with open('results/' + year +'.json', 'w') as outfile:
            json.dump(results[year], outfile)

    print(json.dumps(times, indent=4))
    return False


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here



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
