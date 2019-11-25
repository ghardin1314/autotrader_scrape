# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 21:02:45 2019

@author: Garrett
"""


import pandas as pd
import numpy as np
import matplotlib.tri as tri
import matplotlib.pyplot as plt

df = pd.read_csv('unfiltered_test.csv')

x = np.array(df['Year'])
y = np.array(df['Miles'])
z = np.array(df['Price'])

# x_test = []

# for i in range(len(x)):

#     if x[i] == 2016:
#         x_test.append([y[i],z[i]])

# breakpoint()

# x_test = np.array(x_test)

# p = np.polyfit(x_test[:,0],x_test[:,1], 2)
# z = np.poly1d(p)

# x_plot = np.linspace(min(x_test[:,0]), max(x_test[:,0]), 100)
# y_plot = z(x_plot)

# _ = plt.plot(x_test[:,0], x_test[:,1], '.', x_plot, z(x_plot), '-')
# plt.show()


triang1 = tri.Triangulation(x, y)
triang2 = tri.Triangulation(x, y)


def apply_mask(triang, alpha=0.4):

    # breakpoint()
    # Mask triangles with sidelength bigger some alpha
    triangles = triang.triangles
    # Mask off unwanted triangles.
    xtri = x[triangles] - np.roll(x[triangles], 1, axis=1)
    ytri = y[triangles] - np.roll(y[triangles], 1, axis=1)
    maxi = np.max(np.sqrt(xtri**2 + ytri**2), axis=1)
    # apply masking
    triang.set_mask(maxi > alpha)

apply_mask(triang2, alpha=15)


fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection='3d')

# ax.plot_trisurf(triang2, z, cmap='jet')
ax.scatter(x, y, z, marker='.', s=10, c="black", alpha=0.5)
ax.view_init(elev=60, azim=-45)

ax.set_xlabel('Year')
ax.set_ylabel('Miles')
ax.set_zlabel('Price')
plt.show()
