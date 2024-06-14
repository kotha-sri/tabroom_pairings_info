import requests
from bs4 import BeautifulSoup
from scrapers import *


def login(username, password):
    endpoint = 'https://www.tabroom.com/user/login/login_save.mhtml'
    payload = {'username': username, 'password': password}
    return requests.post(url=endpoint, data=payload)


def pairing_from_account_login():
    pass

# returns array of the paragraphs in the html
def get_judge_paradigm(judge_person_id, text=False):
    r = requests.get(f'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id={judge_person_id}')
    if text:
        pdigm = BeautifulSoup(r.text, 'html.parser')
        pdigm_div = pdigm.find('div', {'class': 'paradigm ltborderbottom'})
        pdigm_para = pdigm_div.find_all('p')
        content = []
        for p in pdigm_para:
            content.append(p.text)
        return content
    return r


def get_judge_id(first_name, last_name, middle_name=''):
    pass


URL = 'https://www.tabroom.com/index.mhtml'
payload = {
    'value': 262656
}

r = requests.post(URL, data=payload)
print(r.text)

x = get_judge_paradigm(12312, False) # "hello"
print(x) # print "hello"