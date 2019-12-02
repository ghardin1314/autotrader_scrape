# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 14:59:35 2019

@author: Garrett
"""


import requests
import os
from config import db
from Models import Make, Xodel, Trim
import sqlite3 as lite

url_base = 'https://www.autotrader.com'
path = '/rest/searchform/advanced/update'
url = url_base + path
payload = {}
headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
response = requests.get(url, headers=headers, params = payload)
results = response.json()

makes = results['searchFormFields']['make']['searchOptions'][0]['options']

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

    for model in models:

        payload = {'makeCodeList': make['value'],
                   'modelCodeList': model['value'],
                   'maxMileage': '0',
                   'searchRadius': '0',
                   'zip': '90250'}
        response = requests.get(url, headers=headers, params = payload)
        try:
            results = response.json()
        except:
            print(f"error on {model['name']}")
            continue
        trims = results['searchFormFields']['trim']['searchOptions'][0]['options']
        del trims[0]
        try:
            model['trims'] = trims
        except:
            model['trims'] = []

    make['models'] = models

if os.path.exists("models.db"):
    os.remove('models.db')

db.create_all()

breakpoint()

for make in makes:

    # breakpoint()
    name = make.get('name')
    value = make.get('value')
    m = Make(make_name = name, make_value = value)

    for model in make.get('models'):
        ma = m.xodels
        xa = Xodel(xodel_name = model.get('name'), xodel_value = model.get('value'))
        ma.append(xa)

        for trim in model.get('trims'):
            tr = xa.trims
            tr.append(Trim(trim_name = trim.get('name'), trim_value = trim.get('value')))

    db.session.add(m)

db.session.commit()

conn = lite.connect('models.db')
cur = conn.cursor()

with conn:
    cur.execute("SELECT * FROM make")
    print(cur.fetchall())

    cur.execute("SELECT * FROM xodel")
    print(cur.fetchall())

    cur.execute("SELECT * FROM trim")
    print(cur.fetchall())

