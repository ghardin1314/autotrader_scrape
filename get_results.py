# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:50:22 2019

@author: Garrett
"""


import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

url_base = 'https://www.autotrader.com'
# path = '/rest/searchform/advanced/'
path = '/rest/searchresults/base'
url = url_base + path
session = requests.Session()
payload = {'makeCodeList': 'FORD',
        'modelCodeList': 'MUST',
        'maxMileage': '0',
        'searchRadius': '0',
        'zip': '90250',
        'marketExtension': 'true',
        'sortBy': 'distanceASC',
        'numRecords': '100',
        'firstRecord': '901'}
headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
response = session.get(url, headers=headers, params = payload)
results = response.json()