__author__ = 'Sonal Ranjit'

'''
This script parses through a GOCE satellite data that includes time information and geodetic coordinates, and based on
a SECS grid for that time an amplitude value is krigged for the satellite posiiton.

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
    lon = lla[:,1]/180.*pi

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

def plot_grid(grid,satPos,title):
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
    #find all the indices of the negative amplitudes in grid data.
    negs = np.where(z<0)[0]
    poss = np.where(z>0)[0]


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
    #m = Basemap(width=8000000, height=8000000, resolution='l', projection='laea',\
            #lat_ts=min(grid[:,0]), lat_0=np.median(grid[:,0]),lon_0=-100.)

    m = Basemap(width=8000000, height=8000000, resolution='l', projection='lcc',\
             lat_0=60,lon_0=-100.)
    m.drawcoastlines()    #draw the coastlines on the basemap

    # draw parallels and meridians and label them
    m.drawparallels(np.arange(-80.,81.,20.),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1],fontsize=10)

    # Project the inputted grid into x,y values defined of the projected basemap parameters
    x,y =m(grid[:,1],grid[:,0])
    satx,saty = m(satPos[0,1],satPos[0,0])

    '''
    Plot the inputted grid as a scatter plot on the basemap,
    1) x,y are the projected latitude and longitude coordinates of the grid
    2) s is the size of the scatter point it is base of the amplitude of the ionospheric current
    3) c is the colormap for the scatter point
    '''
    m.scatter(x[negs],y[negs],s=abs(grid[negs,2])/300,marker=',',c='#0000FF',edgecolors='none')
    m.scatter(x[poss],y[poss],s=abs(grid[poss,2])/300,marker=',',c='#FF0000',edgecolors='none')
    m.scatter(satx,saty,s=abs(satPos[0,2])/300,c='#66FF66',edgecolors='none',marker=',')
    m.scatter(satx,saty,s=800,facecolors='none',edgecolors='#66FF66',linewidth='5')

    #title of the figure
    plt.title(title)

    # show the figure
    #plt.show() #comment this if you don't want to display the figure for every grid.

    # save the figure
    plt.savefig('/home/sonal/SECS_201104/figs/'+title+'.png',bbox_inches='tight',pad_inches=0.1)
    plt.clf()

'''
Main part of the script, here the GOCE satellite time stamp and position is loaded. Then for each timestamp and position
the corresponding SECS grid is searched. If there is a SECS grid for the current time of the satellite then, using
the SECS grid a value is krigged for the current satellite position, and a figure plotted and saved.
'''

# Load the GOCE satellite data
sat_data = np.loadtxt('/home/sonal/SECS/sat_track_201104.txt')
# add an extra column in the satellite data for it be replaced with the krigged value
zero_col = np.zeros((len(sat_data),1))
sat_data = np.column_stack((sat_data,zero_col))
prev_min = []
#for i in range(0,100):
# Iterate through the whole matrix of satellite data
for i in range(548646,len(sat_data)):
    '''
    This section of the loop parses the time information from the satellite data to form a string which is used to check
    if a SECS grid exists for that time.
    '''
    # Define the path to where all the SECS grids lie
    secs_path = '/home/sonal/SECS_EICS/SECS/'

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
    SEC_file = secs_path+'SECS'+sat_ymd+'/'+sat_d+'/'+'SECS'+sat_ymd+'_'+sat_hms+'.dat'
    '''
    This sections checks if there is a SECS grid available for the current time instance of the satellite data, if it
    does exits then the SECS grid is loaded, and using the grid a value is krigged for the current satellite position
    on the grid.
    '''
    #if os.path.exists(SEC_file):
    if os.path.exists(SEC_file) and (sat_mins != prev_min):

        print "Processing file "+str(i)+" of "+str(len(sat_data))

        # Load the SECS grid and convert to ECEF
        sec_grid = np.loadtxt(SEC_file)
        grid_xyz = lla2ecef(sec_grid)

        # Load the Satellite position and convert it to ECEF
        sat_latlon = np.zeros((1,3))
        sat_latlon[:,(0,1)] = sat_data[i,(6,7)]
        sat_xyz = lla2ecef(sat_latlon)

        # Determine the sill for the semivariance model of the grid
        sill = np.var(grid_xyz[:,2])

        # Define the type of semivariacne model to be used for kriging
        covfct = model.covariance(model.exponential,(900000, sill))

        # Krig the value for the satellite position using simple kriging and the defined semivariance model and 10
        # neighbouring points
        ptz = kriging.simple(grid_xyz,covfct,sat_xyz[:,:2],N=10)

        # Add the krigged value to the different variables
        sat_latlon[0,2] = ptz[0]
        sat_xyz[0,2] = ptz[0]
        sat_data[i,8] = ptz[0]
        timestamp = sat_ymd+sat_hms
        plot_grid(sec_grid, sat_latlon, timestamp)
    prev_min = sat_mins
# Save the updated satellite data with the krigged values
#np.savetxt('sat_data_april_krigged.txt',sat_data,delimiter='\t')