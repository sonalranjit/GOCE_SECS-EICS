__author__ ="Sonal Ranjit"
'''
This script parses through a GOCE satellite data that includes time information and geodetic coordinates, and based on
a EICS grid for that time the horizontal components of the Ionospheric current is krigged for the satellite postion.

The package used for kriging is geostatsmodel developed by Connor Johnson.
A simple example can be found at: http://connor-johnson.com/2014/03/20/simple-kriging-in-python/

The github for the project can be accessed at: https://github.com/cjohnson318/geostatsmodels
'''
from geostatsmodels import model, kriging
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os
from math import *

def lla2ecef(lla):
    ''' This functions converts and inputted matrix of geodetic coordinates of size nx3 to ECEF coordinates on
    the ellipsoid so ellipsoid height =0, then outputs it.

    --------------------------------------------------------------
    INPUT: A row vector or a matrix of geodetic coordinates, Latitude, Longitude, and height. the height in this case
    can be 0 or for the GOCE data type it can just be the instrument value since the coordinates are going to be
    converted only to the surface of the ellipsoid.

    ---------------------------------------------------------------
    OUTPUT: A row vector or a matrix of ECEF coordinates, X, Y , and height or the instrument value in this case.

    '''

    #Constats WGS84
    a = 6378137.
    b = 6356752.3142
    e2 = 1-(b**2)/(a**2)

    # check for 1D case:
    dim = len(lla.shape)
    if dim == 1:
        lla = np.reshape(lla,(1,3))

    # convert lat and lon to radians
    lat = lla[:,0]/180.*pi

    lon = (lla[:,1]+360)/180.*pi

    # preallocate the output vector for the ECEF coordinates
    xyz = np.array(np.zeros(lla.shape))

    # Radius of the prime vertical
    N = a/np.sqrt(1-e2*np.sin(lat)*np.sin(lat))

    # Calculate the X-coordinate
    xyz[:,0] = (N)*np.cos(lat)*np.cos(lon)

    # Calculate the Y-coordinate
    xyz[:,1] = N*np.sin(lon)*np.cos(lat)

    # Keep the SECS data as it is
    xyz[:,2] = lla[:,2]

    #return the ECEF coordinates
    return np.array(xyz)

def plot_grid(EIC_grid,sat_latlon,ptz_u,ptz_v,title):
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
    m = Basemap(width=8000000, height=8000000, resolution='l', projection='laea',\
                lat_ts=min(EIC_grid[:,0]), lat_0=np.median(EIC_grid[:,0]),lon_0=-100.)

    m.drawcoastlines() #draw the coastlines on the basemap

    # draw parallels and meridians and label them
    m.drawparallels(np.arange(-80.,81.,20.),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1],fontsize=10)

    # Project the inputted grid into x,y values defined of the projected basemap parameters
    x,y =m(EIC_grid[:,1],EIC_grid[:,0])
    satx,saty = m(sat_latlon[0,1],sat_latlon[0,0])

    '''
    Plot the inputted grid as a quiver plot on the basemap,
    1) x,y are the projected latitude and longitude coordinates of the grid
    2) u and v are the horizontal components of the current
    3) the EICS grid values are plotted in blue color where as the satellite krigged values are in red
    '''
    m.quiver(x,y,u,v,width = 0.004, scale=10000,color='#0000FF')
    m.quiver(satx,saty,ptz_u[0],ptz_v[0],color='#FF0000',width=0.004, scale = 10000)
    m.scatter(satx,saty,s=400,facecolors='none',edgecolors='#66FF66',linewidth='5')

    plt.title(title)
    plt.savefig('/home/sonal/EICS_201104/figs/'+title+'.png',bbox_inches='tight',pad_inches=0.1)
    #plt.show()
    plt.clf()


'''
Main part of the script, here the GOCE satellite time stamp and position is loaded. Then for each timestap and position
the corresponding EICS grid is searched. If there is a EICS grid for the current time of the satellite then, using
the EICS grid the horizontal components value is krigged for the current satellite position, and a figure plotted and saved.
'''

