# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:50:22 2019

@author: Garrett
"""


import requests
import pandas as pd
import numpy as np
import threading
import concurrent.futures
import re
import time
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import math
import scipy.linalg
from scipy.spatial import ConvexHull



class search_res:
    def __init__(self):
        self.value = []
        self.data = []
        self.listings = []
        self.verticies = []
        self.BestBuy = []
        self._lock = threading.Lock()
        
    def run_analysis(self, make_code, model_code, trim_code):
        
        self._get_results(make_code, model_code, trim_code)

        self._get_data()

        #This is some weird data formatting. Need to clean up later

        self.value.sort()

        data1 = self.value
        df = pd.DataFrame(data1, columns=['Year', 'Miles', 'Price'])
        x = np.array(df['Year'])
        y = np.array(df['Miles'])
        z = np.array(df['Price'])
        self.data = np.c_[x, y, z]

        self._get_verticies()

        self._get_bestbuy()    

    def _get_results(self, make_code, model_code, trim_code):

        """

        Parameters
        ----------
        make_code : STR, optional
            Internal make code. The default is [].
        model_code : STR, optional
            Internal model code. The default is [].
        trim_code : STR, optional
            Internal trim code. The default is [].

        Returns
        -------
        Pulls results from Autotrader.com. Max results are 1000. Pulls each 
        page individually and then appends each listing to self.listings

        """
        
        res = self._get_page(make_code=make_code, model_code=model_code,
                            trim_code=trim_code)

        numResults = res['totalResultCount']

        if numResults > 1000:
            pages = 10
        else:
            pages = math.ceil(numResults/100)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for i in range(1, pages):
                executor.submit(self._get_page(make_code=make_code,
                                              model_code=model_code,
                                              trim_code=trim_code, page=i))

    def _get_page(self, make_code=[], model_code=[], trim_code=[],
                 page=0):
        """

        Parameters
        ----------
        make_code : STR, optional
            Internal make code. The default is [].
        model_code : STR, optional
            Internal model code. The default is [].
        trim_code : STR, optional
            Internal trim code. The default is [].
        page : int, optional
            What page of results you want to pull. The default is 0.

        Returns
        -------
        results : JSON
            JSON page of results. Also pulls listings from page data and 
            appends to self.listings.

        """

        firstRecord = str(page*100)

        url_base = 'https://www.autotrader.com'
        path = '/rest/searchresults/base'
        url = url_base + path
        session = requests.Session()
        payload = {'makeCodeList': make_code,
                   'searchRadius': '0',
                   'listingTypes': 'USED',
                   'modelCodeList': model_code,
                   'trimCodeList': trim_code,
                   'zip': '90250',
                   'startYear': '2010',
                   'sortBy': 'distanceASC',
                   'numRecords': '100',
                   'firstRecord': firstRecord,
                   }
        headers= {'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"""}
        response = session.get(url, headers=headers, params=payload)
        results = response.json()
        self._pull_listings(results)
        return results

    def _pull_listings(self, results):
        """

        Parameters
        ----------
        results : JSON
            JSON of Autotrader API response.

        Returns
        -------
        None. Appends each listing to self.listings

        """
        page_listings = results['listings']
        with self._lock:
            for item in page_listings:
                self.listings.append(item)

    def _get_data(self):
        """
        Extracts Year, Miles, and Price from each listing. Stores data in 
        self.value

        Returns
        -------
        None.

        """

        for item in self.listings:

            # breakpoint()
            try:
                year = item['year']
                miles = item['specifications']['mileage']['value']
                miles = int(re.sub('\W+', '', miles))
                price = item['pricingDetail']['primary']

                self.value.append([year, miles, price])
            except:
                # print('error on data placeholder')
                continue

    def _get_verticies(self):
        """
        Gets the verticies of the convex hull that incapsulates Price-Miles 
        space of results. Appends verticies to self.verticies

        Returns
        -------
        None.

        """
        
        years = list(set(self.data[:, 0]))
        years.sort()
    
        dataRange = []
        for year in years:
            temp = np.where(self.data[:, 0] == year)
            maxI = max(temp[0])
            minI = min(temp[0])
            maxMiles = max(self.data[minI:maxI+1, 1])
            minMiles = min(self.data[minI:maxI+1, 1])
            maxPrice = max(self.data[minI:maxI+1, 2])
            minPrice = min(self.data[minI:maxI+1, 2])
            ranges = [year, maxMiles, minMiles, maxPrice, minPrice]
            dataRange.append(ranges)
    
        dataRange = pd.DataFrame(dataRange, columns=['Year',
                                                     'MaxMiles', 'MinMiles',
                                                     'MaxPrice', 'MinPrice'])
        points = []
    
        for i, year in enumerate(dataRange['Year']):
            points.append([year, dataRange['MaxMiles'][i]])
            points.append([year, dataRange['MinMiles'][i]])
    
        points = np.array(points)
    
        hull = ConvexHull(points)
        vertex_ind = hull.vertices
        vertex_ind = np.append(vertex_ind, vertex_ind[0])
        self.verticies = points[vertex_ind, :]

    def _get_bestbuy(self):
        """
        Takes Year, Miles, Price data and create a cubic surface to approximate
        results. Then finds minimum curvature of the surface inside of the
        Year-Miles domain range. This is the place where depreciation is 
        decelerating the most and therefore the optimal place to buy a car.
        Appends best Year and Miles to self.BestBuy

        Returns
        -------
        None.

        """
        mn = np.min(self.data, axis=0)
        mx = np.max(self.data, axis=0)
        
        X, Y = np.meshgrid(np.linspace(mn[0], mx[0], 100), np.linspace(mn[1],
                           mx[1], 100))
        XX = X.flatten()
        YY = Y.flatten()
    
        A1 = np.ones(self.data.shape[0])
        A2 = self.data[:, :2]
        A3 = np.prod(self.data[:, :2], axis=1)
        A4 = self.data[:, :2]**2
        A5 = self.data[:, 0]**2*self.data[:, 1]
        A6 = self.data[:, 1]**2*self.data[:, 0]
        A7 = self.data[:, :2]**3

        A = np.c_[A1, A2, A3, A4, A5, A6, A7]


        C, _, _, _ = scipy.linalg.lstsq(A, self.data[:, 2])
    
        Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2, XX**2*YY,
                         YY**2*XX, XX**3, YY**3], C).reshape(X.shape)

        H = self._mean_curvature(Z)

        H_flat = [item for sublist in H for item in sublist]
        H_flat.sort()

        for value in H_flat:

            index = np.where(H == value)
            xmin = int(X[index[0], index[1]])
            ymin = int(Y[index[0], index[1]])

            if self._inside(self.verticies, xmin, ymin):
                xmin = round(xmin)
                ymin = round(ymin/1000)*1000
                self.BestBuy = [xmin, ymin]
                break

    def _mean_curvature(self, Z):
        """
        Finds the mean curvature of a square matrix Z
        """
        Zy, Zx = np.gradient(Z)
        Zxy, Zxx = np.gradient(Zx)
        Zyy, _ = np.gradient(Zy)
    
        H = (Zx**2 + 1)*Zyy - 2*Zx*Zy*Zxy + (Zy**2 + 1)*Zxx
        H = -H/(2*(Zx**2 + Zy**2 + 1)**(1.5))
    
        return H
    
    def _inside(self, verticies, x, y):
        """
        Tests if point (x,y) is located in a shape that has verticies
        """
        inside = True
        for i in range(1, len(verticies)):
            res = self._cross(verticies[i-1], verticies[i], (x, y))
    
            if res < 0:
                inside = False
                break
    
        return inside
    
    def _cross(self, o, a, b):
        """ 2D cross product of OA and OB vectors,
         i.e. z-component of their 3D cross product.
        :param o: point O
        :param a: point A
        :param b: point B
        :return cross product of vectors OA and OB (OA x OB),
         positive if OAB makes a counter-clockwise turn,
         negative for clockwise turn, and zero
         if the points are colinear.
        """
    
        res = (a[0] - o[0]) * (b[1] - o[1]) -\
              (a[1] - o[1]) * (b[0] - o[0])
    
        return res

