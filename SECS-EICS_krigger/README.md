# SECS and EICS krigging and plotting
Python Scripts for kriging SECS and EICS data and plotting.
The two main scripts for the kriging and plotting are `SECS_krig.py` and `EICS_krig.py`. 

The script takes in an input array of the satellite track in latitude and longitude, and its corresponding timestamp. 
The inputted satellite track is an ASCII text file, where the first 7 columns are for the timestamp. It has to formatted as:
<table style="width:100%">
    <tr>
        <th>YEAR</th>
        <th>MONTH</th>
        <th>DAY</th>
        <th>HOUR</th>
        <th>MINUTES</th>
        <th>SECONDS</th>
        <th>Latitude</th>
        <th>Longitude</th>
    </tr>
    <tr>
        <td>2011</td>
        <td>03</td>
        <td>01</td>
        <td>00</td>
        <td>00</td>
        <td>00.000</td>
        <td>45.000</td>
        <td>298.000</td>
    </tr>
</table>

The script then just parses through the inputted array, it searches the directory where all the SECS and EICS grids are 
located for a grid with the corresponding timestamp. If a corresponding grid with the matching timestamp is found, then the SECS or 
EICS grid is loaded, then the Equivalent Ionoshperic Current value is krigged for the current coordinates using
the SECS or EICS grid. The krigged value is appended in a new column of the loaded array, then a figure is produced with
the krigged value on top on the SECS or EICS grid. 

Usage
------

To use the script there are only 2 variables to change.
*   The path to where all the SECS/EICS grids lie. 
    *   ex: `/path_to_SECS/SECS/SECSYYYYMMDD/`
*   The path to the GOCE satellite track data.
  