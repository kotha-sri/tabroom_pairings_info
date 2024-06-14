import requests
import pandas
from bs4 import BeautifulSoup


def html_table_to_df(page, entries=False):

    html = requests.get(page).text
    data = []
    list_header = []
    soup = BeautifulSoup(html, 'html.parser')

    # getting the header html and adding it to the array
    header = soup.find_all("table")[0].find("tr")
    for items in header:
        try:
            list_header.append(items.get_text().strip())
        except:
            continue

    # getting the rest of the rows and adding them to the array
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

    # for index in range(0, len(HTML_data), 2):
    #     element = HTML_data[index]
    #     print("-"*100)
    #     print(element.prettify())
    #     sub_data = []
    #     for sub_element in element:
    #         try:
    #             sub_data.append(sub_element.get_text().strip())
    #         except:
    #             continue

    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text().strip())
            except:
                continue

        # if this page is a page with entries, then get the link to the results of each team and add it under 'record'

        # add this in get_pairings after finidng the row with team name
        # if entries:
        #     record = "tabroom.com" + element.find('a')['href']
        #     # len(sub_data)-2 instead of -1 because of the extra empty columns in between
        #     sub_data[len(sub_data) - 2] = record
        data.append(sub_data)

    dataFrame = pandas.DataFrame(data=data, columns=list_header)


    # for empty_col in range(0, dataFrame.shape[1], 2):
    dataFrame.drop(dataFrame.columns[0], axis=1, inplace=True)

    return dataFrame