#Load the GOCE satellite data
sat_data = np.loadtxt('/home/sonal/SECS/sat_track_201104.txt')
# add an extra column in the satellite data for it be replaced with the krigged value
zero_col = np.zeros((len(sat_data),2))
sat_data = np.column_stack((sat_data,zero_col))
prev_min = []
# Iterate through the whole matrix of satellite data
for i in range(len(sat_data)):

    '''
    This section of the loop parses the time information from the satellite data to form a string which is used to check
    if a EICS grid exists for that time.
    '''

    # Define the path to where all the EICS grids lie
    eics_path = '/home/sonal/EICS_201104/'

    # Extract the Year, Month, Day, Hour, Minutes, Seconds from the satellite data.
    sat_y = str(int(sat_data[i,0]))
    sat_m = str(int(sat_data[i,1])).zfill(2)
    sat_d = str(int(sat_data[i,2])).zfill(2)
    sat_ymd = sat_y+sat_m+sat_d
    sat_h = str(int(sat_data[i,3])).zfill(2)
    sat_mins = str(int(sat_data[i,4])).zfill(2)
    sat_secs = str(int(floor(sat_data[i,5]))).zfill(2)
    sat_hms = sat_h+sat_mins+sat_secs

    # Concatenate all the time information to a single string to see if the SECS grid exists
    EICS_file = eics_path+'EICS'+sat_ymd+'/'+sat_d+'/'+'EICS'+sat_ymd+'_'+sat_hms+'.dat'

    '''
    This sections checks if there is a EICS grid available for the current time instance of the satellite data, if it
    does exists then the EICS grid is loaded, and using the grid a value is krigged for the current satellite position
    on the grid.
    '''
    #if os.path.exists(EICS_file):
    if os.path.exists(EICS_file) and (sat_mins !=prev_min):
        print "Processing file "+str(i)+" of "+str(len(sat_data))

        # Load the EICS grid and convert to ECEF
        EIC_grid = np.loadtxt(EICS_file)
        eic_u = EIC_grid[:,:3]
        eic_v = np.column_stack((EIC_grid[:,:2],EIC_grid[:,3]))

        #The EICS grid contains 2 values for the horizontal components have to separate them and krig it separately
        eic_xyu = lla2ecef(eic_u)
        eic_xyv = lla2ecef(eic_v)

        # Load the Satellite position and convert it to ECEF
        sat_latlon = np.zeros((1,3))
        sat_latlon[:,(0,1)] = sat_data[i,(6,7)]
        sat_latlon[:,1] = sat_latlon[:,1]-360
        sat_xyz = lla2ecef(sat_latlon)

        # Determine the sill for the semivariance model of the grid
        sill_u = np.var(eic_xyu[:,2])
        sill_v = np.var(eic_xyv[:,2])

        # Define the type of semivariance model to be used for kriging
        covfct_u = model.covariance(model.exponential,(900000, sill_u))
        covfct_v = model.covariance(model.exponential,(900000, sill_v))

        # Krig the value for the satellite position using simple kriging and the defined semivariance model and 10
        # neighbouring points
        ptz_u = kriging.simple(eic_xyu,covfct_u,sat_xyz[:,:2],N=10)
        ptz_v = kriging.simple(eic_xyv,covfct_v,sat_xyz[:,:2],N=10)

        # Add the krigged value to the different variables
        sat_data[i,8] = ptz_u[0]
        sat_data[i,9] = ptz_v[0]
        timestamp = sat_ymd+sat_hms

        #Call the plotting function to plot the grid and krigged values
        plot_grid(EIC_grid,sat_latlon,ptz_u,ptz_v,timestamp)
    prev_min = sat_mins

#np.savetxt('sat_EICS_april_krigged.txt',sat_data,delimiter='\t')
