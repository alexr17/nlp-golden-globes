import json
from src.queries.humor import find_jokes
import re
import nltk
from src.queries.host import find_hosts
from src.queries.award_names import find_awards
from src.queries.nominees import find_nominee, eval_nominee_tweet, generate_nominees_sw
from src.queries.winners import find_winner, eval_winner_tweet, generate_winners_sw
from src.queries.presenters import find_presenter, eval_presenter_tweet, generate_presenters_sw
from src.helpers.load import load_json, generate_tmdb_data
from src.helpers.clean import join_ngrams, valid_tkn
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
    return load_json(year, 'results/')['nominees']

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

def g_map(lst):
    tech_movie_awards = {'director', 'song', 'cinematography', 'screenplay', 'editing', 'score'}
    
    map = {
        'include': {},
        'exclude': {}
    }
    for e in lst:
        if e in tech_movie_awards:
            return {
                'include': {e: []},
                'exclude': {}
            }

        # actor keywords
        if e == 'actress':
            map['include'][e] = ['actriz']
        elif e == 'television' or e == 'series':
            map['include']['television'] = ['series', 'tv']
        elif e == 'motion' or e == 'picture':
            map['include']['motion'] = ['picture', 'movie']
        elif e == 'miniseries':
            map['include'][e] = ['mini-series', 'mini']
        elif e == 'comedy' or e == 'musical':
            map['include']['comedy'] = ['musical']
        else:
            map['include'][e] = []

    # if map generated for best actor and not supporting actor, then exclude supporting from search
    if 'supporting' not in map['include'] and any(word in map['include'] for word in ['actress', 'actor']):
        map['exclude']['supporting'] = []

    # if non-actor award, exclude actor/actress from results
    if not any(word in map['include'] for word in ['actress', 'actor']):
        map['exclude']['actress'] = ['actriz', 'actor']
    else:
        if 'miniseries' in map['include'] and 'supporting' in map['include']:
            del map['include']['television']
            del map['include']['motion']
            map['include']['miniseries'] += ['series', 'television film', 'tv film', 'tv movie', 'tv', 'television', 'television movie']
    return map

def generate_awards_map(awards):
    award_sw = {"best", "award", "performance", 'made', 'role', 'any', '-', 'limited'}
    awards_map = {}
    for award in awards:
        award_lst = [tkn for tkn in re.sub('[^a-zA-Z. ]', '', award).split(' ') if valid_tkn(tkn, [], award_sw)]
        awards_map[award] = g_map(award_lst)
    return awards_map

