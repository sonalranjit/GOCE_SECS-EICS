__author__ = 'sonal'

import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
from math import *

def polar_plot(grid, title):

    #z = grid[:,8]
    u = grid[:,8]
    v = grid[:,9]
    plt.figure(figsize=(18,18))
    ax = plt.gca()
    #m = Basemap(projection='npaeqd',boundinglat=20,lon_0=-100.,resolution='l')
    m = Basemap(width=8000000, height=8000000, resolution='l', projection='lcc',\
             lat_0=60,lon_0=-100.)
    m.drawcoastlines()
    m.drawparallels(np.arange(-80.,81,20.),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1],fontsize=10)

    x,y =m(grid[:,7],grid[:,6])
    sc = m.scatter(x,y,s=abs(u),c=u,marker=',',cmap=cm.jet,alpha=0.9,edgecolors='none')
    plt.title(title)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cb1 = plt.colorbar(sc,cax=cax)
    cb1.set_label("mA/m",fontsize=18)
    plt.savefig('GOCE_asc_EICSu_krigged_201104.png',bbox_inches='tight',pad_inches=0.2)
    #plt.show()

def asc_desc(data):
    asc = []
    desc = []
    lat = data[:,6]
    for i in range(0,len(data)-1):
        if lat[i+1] >= lat[i]:
            asc.append(i)
        else:
            desc.append(i)

    return asc, desc

SECS_data = np.loadtxt('EICS_201103_krigged.txt')

asc_idx, desc_idx= asc_desc(SECS_data)

asc_track = SECS_data[asc_idx,:]
desc_track = SECS_data[desc_idx,:]


polar_plot(asc_track,'GOCE Ascending EICS u component Krigged April, 2011')