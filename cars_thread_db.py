# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 10:45:44 2019

@author: Garrett
"""


import requests
import os
from config import db
from Models import Make, Xodel, Trim
import sqlite3 as lite
import threading
import concurrent.futures
import time

"""
This file creates .json files to populate autoscrape database 
for options to pick from.

Sleep in the get_trims method is to avoid api limiting. Takes a long time to run.
"""


class result_obj:
    def __init__(self):
        self.value = []
        self._lock = threading.Lock()

    def get_makes(self):
        url_base = 'https://www.autotrader.com'
        path = '/rest/searchform/advanced/update'
        url = url_base + path
        headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        payload = {'maxMileage': '0',
                       'searchRadius': '0',
                       'zip': '90250'}
        response = requests.get(url, headers=headers, params = payload)
        try:
            results = response.json()
            makes = results['searchFormFields']['make']['searchOptions'][0]['options']
            del makes[0]
            with self._lock:
                self.value = makes
        except:
            print('error on makes')
            exit()


    def get_models(self, make, make_index):
        url_base = 'https://www.autotrader.com'
        path = '/rest/searchform/advanced/update'
        url = url_base + path
        headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        payload = {'makeCodeList': make,
                       'maxMileage': '0',
                       'searchRadius': '0',
                       'zip': '90250'}
        response = requests.get(url, headers=headers, params = payload)
        try:
            results = response.json()
            models = results['searchFormFields']['model']['searchOptions'][0]['options']
            del models[0]
            with self._lock:
                make = self.value[make_index]
                make['models'] = models
                self.value[make_index] = make
        except:
            print(f'error on {make["name"]}')

    def get_trims(self, make, model, make_index, model_index):
        url_base = 'https://www.autotrader.com'
        path = '/rest/searchform/advanced/update'
        url = url_base + path
        headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        payload = {'makeCodeList': make,
                       'modelCodeList': model,
                       'maxMileage': '0',
                       'searchRadius': '0',
                       'zip': '90250'}

        time.sleep(10)
                    
        response = requests.get(url, headers=headers, params = payload)
        results = response.json()
        trims = results['searchFormFields']['trim']['searchOptions'][0]['options']
        del trims[0]
        with self._lock:
            model = self.value[make_index]['models'][model_index]
            print(f'getting trims for {model}')
            try:
                model['trims'] = trims
            except:
                model['trims'] = []
                print(f"error on {model['value']}")
            print(model['trims'])
            self.value[make_index]['models'][model_index] = model

def pull_data(results):

    results.get_makes()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        for make_index, make in enumerate(results.value):

            executor.submit(results.get_models, make['value'], make_index)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        for make_index, make in enumerate(results.value):

            models = make['models']

            for model_index, model in enumerate(models):

                executor.submit(results.get_trims, make['value'], model['value'], make_index, model_index)


if __name__ == '__main__':

    # breakpoint()

    #initialize new result object instance

    test = result_obj()

    pull_data(test)
    
    makes = test.value
    
    #write this to database. Done after aquiring data for database dependency

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
    



