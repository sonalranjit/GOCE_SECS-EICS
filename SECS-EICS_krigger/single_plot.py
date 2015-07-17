__author__ = 'sonal'

import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os
from math import *
import matplotlib
#matplotlib.rcParams['legend.handlelength']=1
def plot_grid(grid,sat_track,sat_krig,title):
    ''' This function plots a scatter map of the SECS Grid and its amplitudes, and the Krigged value for the satellite
    and its position.

    ----------------------------------------------------
    INPUT:
    1) grid --> is the SECS grid
    2) satPos --> is the position of the satellite and its krigged value
    3) title --> is the timestamp of the satellite

    ----------------------------------------------------
    OUTPUT: A figure of the SECS grid and the satellite position with its krigged value
    '''

    # The amplitude of the vertical ionospheric current
    z = grid[:,2]

    '''Defining the colormap for the positive and negative values of the vertical ionospheric current,
       The colormap is defined by the variable colmap, it is just defined as 1 for positive amplitude
       and 0 for negative amplitude. This colors the amplitude red for positive values and blue for negative values.
    '''

    # Preallocate a column vector of ones for the colormap
    #colmap = np.array((len(grid),1),object)
    #colmap[:] = (1,0,0)
    #find all the indices of the negative amplitudes in grid data.
    negs = np.where(z<0)[0]
    poss = np.where(z>0)[0]
    # for the indices with negative values define the colormap as 0.
    #colmap[negs][0] = (0,0,1)
    ''' This next section of the function is where the plotting of the figure takes places. The module used for plotting
    data on maps is the built in module in matplotlib called mpl_toolkits.
    Source and api: http://matplotlib.org/basemap/index.html
    The module allows to plot 2D data on maps, with various different projections, it is similar to MATLAB mapping
    toolbox and GMT.
    '''

    # Defining the size of the figure in inches
    plt.figure(figsize=(18,18))

    '''
    The m variable defines the basemap of area that is going to be displayed.
    1) width and height is the area in pixels of the area to be displayed.
    2) resolution is the resolution of the boundary dataset being used 'c' for crude and 'l' for low
    3) projection is type of projection of the basemape, in this case it is a Lambert Azimuthal Equal Area projection
    4) lat_ts is the latitude of true scale,
    5) lat_0 and lon_0 is the latitude and longitude of the central point of the basemap
    '''
    m = Basemap(width=8000000, height=8000000, resolution='l', projection='lcc',\
             lat_0=60,lon_0=-100.)
    #m = Basemap(width=8000000, height=8000000,llcrnrlon =-160., llcrnrlat=40.,urcrnrlon=-20.,urcrnrlat=80.,projection='lcc',lat_1=45.,lat_2=55.,lat_0=45,lon_0=-100.)

    m.drawcoastlines()    #draw the coastlines on the basemap

    # draw parallels and meridians and label them
    m.drawparallels(np.arange(-80.,81.,20.),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1],fontsize=10)

    # Project the inputted grid into x,y values defined of the projected basemap parameters
    x,y =m(grid[:,1],grid[:,0])
    satx,saty =m(sat_track[::10,7],sat_track[::10,6])
    satkrigx,satkrigy = m(sat_krig[1],sat_krig[0])
    '''
    Plot the inputted grid as a scatter plot on the basemap,
    1) x,y are the projected latitude and longitude coordinates of the grid
    2) s is the size of the scatter point it is base of the amplitude of the ionospheric current
    3) c is the colormap for the scatter point
    '''
    #m.scatter(x,y,s=abs(grid[:,2])/300,marker=',',c = '#0000FF' ,edgecolors='none')
    secs_negs = m.scatter(x[negs],y[negs],s=abs(grid[negs,2])/300,marker=',',c = '#0000FF' ,edgecolors='none')
    secs_pos =m.scatter(x[poss],y[poss],s=abs(grid[poss,2])/300,marker=',',c = '#FF0000' ,edgecolors='none')
    satpos = m.scatter(satx,saty,s=100,marker='.',c='#009933',edgecolors='none')
    satkrig = m.scatter(satkrigx,satkrigy,s=abs(sat_krig[2])/300,marker=',',c='#66FF66',label=str(abs(sat_krig[2])))
    sat_halo = m.scatter(satkrigx,satkrigy,s=800,facecolors='none',edgecolors='#66FF66',linewidth='5')

    plt.legend((satpos,satkrig),('Satellite Track',u'\u00B1' +' 5700 A'),scatterpoints =1)

    #title of the figure/home/sonal/SECS_EICS/SECS/SECS20110310/10
    plt.title(title)

    # show the figure
    #plt.show() #comment this if you don't want to display the figure for every grid.
    plt.savefig('SECS_20110311_170600.png',bbox_inches='tight',pad_inches=0.2)



sec_grid = np.loadtxt('/home/sonal/SECS_EICS/SECS/SECS20110311/11/SECS20110311_170600.dat')
sat_track = np.loadtxt('sat_track_20110311_170600.txt')
sat_krigged =np.array([6.496399999999999864e+01,2.185699999999999932e+02,5.708898782685990227e+03])
plot_grid(sec_grid,sat_track,sat_krigged, '20110311_170600')

#20110311002400
# 5.373599999999999710e+01	2.656499999999999773e+02	1.549485103880631414e+03

#20110311170600
#6.496399999999999864e+01	2.185699999999999932e+02	5.708898782685990227e+03