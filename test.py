import requests
import json

make_code = 'AUDI'
model_code = 'S4'
firstRecord = 1


url_base = 'https://www.autotrader.com'
path = '/rest/searchresults/base'
url = url_base + path
session = requests.Session()
payload = {'makeCodeList': make_code,
            'searchRadius': '0',
            'listingTypes': 'USED',
            'modelCodeList': model_code,
            'zip': '90250',
            'startYear': '2010',
            'sortBy': 'distanceASC',
            'numRecords': '100',
            'firstRecord': firstRecord,
            }
headers= {'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"""}

print(f'Requesting {url}')

response = session.get(url, headers=headers, params=payload)

print(f'response: {response}')

results = response.json()

print(results)