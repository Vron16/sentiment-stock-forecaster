import json
from pprint import  pprint
import requests

url = ('https://newsapi.org/v2/everything?'
       'q=Google&'
       'from=2019-03-14&'
       'sortBy=popularity&'
       'apiKey=22d271b54d1845858fbddf96cb9d20d2')

response = requests.get(url)

with open('googletest.json', 'w') as outfile:
       json.dump(response.json(), outfile)


#print (response.json)