# SECS and EICS kriggin and plotting
Python Scripts for kriging SECS and EICS data and plotting.
The two main scripts for the kriging and plotting are `SECS_krig.py` and `EICS_krig.py`. 

The script takes in an input array of the satellite track in latitude and longitude, and its corresponding timestamp. 
The inputted satellite track is a text file, where the first 7 columns are for the timestamp. It has to formatted as:
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
        <td>00</td>
        <td>45.000</td>
        <td>298.000</td>
    </tr>
</table>