if __name__ == '__main__':
    
    test2 = search_res()
    test2.run_analysis(make_code='FORD', model_code='MUST',
                     trim_code='MUST|GT')
    
    print(test2.BestBuy)
    
    # This is the graveyard for testing
    '_________________________________________________________________________'
    
    # test1 = search_res()


    # time_start = time.time()

    # test1.get_results(make_code='FORD', model_code='MUST',
    #                  trim_code='MUST|GT')
    
    
    # # breakpoint()

    # # print(time.time()-time_start)
    
    # test1.get_data()
    # data1 = test1.value
    
    # # print(time.time()-time_start)

    # data1.sort()

    # df = pd.DataFrame(data1, columns=['Year', 'Miles', 'Price'])
    # x = np.array(df['Year'])
    # y = np.array(df['Miles'])
    # z = np.array(df['Price'])

    # data = np.c_[x, y, z]
    
    # dataRange = []

    # years = list(set(data[:, 0]))
    # years.sort()

    # for year in years:
    #     temp = np.where(data[:, 0] == year)
    #     maxI = max(temp[0])
    #     minI = min(temp[0])
    #     maxMiles = max(data[minI:maxI+1, 1])
    #     minMiles = min(data[minI:maxI+1, 1])
    #     maxPrice = max(data[minI:maxI+1, 2])
    #     minPrice = min(data[minI:maxI+1, 2])
    #     ranges = [year, maxMiles, minMiles, maxPrice, minPrice]
    #     dataRange.append(ranges)

    # dataRange = pd.DataFrame(dataRange, columns=['Year',
    #                                              'MaxMiles', 'MinMiles',
    #                                              'MaxPrice', 'MinPrice'])
    # points = []

    # for i, year in enumerate(dataRange['Year']):
    #     points.append([year, dataRange['MaxMiles'][i]])
    #     points.append([year, dataRange['MinMiles'][i]])

    # points = np.array(points)

    # hull = ConvexHull(points)
    # vertex_ind = hull.vertices
    # vertex_ind = np.append(vertex_ind, vertex_ind[0])
    # verticies = points[vertex_ind, :]
    
    # verts2 = test2.verticies
    
    # '_________________________________________________________________________'



    # mn = np.min(data, axis=0)
    # mx = np.max(data, axis=0)
    # X, Y = np.meshgrid(np.linspace(mn[0], mx[0], 100), np.linspace(mn[1],
    #                    mx[1], 100))
    # XX = X.flatten()
    # YY = Y.flatten()
    
    # data2 = test2.value
               
    
    # # breakpoint()

    # A1 = np.ones(data.shape[0])
    # A11 = test2.A1
    # A2 = data[:, :2]
    # A22 = test2.A2
    # A3 = np.prod(data[:, :2], axis=1)
    # A33 = test2.A3
    # A4 = data[:, :2]**2
    # A44 = test2.A4
    # A5 = data[:, 0]**2*data[:, 1]
    # A55 = test2.A5
    # A6 = data[:, 1]**2*data[:, 0]
    # A66 = test2.A6
    # A7 = data[:, :2]**3
    # A77 = test2.A7

    # breakpoint()

    # A = np.c_[A1, A2, A3, A4, A5, A6, A7]
    
    # print(A == test2.A)
    
    # C, _, _, _ = scipy.linalg.lstsq(A, data[:, 2])

    # Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2, XX**2*YY,
    #                  YY**2*XX, XX**3, YY**3], C).reshape(X.shape)

    # H = mean_curvature(Z)

    # H_flat = [item for sublist in H for item in sublist]
    # H_flat.sort()

    # for value in H_flat:

    #     index = np.where(H == value)
    #     xmin = int(X[index[0], index[1]])
    #     ymin = int(Y[index[0], index[1]])

    #     if inside(verticies, xmin, ymin):
    #         xmin = round(xmin)
    #         ymin = round(ymin/1000)*1000
    #         BestBuy = [xmin, ymin]
    #         break
    # # print(BestBuy == test2.BestBuy)
    
    # breakpoint()


