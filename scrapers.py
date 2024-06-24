from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json


# some functions to make the code more readable
def clean_html(html_text):
    return html_text.strip().replace('\n', ' ').replace('\t', '').replace('1111111 ', '')

def link_split(link, split):
    return link.split(split)[1]


def sQUARE(x=5):
    return x * x
    
# converts a html table (from a link) to a python dictionary
# different parameters are for the different types of tables on the Tabroom.com site

# TODO: find out how tabroom pairings look like in the future tab (where upcoming tournaments are shown)
#       and modify the function to work for that table
def html_table_to_dict_list(page, stop=None, pairings=False, hrefed=False, headless_webdriver=False, html=False):
    table_list = []

    # the pages that have links in tables
    HREFED = ['Record', 'Paradigm', 'Tournament Name']

    # requests only gets the initial site, before any JS loading
    # selenium webdriver gets it after by using a headless Chrome browser
    if headless_webdriver:
        headless = webdriver.ChromeOptions()
        headless.add_argument('--headless')
        driver = webdriver.Chrome(options=headless)
        driver.get(page)
        page_html = driver.page_source
        driver.quit()
    else:
        if html:
            page_html = page
        else:
            page_html = requests.get(page).text

    soup = BeautifulSoup(page_html, 'html.parser').find('table')

    # TODO: base_dict isn't needed since the only the order of the header needs to be saved, so instead save everything
    #   in order to the dict_order list
    base_dict = {}
    empty_counter = 0
    for th in soup.find('thead').find_all('th'):
        th_text = clean_html(th.get_text())

        if th_text == '':

            if pairings:
                if empty_counter == 0:
                    base_dict['Team 1'] = None
                    empty_counter += 1
                base_dict['Team 2'] = None
                continue

            empty_counter += 1
            base_dict[f'Blank #{empty_counter}'] = None

        base_dict[th_text] = None

    dict_order = []
    for key in base_dict.keys():
        dict_order.append(key)
    for tr in soup.find_all('tr')[1:]:
        append_dict = base_dict.copy()

        key_counter = 0
        for td in tr.find_all('td'):
            # normally a link embedded in the table will come as an empty string (as the link is in the HTML tag),
            # making it so that it is instead the link itself in the dictionary
            if hrefed and (dict_order[key_counter] in HREFED):
                a = td.find('a')
                if a is not None:
                    href = a.get('href')

                    if dict_order[key_counter] == 'Tournament Name':
                        append_dict['Tournament Name'] = clean_html(td.get_text())
                        append_dict['Tournament Link'] = "https://www.tabroom.com/" + href
                    else:
                        append_dict[dict_order[key_counter]] = "https://www.tabroom.com/" + href
                    key_counter += 1
                    continue
                    
            append_dict[dict_order[key_counter]] = clean_html(td.get_text())
            key_counter += 1

        if stop is not None:
            for value in append_dict.values():
                # likely will remove stop after the JSON info file is created, as we want to load all the data the first
                # time around
                if value == stop:
                    return [append_dict]

        table_list.append(append_dict)

    return table_list


def get_tourn_id(tourn_name):
    url = f"https://www.tabroom.com/index/search.mhtml?search=${tourn_name}&caller=%2Findex%2Findex.mhtml"
    tourn_link = str(html_table_to_dict_list(page=url, hrefed=True, stop=tourn_name)[0]['Tournament Link'])
    tourn_id = link_split(tourn_link, 'tourn_id=')
    return tourn_id

def get_event_id(event_name, tourn_id):
    events_tab_link = "https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id="+tourn_id
    events_tab_html = requests.get(events_tab_link).text
    soup = BeautifulSoup(events_tab_html, 'html.parser')
    events = soup.find('div', {'class': 'sidenote'})
    with open('constants.json', 'r') as constants:
        event_names = json.loads(constants.read())['entries_and_categories'][event_name]
    for a in events.find_all('a'):
        a_name = clean_html(a.get_text())
        for name in event_names:
            if a_name == name:
                event_id = link_split(a.get('href'), 'event_id=')
                return event_id

def get_category_id(category_name, tourn_id):
    category_tab_link = "https://www.tabroom.com/index/tourn/judges.mhtml?tourn_id="+tourn_id
    category_tab_html = requests.get(category_tab_link).text
    soup = BeautifulSoup(category_tab_html, 'html.parser')
    categories = soup.find('div', {'class': 'sidenote'})
    for div in categories.find_all('div', {'class': 'odd nospace'}):
        span_category_name = clean_html(div.find('span', {'class': 'third semibold bluetext'}).get_text())
        with open('constants.json', 'r') as consts:
            for name in json.loads(consts.read())['entries_and_categories'][category_name]:
                if span_category_name == name:
                    judges_link = div.find('a', {'class': 'blue full centeralign padno padvertless'}).get('href')
                    category_id = link_split(judges_link, 'category_id=').split('&tourn_id=')[0]
                    return category_id

def get_paradigm_text(judge_page):
        paradigm_html = requests.get(judge_page).text
        paradigm_soup = BeautifulSoup(paradigm_html, 'html.parser')
        paradigm_div = paradigm_soup.find('div', {'class': 'paradigm ltborderbottom'})
        paradigm_content = paradigm_div.find_all('p')
        for paragraph in range(len(paradigm_content)):
            paradigm_content[paragraph] = paradigm_content[paragraph].get_text()
        return paradigm_content
