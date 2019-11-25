# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 18:05:01 2019

@author: Garrett
"""


import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

url_base = 'https://www.autotrader.com'
path = '/rest/searchform/advanced/update'
url = url_base + path
payload = {}
# payload = {'makeCodeList': 'AUDI',
            # 'modelCodeList': 'A3'}
headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
response = requests.get(url, headers=headers, params = payload)
results = response.json()

makes = results['searchFormFields']['make']['searchOptions'][0]['options']
# makes = pd.DataFrame(makes)
# makes['models'] = [0] * len(makes['value'])
del makes[0]

res = {}


for make in makes:
    some_res = {}
    # breakpoint()
    payload = {'makeCodeList': make['value']}
    response = requests.get(url, headers=headers, params = payload)
    try:
        results = response.json()
    except:
        print(f"error on {make['name']}")
        continue

    models = results['searchFormFields']['model']['searchOptions'][0]['options']
    del models[0]
    # model = pd.DataFrame(model)
    # makes['models'][i] = model
    # res[make['name']] = models

    for model in models:
        # breakpoint()
        payload = {'makeCodeList': make['value'],
                   'modelCodeList': model['value'],
                   'maxMileage': '0',
                   'searchRadius': '0',
                   'zip': '90250'}
        # sleep(1)
        response = requests.get(url, headers=headers, params = payload)
        try:
            results = response.json()
        except:
            print(f"error on {model['name']}")
            # print(response.header)
            print(response.status_code)
            # breakpoint()
            continue

        trims = results['searchFormFields']['trim']['searchOptions'][0]['options']
        del trims[0]
        try:
            # trims = pd.DataFrame(trims)
            # trims = trims['name']
            some_res[model['name']] = trims
        except:
            some_res[model['name']] = []

    # breakpoint()
    res[make['name']] = some_res







# html = response.text

# soup = BeautifulSoup(html, "html.parser")

# makeResults = soup.find('select', attrs={'name': 'makeCode'})

# makeResults = makeResults.findAll('option')

# makes = []

# for make in makeResults:

#     makes.append(make.text)


# car = makes[2]
# session = requests.Session()
# url = 'https://www.autotrader.com'
# path = '/rest/searchform/advanced'
# url = url+path
# payload = {'makeCodeList': 'AUDI',
#            'modelCodeList': 'A3'}
# headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
# response = session.get(url, headers=headers, params = payload)
# results = response.json()
# soup = BeautifulSoup(response.text, "html.parser").text
# # modelResults = soup.find('select', attrs={'name': 'ModelCode'}).text