__author__ = 'sonal'

import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

def polar_plot(grid, col, title,filename):

    z = grid[:,col]
    plt.figure(figsize=(18,18))
    ax = plt.gca()
    #polar projection
    m = Basemap(projection='npaeqd',boundinglat=30,lon_0=-100.,resolution='l')
    # Lambert projection
    #m = Basemap(width=8000000, height=8000000, resolution='l', projection='lcc',\
     #        lat_0=60,lon_0=-100.)
    m.drawcoastlines()
    m.drawparallels(np.arange(-80.,81,20.),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1],fontsize=10)

    x,y =m(grid[:,7],grid[:,6])
    sc = m.scatter(x,y,s=25,c=z,marker='.',cmap=cm.jet,alpha=0.9,edgecolors='none',vmin=min(z),vmax=max(z))
    #sc = m.scatter(x,y,s=abs(z)/300,c=z/300,marker=',',cmap=cm.jet,alpha=0.9,edgecolors='none')
    plt.title(title)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cb1 = plt.colorbar(sc,cax=cax)
    if col == 11 or col == 12:
        cb1.set_label("mA/m",fontsize=18)
    else:
        cb1.set_label("A",fontsize=18)
    plt.savefig(filename,bbox_inches='tight',pad_inches=0.2)
    #plt.show()

def filter_grid(grid,col,high,low):
    high_idx = np.where(grid[:,col]<high)[0]
    high_grid = grid[high_idx,:]
    low_idx = np.where(high_grid[:,col]>low)[0]
    fil_grid = high_grid[low_idx,:]

    return fil_grid

asc_grid = np.loadtxt('SECS_and_EICS_GRF_asc.txt')
des_grid = np.loadtxt('SECS_and_EICS_GRF_des.txt')

#Ascending
#Z: -30000:30000
#X: -15000:15000
#Y: -15000"15000

#Descending
#X: -15000:15000
#Y: -15000:15000
#Z: -35000:35000

asc_grid_x = filter_grid(asc_grid,11,15000,-15000)
asc_grid_y = filter_grid(asc_grid,12,15000,-15000)
asc_grid_z = filter_grid(asc_grid,13,30000,-30000)
des_grid_x = filter_grid(des_grid,11,15000,-15000)
des_grid_y = filter_grid(des_grid,12,15000,-15000)
des_grid_z = filter_grid(des_grid,13,30000,-30000)

polar_plot(asc_grid_x,11,'EICS Along-track in GRF (Ascending)','EICS_X_GRF_asc.png')
polar_plot(asc_grid_y,12,'EICS Cross-track in GRF (Ascending)','EICS_Y_GRF_asc.png')
polar_plot(asc_grid_z,13,'EICS Radial-track in GRF (Ascending)','EICS_Z_GRF_asc.png')
polar_plot(des_grid_x,11,'EICS Along-track in GRF (Descending)','EICS_X_GRF_des.png')
polar_plot(des_grid_y,12,'EICS Cross-track in GRF (Descending)','EICS_Y_GRF_des.png')
polar_plot(des_grid_z,13,'EICS Radial-track in GRF (Descending)','EICS_Z_GRF_des.png')



'''plt.plot(new_grid[:,14],new_grid[:,11],'.')
plt.title('EICS v component GRF Ascending Track Trace')
plt.ylabel('mA/m')
plt.show()
#plt.savefig('SECS_GRF_asc_trace.png',bbox_inches='tight',pad_inches=0.2)'''