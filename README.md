# GOCE_SECS-EICS
Python Scripts for kriging SECS and EICS data and plotting.
The scripts also plots GOCE data. 

# Dependencies 

geostatsmodels
--------------
For Kriging the library used is the geostatsmodel developed by Connor Johnson.
The method of kriging used here is Simple Kriging, simple kriging involves interpolating the value at a give point
using neighbouring points and a model to weight each neighbour based on its distance.
The project page and example demonstration can be found here: [example](http://connor-johnson.com/2014/03/20/simple-kriging-in-python/)

The github project for the geostatsmodel can be found [here](http://github.com/cjohnson318/geostatsmodels)

Please follow the outlined steps on geostatsmodel page for a proper installation. The library is provided in this package as well. 

SciPy
-----
For all the matrix operations and plotting the SciPy package is required. The SciPy installation link can be found [here](http://www.scipy.org/install.html)

Basemap Matplotlib Toolkit
--------------------------
For the spatial plotting of data, the basemap extension to matlplotlib is required. matplotlib is installed with SciPy
but doesn't have the basemap extensions. Follow the instructions [here](http://matplotlib.org/basemap/users/installing.html)
for installing the basemap toolkit.


