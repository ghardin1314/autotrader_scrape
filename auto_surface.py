# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:49:59 2019

@author: Garrett
"""


import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd


def hessian(x):

    # breakpoint()

    """
    Calculate the hessian matrix with finite differences
    Parameters:
       - x : ndarray
    Returns:
       an array of shape (x.dim, x.ndim) + x.shape
       where the array[i, j, ...] corresponds to the second derivative x_ij
    """
    x_grad = np.gradient(x) 
    hessian = np.empty((x.ndim, x.ndim) + x.shape, dtype=x.dtype) 
    for k, grad_k in enumerate(x_grad):
        # iterate over dimensions
        # apply gradient again to every component of the first derivative.
        tmp_grad = np.gradient(grad_k) 
        for l, grad_kl in enumerate(tmp_grad):
            hessian[k, l, :, :] = grad_kl
    # breakpoint()
    laplace = hessian.trace()
    return laplace

def mean_curvature(Z):
    Zy, Zx  = np.gradient(Z)
    Zxy, Zxx = np.gradient(Zx)
    Zyy, _ = np.gradient(Zy)

    H = (Zx**2 + 1)*Zyy - 2*Zx*Zy*Zxy + (Zy**2 + 1)*Zxx
    H = -H/(2*(Zx**2 + Zy**2 + 1)**(1.5))

    return H

def gaussian_curvature(Z):
    Zy, Zx = np.gradient(Z)                                                     
    Zxy, Zxx = np.gradient(Zx)                                                  
    Zyy, _ = np.gradient(Zy)                                                    
    K = (Zxx * Zyy - (Zxy ** 2)) /  (1 + (Zx ** 2) + (Zy **2)) ** 2
    return K

if __name__ == '__main__':

    df = pd.read_csv('unfiltered_test.csv')
    
    x = np.array(df['Year'])
    y = np.array(df['Miles'])
    z = np.array(df['Price'])
    
    data = np.c_[x,y,z]
    
    mn = np.min(data, axis=0)
    mx = np.max(data, axis=0)
    X,Y = np.meshgrid(np.linspace(mn[0], mx[0], 100), np.linspace(mn[1], mx[1], 100))
    XX = X.flatten()
    YY = Y.flatten()
    
    A1 = np.ones(data.shape[0])
    A2 = data[:,:2]
    A3 = np.prod(data[:,:2], axis=1)
    A4 = data[:,:2]**2
    A5 = data[:,0]**2*data[:,1]
    A6 = data[:,1]**2*data[:,0]
    A7 = data[:,:2]**3
    
    #2nd order
    # A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
    
    #3rd order
    A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2, data[:,0]**2*data[:,1], data[:,1]**2*data[:,0], data[:,:2]**3]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])
    
    breakpoint()
    
    #2nd order
    # Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)
    
    #3rd order
    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2, XX**2*YY, YY**2*XX, XX**3, YY**3],C).reshape(X.shape)

    # breakpoint()

    ZZ = np.abs(hessian(Z))

    zmean = mean_curvature(Z)

    zgaus = gaussian_curvature(Z)

    # Zp = np.zeros([99,99])
    
    # breakpoint()
    
    # for i in range(len(Z[:,0])-1):
    #     for j in range(len(Z[0,:])-1):
    #         q= Z[i,j]-Z[i+1,j]
    #         w= Z[i,j]-Z[i,j+1]
    #         r = np.sqrt(q**2+w**2)
    #         Zp[i][j] = r
    
    # Zpp = np.zeros([98,98])
    
    # # breakpoint()
    
    # for i in range(len(Zp[:,0])-1):
    #     for j in range(len(Zp[0,:])-1):
    #         q= Zp[i,j]-Zp[i+1,j]
    #         w= Zp[i,j]-Zp[i,j+1]
    #         r = np.sqrt(q**2+w**2)
    #         Zpp[i][j] = r
    
    
    fig = plt.figure(0)
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
    # ax.scatter(data[:,0], data[:,1], data[:,2], c='r', s=50)
    plt.xlabel('X')
    plt.ylabel('Y')
    ax.set_zlabel('Z')

    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, zmean, rstride=1, cstride=1, alpha=0.2)
    # ax.scatter(data[:,0], data[:,1], data[:,2], c='r', s=50)
    plt.xlabel('X')
    plt.ylabel('Y')
    ax.set_zlabel('Z')

    fig = plt.figure(2)
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, zgaus, rstride=1, cstride=1, alpha=0.2)
    # ax.scatter(data[:,0], data[:,1], data[:,2], c='r', s=50)
    plt.xlabel('X')
    plt.ylabel('Y')
    ax.set_zlabel('Z')
