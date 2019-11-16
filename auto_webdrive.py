# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:04:45 2019

@author: Garrett
"""


# import time
# import urllib
import requests
# from splinter import Browser
# from selenium import webdriver
# from datetime import date, timedelta, datetime
from datetime import datetime
from bs4 import BeautifulSoup
import math
import pandas as pd
import re
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np


def url2soup(url):

    response = requests.get(url, headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    return soup


if __name__ == '__main__':

    make = 'Toyota'

    model = 'Camry'

    trim = 'LE'

    makeUP = make.upper()

    modelUP = model.upper()

    year = datetime.now().year

    years = np.arange(year-5,year+3, 1)

    df = []

    for year in years:

        i = 0

        url = 'https://www.autotrader.com/cars-for-sale/{make}/{model}/Hawthorne+CA-90250?makeCodeList={makeUP}&searchRadius=0&modelCodeList={modelUP}&zip=90250&marketExtension=true&startYear={year}&endYear={year}&trimCodeList={modelUP}%7{trim}&&listingTypes=USED&sortBy=distanceASC&numRecords=100&firstRecord={i}'.format(make=make, model=model, makeUP = makeUP, modelUP = modelUP,year = year,trim = trim, i = i)
    
        # url = 'https://www.autotrader.com/cars-for-sale/Toyota/Camry/Hawthorne+CA-90250?makeCodeList=TOYOTA&searchRadius=0&modelCodeList=CAMRY&zip=90250&marketExtension=true&listingTypes=USED&sortBy=derivedpriceDESC&numRecords=100&firstRecord=0'
    
        soup = url2soup(url)

        try:
    
            numResults = soup.find('div', attrs={'class': 'results-text-container'}).text
    
            numResults = numResults[numResults.find('1-100 of ')+len('1-100 of '):numResults.rfind(' Results')]


            if numResults == '1,000+':
                numResults = '1000'
        
            numResults = int(numResults)
        
            numPages = math.floor(numResults/100)

        except:
            continue
    
        # df = pd.DataFrame(columns=['Name','Price', 'Miles'])

        for i in range(-1,numPages):
    
            # breakpoint()
    
            if i != 0:
    
                i=i*100+1
    
            # url = 'https://www.autotrader.com/cars-for-sale/Toyota/Camry/Hawthorne+CA-90250?makeCodeList=TOYOTA&searchRadius=0&modelCodeList=CAMRY&zip=90250&marketExtension=true&listingTypes=USED&sortBy=derivedpriceDESC&numRecords=100&firstRecord={i}'.format(i = i)
    
            url = 'https://www.autotrader.com/cars-for-sale/{make}/{model}/Hawthorne+CA-90250?makeCodeList={makeUP}&searchRadius=0&modelCodeList={modelUP}&zip=90250&marketExtension=true&startYear={year}&endYear={year}&trimCodeList={modelUP}%7{trim}&&listingTypes=USED&sortBy=distanceASC&numRecords=100&firstRecord={i}'.format(make=make, model=model, makeUP = makeUP, modelUP = modelUP,year = year,trim = trim, i = i)
    
            soup = url2soup(url)
    
            listings = soup.findAll('div', attrs={'data-cmp': 'inventoryListing'})
    
            for listing in listings:
    
                # breakpoint()
    
                year = listing.find('h2', attrs={'data-cmp': 'subheading'})
    
                price = listing.find('span', attrs={'class': 'first-price'})
    
                miles = listing.find('span', text=re.compile('miles'))
    
    
                try:
    
                    year = year.text
    
                    year = year[:year.rfind(' {}'.format(make))]
    
                    year = int(re.findall(r'\d+', year)[0])
    
                    price = int(price.text.replace(',',''))
    
                    miles = miles.text.replace(',','')
    
                    miles = int(miles[:miles.rfind(' miles')])
    
                    data =[year, price, miles]
    
                    print(data)
    
                    df.append(data)
    
                except:
                    print('error')
                    continue
    breakpoint()

    df = pd.DataFrame(df, columns=['Year','Price', 'Miles'])

    fig = plt.figure()
    ax = plt.axes(projection = '3d')
    ax.scatter3D(df['Year'],df['Miles'],df['Price'])

    ax.set_xlim(2014,max(df['Year']+1))
    ax.set_ylim(0,100000)
    ax.set_zlim(min(df['Price']-1000),40000)


    # con = urllib.urlopen(req)

    # html = con.read()

    # soup = BeautifulSoup(html)

    # path = {'executable_path': r'C:\Users\Garrett\Documents\chromedriver'}

    # Set some default behaviors

    # browser = Browser('chrome', **path, headless = False)

    # built_url = 'https://www.autotrader.com'

    # browser.visit(url)

    # browser.find_link_by_partial_text('Advanced Search').click()

    # breakpoint()

    # browser.find_by_name("makeCodeListPlaceHolder").first.type(make, slowly=True)

    # browser.find_by_name("modelCodeListPlaceHolder").first.type(model)

    # browser.find_by_id("search").click()

    # breakpoint()

    # browser.quit()

