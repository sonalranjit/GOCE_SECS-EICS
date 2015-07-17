__author__ = 'sonal'
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os
from math import *

def plot_grid(EIC_grid,sat_track,sat_krig,title):
    '''
    This function plots a scatter map of the EICS grid and its horizontal components, and the krigged value for the
    satellite.

    :param EIC_grid: The EICS grid
    :param satPos: The position of the satellite
    :param ptz_u: The krigged u component of the satellite
    :param ptz_v: The krigged v component of the satllite
    :param title: Timestamp of the satellite
    :return: The figure
    '''

    # Define the size of the figure in inches
    plt.figure(figsize=(18,18))

    # The horizontal components of the Ionospheric current from the EICS grid
    u = EIC_grid[:,2]
    v = EIC_grid[:,3]

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

    m.drawcoastlines() #draw the coastlines on the basemap

    # draw parallels and meridians and label them
    m.drawparallels(np.arange(-80.,81.,20.),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1],fontsize=10)

    # Project the inputted grid into x,y values defined of the projected basemap parameters
    x,y =m(EIC_grid[:,1],EIC_grid[:,0])
    satx,saty = m(sat_track[::10,7],sat_track[::10,6])
    satkrigx,satkrigy = m(sat_krig[1],sat_krig[0])


    '''
    Plot the inputted grid as a quiver plot on the basemap,
    1) x,y are the projected latitude and longitude coordinates of the grid
    2) u and v are the horizontal components of the current
    3) the EICS grid values are plotted in blue color where as the satellite krigged values are in red
    '''
    eic = m.quiver(x,y,u,v,width = 0.004, scale=10000,color='#0000FF')
    satkrig = m.quiver(satkrigx,satkrigy,sat_krig[2],sat_krig[3],color='#FF0000',width=0.004, scale = 10000)
    satpos = m.scatter(satx,saty,s=100,marker='.',c='#009933',edgecolors='none',label='Satellite Track')
    sat_halo = m.scatter(satkrigx,satkrigy,s=400,facecolors='none',edgecolors='#66FF66',linewidth='5')

    plt.title(title)
    plt.legend([satpos],['Satellite Track'],loc='upper right',scatterpoints=1)
    plt.quiverkey(satkrig,0.891,0.948,520,u'\u00B1' +'520 mA/m',labelpos='E')

    plt.savefig('EICS_20110311_002400.png',bbox_inches='tight',pad_inches=0.2)
    #plt.show()

eics_grid = np.loadtxt('/home/sonal/SECS_EICS/EICS/EICS20110311/11/EICS20110311_002400.dat')
sat_track = np.loadtxt('satpos_0311002400.txt')
sat_krigged =np.array([5.373599999999999710e+01,	2.656499999999999773e+02,	8.653521762583993393e+01,	7.892852606410862109e+02])
plot_grid(eics_grid,sat_track,sat_krigged, '20110311_002400')

#20110311002400
#5.373599999999999710e+01	2.656499999999999773e+02	8.653521762583993393e+01	7.892852606410862109e+02

#20110311170600
#6.496399999999999864e+01	2.185699999999999932e+02	9.197923974020349078e+02	-2.258385440140647006e+03