def tweet_corresponds_to_award(tweet, award_map):
    for award_key in award_map['include']:
        # if not then check if the child keys are

        if not any(rel_key in tweet for rel_key in ([award_key] + award_map['include'][award_key])):
            
            # did not pass test
            return False

    for award_key in award_map['exclude']:
         
        if any(rel_key in tweet for rel_key in ([award_key] + award_map['exclude'][award_key])):

            return False
    return True

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    # load data
    print("Loading data from text files")
    data = {}
    try:
        data['2019'] = load_json('2019')
        data['2018'] = load_json('2018')
    except FileNotFoundError as e:
        print("2018 and 2019 files not found. Please ^C and add them to the directory and run main again")
        # raise FileNotFoundError('\nIt looks like you haven\'t put the data for 2018 and 2019 into the /data/ directory.\n\nPlease do so the code can run properly.')
    data['2013'] = load_json('2013')
    data['2015'] = load_json('2015')
    print("Data loaded")

    lst = find_awards(data['2013'])

    debug = {}#{'aziz ansari', 'jason bateman'}
    # 2013/2015
    winners_sw = generate_winners_sw(OFFICIAL_AWARDS_1315)
    presenters_sw = generate_presenters_sw(OFFICIAL_AWARDS_1315)
    nominees_sw = generate_nominees_sw(OFFICIAL_AWARDS_1315)
    
    awards_map = generate_awards_map(OFFICIAL_AWARDS_1315)
    # lst = find_awards(data['2013'])
    results = {}
    t = time.time()
    for year in data:
        print("Now parsing data for " + year)
        nominated_dict = {}
        results[year] = load_json(year, 'results/')

        # hosts
        results[year]['host'] = results[year]['host'] or find_hosts(data[year])

        # winners
        results[year]['winners'] = results[year]['winners'] or {}
        winner_dicts = {}

        results[year]['nominees'] = results[year]['nominees'] or {}
        nominee_dicts = {}

        results[year]['presenters'] = results[year]['presenters'] or {}
        presenter_dicts = {}

        # set the empty dicts
        for award in awards_map:
            winner_dicts[award] = {}
            presenter_dicts[award] = {}
            nominee_dicts[award] = {}

        # iterate through each tweet
        for obj in data[year]:
            tweet = obj['text'].lower()
            if any(word in tweet for word in debug):
                print(tweet)
            
            # list of award dicts that WE WANT to add the tweet to
            valid_award_keys = {
                'winner': [],
                'presenter': [],
                'nominee': []
            }
            for award in awards_map:

                if tweet_corresponds_to_award(tweet, awards_map[award]):
                    valid_award_keys['winner'].append(award)
                    if any(word in tweet for word in {'present', 'introduc', 'award best', 'awarded best'}):
                        valid_award_keys['presenter'].append(award)
                    if any(word in tweet for word in {'nomin', 'nom\'d', 'lost', 'not win', 'should have won'}):
                        valid_award_keys['nominee'].append(award)
                        # if (award in {'best performance by an actress in a television series - drama', 'best performance by an actor in a supporting role in a motion picture'}):
                        #     print(tweet)

            if len(valid_award_keys['winner']):
                eval_winner_tweet(tweet, winner_dicts, valid_award_keys['winner'], winners_sw, awards_map)

            if len(valid_award_keys['nominee']):
                eval_winner_tweet(tweet, nominee_dicts, valid_award_keys['nominee'], nominees_sw, awards_map)

            if len(valid_award_keys['presenter']):
                eval_presenter_tweet(tweet, presenter_dicts, valid_award_keys['presenter'], presenters_sw)
        
        other_winners = {'name': set(), 'title': set()}
        print("\n\nFinding Awards")
        for award in awards_map:
            results[year]['winners'][award] = find_winner(winner_dicts[award], award, other_winners)

        other_presenters = set()
        print("\n\nFinding Presenters")
        for award in awards_map:
            results[year]['presenters'][award] = find_presenter(presenter_dicts[award], award, other_presenters, results[year]['winners'][award])

        other_nominees = {'name': set(), 'title': set()}
        print("\n\nFinding Nominees")
        for award in awards_map:
            # print(nominees_map[award])
            other_set = [results[year]['winners'][award]]
            other_set += results[year]['presenters'][award]
            results[year]['nominees'][award] = find_nominee(nominee_dicts[award], award, other_nominees, set(other_set))
       

        # AWARD NAMES
        lst = find_awards(data[year])
        results['award_names'] = lst

       # write results to file
        with open('results/' + year +'.json', 'w') as outfile:
            outfile.write(json.dumps(results[year], indent=4))

        #PRINTING STUFF
        print(f"The Host(s) of the {year} Golden Globes were: {', '.join(results[year]['host'])}")

        for award in awards_map:
            print(f"\nAward: {award}\nPresenters {', '.join(results[year]['presenters'][award])}\nNominees: {', '.join(results[year]['nominees'][award])}\nWinner: {(results[year]['winners'][award])}")

        # RED CARPET
        dress_dict = top_dressed(find_best_dressed(data[year]), find_worst_dressed(data[year]))
        print(f"The best dressed at the {year} Golden Globes were: " + ', '.join(dress_dict['best_dressed']))
        print(f"The worst dressed were: " + ', '.join(dress_dict['worst_dressed']))
        print(f"The most controversially dressed were: " + ', '.join(dress_dict['polarized_dressed']))

        # JOKES
        jokes_dict = find_jokes(data[year])

        print(f"Done with {year} Golden Globes\n\n")
    print(str(time.time() - t))
    return False



if __name__ == '__main__':
    main()
