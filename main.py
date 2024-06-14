from helpers import *

# constantststststststst
tourn_dict = get_current_tournament()

tourn_name = tourn_dict['name']
event_name = tourn_dict['event']


tourn_id = tourn_dict['tourn_id']
event_id = tourn_dict['event_id']
category_id = tourn_dict['category_id']
# except:
#     tourn_id = get_tourn_id(tourn_name)
#     event_id = get_event_id(event_name, tourn_id)
#     category_id = get_category_id(event_name, tourn_id)
#     with open('tournaments.json', 'r') as tourn:
#         tourn = json.loads(tourn.read())
#         tourn[tourn_name]['tourn_id'] = tourn_id
#         tourn[tourn_name]['event_id'] = event_id
#         tourn[tourn_name]['category_id'] = category_id



with open('tournaments.json', 'r') as file:
    team_code = json.loads(file.read())[tourn_name]['team_code']

# temp for now
# pairings_page_r2 = 'https://www.tabroom.com/index/tourn/postings/round.mhtml?tourn_id=27834&round_id=1029697'
# pairings_page_final = 'https://www.tabroom.com/index/tourn/postings/round.mhtml?tourn_id=27834&round_id=1054146'

# need to update html_table_to_dict_list so that using requests works
pairings_page = f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={tourn_id}&event_id={event_id}'
# print(pairings_page.text)

pairing = html_table_to_dict_list(pairings_page, stop=team_code, pairings=True, headless_webdriver=True)[0]

opponent = ''

if pairing['Team 1'] == team_code:
    opponent = pairing['Team 2']
else:
    opponent = pairing['Team 1']

try:
    flight = pairing['Flt']
except:
    flight = None

room = pairing['Room']

try:
    judge_name = [pairing['Judge']]
except:
    judge_name = []
    for key in pairing.keys():
        if key.split(' ')[0] == 'Judge':
            judge_name.append(pairing[key])

if not is_loaded('tournament_entries.json', tourn_name):
    print(tourn_name, event_name)
    load_entries(tourn_name, event_name)

with open('tournament_entries.json', 'r') as file:
    opponent_page = json.loads(file.read())[tourn_name][opponent]['Record']
    opponent_record = html_table_to_dict_list(page=opponent_page, stop=opponent, headless_webdriver=True)

# opponent_record_r2 = [{'Comparison': 'Open', 'Prelim Rds': '33.3% (1/3)', 'Prelim Ballots': '50.0% (1/2)', 'Elim Rds': '0% (0/0)', 'Elim Ballots': '0% (0/0)', 'Total': '33.3% (1/3)'}, {'Comparison': 'Totals', 'Prelim Rds': '33.3% (1/3)', 'Prelim Ballots': '50.0% (1/2)', 'Elim Rds': '0% (0/0)', 'Elim Ballots': '0% (0/0)', 'Total': '33.3% (1/3)'}]

if not is_loaded('tournament_judges.json', tourn_name):
    load_paradigms(tourn_name, event_name)

with open('tournament_judges.json', 'r') as file:
    judge_paradigms = []
    json_loaded = json.loads(file.read())[tourn_name]
    for judge in judge_name:
        judge_paradigms.append(get_paradigm_text(json_loaded[judge]['Paradigm']))

# format all the information nicely and idk what to do with it after that

format_pairing(room, flight, opponent, opponent_record, judge_name, judge_paradigms)

# reset_json_files()