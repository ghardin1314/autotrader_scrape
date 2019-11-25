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
from sklearn.preprocessing import scale
import matplotlib.tri as mtri


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

    years = np.arange(year-5,year+2, 1)
    # years = [2015]

    df = []

    df_filtered = []

    df_surface = []

    for year in years:

        df_test = []

        df_unfiltered = []

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

        for i in range(0,numPages+1):
    
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
    
                    df_unfiltered.append(data)
    
                except:
                    print('error')
                    continue

        df_unfiltered = np.array(df_unfiltered)

        df_test = scale(df_unfiltered, axis=0, with_mean = True, with_std = True)

        z_test = np.sqrt(df_test[:,1]**2+df_test[:,2]**2)

        del_indexs = [n for n,i in enumerate(z_test) if i>1]

        df_fil = df_unfiltered

        for i in sorted(del_indexs, reverse=True):
            df_fil = np.delete(df_fil, np.s_[i],axis = 0)

        # breakpoint()

        df.append(df_unfiltered)

        df_filtered.append(df_fil)

        # breakpoint()

        p = np.polyfit(df_unfiltered[:,2],df_unfiltered[:,1], 2)
        z = np.poly1d(p)
        
        reg_miles = np.linspace(min(df_unfiltered[:,2]), max(df_unfiltered[:,2]), 100)
        reg_price = z(reg_miles)
        
        df_surface.append(np.transpose([[year]*len(reg_miles), reg_price, reg_miles]))


    # breakpoint()

    df = np.vstack(df)
    df_filtered = np.vstack(df_filtered)
    df_surface = np.vstack(df_surface)

    # breakpoint()

    df = pd.DataFrame(df, columns=['Year','Price', 'Miles'])
    df_filtered = pd.DataFrame(df_filtered, columns=['Year','Price', 'Miles'])
    df_surface = pd.DataFrame(df_surface, columns=['Year','Price', 'Miles'])

    df.to_csv(r'unfiltered_test.csv', index = False)
    df_filtered.to_csv(r'filtered_test.csv', index = False)
    df_surface.to_csv(r'surface_test.csv', index = False)

    triang = mtri.Triangulation(df_filtered['Year'], df_filtered['Miles'])
    triang2 = mtri.Triangulation(df_filtered['Year'], df_filtered['Miles'])
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    
    # ax.triplot(triang, c="#D3D3D3", marker='.', markerfacecolor="#DC143C", markeredgecolor="black", markersize=10)
    
    # ax.set_xlabel('Year')
    # ax.set_ylabel('Miles')
    # plt.show()

    # x = pd.series.tolist(df_filtered['Year'])
    # y = pd.series.tolist(df_filtered['Miles'])

    # def apply_mask(triang, alpha=1.5):

    #     breakpoint()
    #     # Mask triangles with sidelength bigger some alpha
    #     triangles = triang.triangles
    #     # Mask off unwanted triangles.
    #     xtri = x[triangles] - np.roll(x[triangles], 1, axis=1)
    #     ytri = y[triangles] - np.roll(y[triangles], 1, axis=1)
    #     maxi = np.max(np.sqrt(xtri**2 + ytri**2), axis=1)
    #     # apply masking
    #     triang.set_mask(maxi > alpha)

    # apply_mask(triang2, alpha=1.5)

    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1, projection='3d')
    
    # ax.plot_trisurf(triang2, df_filtered['Price'], cmap='jet')
    # ax.scatter(df_filtered['Year'],df_filtered['Miles'],df_filtered['Price'], marker='.', s=10, c="black", alpha=0.5)
    # ax.view_init(elev=60, azim=-45)
    
    # ax.set_xlabel('Year')
    # ax.set_ylabel('Miles')
    # ax.set_zlabel('Price')
    # plt.show()

    # fig = plt.figure()
    # ax = plt.axes(projection = '3d')
    # ax.scatter3D(df['Year'],df['Miles'],df['Price'])

    # ax.set_xlim(min(df['Year']-1),max(df['Year']+1))
    # ax.set_ylim(0,100000)
    # ax.set_zlim(min(df['Price']-1000),40000)

    # fig = plt.figure()
    # ax = plt.axes(projection = '3d')
    # ax.scatter3D(df_filtered['Year'],df_filtered['Miles'],df_filtered['Price'])

    # ax.set_xlim(min(df_filtered['Year']-1),max(df_filtered['Year']+1))
    # ax.set_ylim(0,100000)
    # ax.set_zlim(min(df['Price']-1000),40000)


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

