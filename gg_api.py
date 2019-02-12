import json
from src.queries.host import find_hosts
from src.queries.award_names import find_awards
from src.queries.nominees import find_nominee
from src.queries.winners import find_winner
from src.helpers.load import load_json, load_names
from src.helpers.debug import top_keys, find_key
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

    return find_hosts(data[year])


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return []


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
        nominees_obj[award] = find_winner(data[year], award)
    return nominees_obj


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    OFFICIAL_AWARDS = []
    if year in ['2013', '2015']:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
    else:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819
    
    winners_obj = {}
    for award in OFFICIAL_AWARDS:
        # if any(name in award for name in ['award', 'actress', 'actor', 'director']):
        winners_obj[award] = find_winner(data[year], award)

    # print(json.dumps(winners_obj, indent=4))
    return winners_obj


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
        presenters_obj[award] = '' # find_presenters(data[year], award)
    return presenters_obj


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    data['2015'] = load_json('2015')
    data['2013'] = load_json('2013')
    return False


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    pre_ceremony()
    #print(get_hosts('2013'))
    #print(get_hosts('2015'))
    # get_winner('2013')
    return False


if __name__ == '__main__':
    main()
