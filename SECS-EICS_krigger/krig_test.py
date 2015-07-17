from geostatsmodels import utilities, variograms, model, kriging, geoplot
import numpy as np
import matplotlib.pyplot as plt
from math import *

z = utilities.readGeoEAS('ZoneA.dat')
P = z[:,[0,1,3]]

pt = [2000, 4700]

plt.scatter(P[:,0], P[:,1], c=P[:,2], cmap=geoplot.YPcmap)
plt.title('Zone A Subset % Porosity')
plt.colorbar()
xmin, xmax = 0, 4250
ymin, ymax = 3200, 6250
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
for i in range( len( P[:,2] ) ):
    x, y, por = P[i]
    if( x < xmax )&( y > ymin )&( y < ymax ):
        plt.text( x+100, y, '{:4.2f}'.format( por ) )
plt.scatter( pt[0], pt[1], marker='x', c='k' )
plt.text( pt[0]+100 , pt[1], '?')
plt.xlabel('Easting (m)')
plt.ylabel('Northing (m)')
plt.show()

tolerance = 250
lags = np.arange(tolerance, 10000, tolerance*2)
sill = np.var(P[:,2])

geoplot.semivariogram(P, lags, tolerance)

svm = model.semivariance(model.spherical, (4000, sill))
geoplot.semivariogram(P, lags, tolerance, model=svm)

covfct = model.covariance(model.spherical, (4000, sill))
print kriging.simple(P, covfct, pt, N=6)
