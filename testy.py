from helpers import *
from scrapers import *


key = 'Judges   Results/Comments'
value = 'P  George, Emily    L'

value_list = re.split(' /*', value)
result = None
first_name = None
last_name = None

for thing in value_list:
    if thing == '' or thing == 'P':
        continue
    if thing in ('W', 'L'):
        result = thing

    first_name = re.find
