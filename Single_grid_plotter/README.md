# Single Grid Plot
The script single_grid_plot.py plots an inputted grid of Latitude, Longitude and Value on the specified project. 
The script is setup to take in GOCE dataset, the same format as the SECS and EICS data. Where columns 1-7 are 
reserved for the date and time. **bold**The latitude and longitude columns are 7 and 8**bold**. The value to be plotted on the 
corresponding coordinates can be specified in the function. 

Usage
------
1. First load the grid as a numpy array. 
    `<code>` example_grid = np.loadtxt('example_grid.txt')
There is one main function in the script polar_plot().