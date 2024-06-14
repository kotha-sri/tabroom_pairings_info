from datetime import date
from scrapers import *


def get_judge_full_name(judge_dict):
    full_name = ''

    if judge_dict['First'] != '' and judge_dict['First'] is not None:
        full_name += judge_dict['First'] + ' '
    try:
        if judge_dict['Middle'] is not None and judge_dict['Middle'] != '':
            full_name += judge_dict['Middle'] + ' '
    except:
        pass
    if judge_dict['Last'] != '' and judge_dict['Last'] is not None:
        full_name += judge_dict['Last'] + ' '
    return full_name.strip()

def load_entries(tourn_name, event_name):
    tourn_id = get_tourn_id(tourn_name)
    event_id = get_event_id(event_name, tourn_id)
    entries_page = f'https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id={tourn_id}&event_id={event_id}'
    entries = html_table_to_dict_list(page=entries_page, hrefed=True)

    entries_dump = {}

    for entry in entries:
        entries_dump[entry['Code']] = entry

    entries_dump = {tourn_name: entries_dump}

    entries_dump = json.dumps(entries_dump, indent=4)

    with open('tournament_entries.json', 'w') as entries_json:
        entries_json.write(entries_dump)

def load_paradigms(tourn_name, category_name):
    tourn_id = get_tourn_id(tourn_name)
    cat_id = get_category_id(category_name, tourn_id)

    paradigm_page = f'https://www.tabroom.com/index/tourn/judges.mhtml?category_id={cat_id}&tourn_id={tourn_id}'

    paradigms = html_table_to_dict_list(page=paradigm_page, hrefed=True)

    paradigm_dump = {}

    for para in paradigms:
        full_name = get_judge_full_name(para)
        paradigm_dump[full_name] = para

    paradigm_dump = {tourn_name: paradigm_dump}

    paradigm_dump = json.dumps(paradigm_dump, indent=4)

    with open('tournament_judges.json', 'w') as paras:
        paras.write(paradigm_dump)

def is_loaded(json_file, tourn_name):
    with open(json_file, 'r') as file:
        json_dict = json.loads(file.read())
        if tourn_name in json_dict.keys():
            return True
        else:
            return False

def get_current_tournament():
    with open('tournaments.json', 'r') as file:
        tourn_dict = json.loads(file.read())
        for key in tourn_dict.keys():
            if tourn_dict[key]['date'] == date.isoformat(date.today()):
                return tourn_dict
    return None

def record_as_table(record):
    header = "|"
    for key in record.keys():
        header += " " + key + " "*(16-len(key)) + "|" + " "
    content = "|"
    for value in record.values():
        content += " " + value + " "*(16-len(value)) + "|" + " "
    print(header)
    print(content)


def format_pairing(room, flight, opponent, opponent_record, judge, judge_paradigm):
    print()
    print(f"Room: {room}")
    print()
    print(f"Flight {flight}")
    print()
    print(f"{opponent}")
    record_as_table(opponent_record[0])
    print()
    for i in range(len(judge)):
        print(judge[i])
        for p in judge_paradigm[i]:
            print(p)
    print()

def reset_json_files():
    with open('tournament_entries.json', 'w') as entries, open('tournament_judges.json', 'w') as judges:
        entries.write('{}')
        judges.write('{}')

def get_pairings_page():
    pass