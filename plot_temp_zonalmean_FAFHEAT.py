#
import sys
import os
import numpy as np
import numpy.ma as ma
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/DATA'
exp = ["$T_A^{'}$","$T_R^{'}$"]

filename = ['added_zonalmean_FAFHEAT.nc','redist_zonalmean_FAFHEAT.nc']

temp_zonal = [None]*len(exp)
LAT        = [None]*len(exp)
LAT2       = [None]*len(exp)
DEPTH      = [None]*len(exp)
DEPTH2     = [None]*len(exp)

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]        = file.variables['YT_OCEAN'][:]
    DEPTH[i]      = file.variables['ST_OCEAN'][:]
    temp_zonal[i] = np.squeeze(file.variables['TEMP_ZONALMEAN'][:,:])
    file.close()

#------------------------PLOTTING
#rc('text',usetex=True)
rc('figure', figsize=(11.69,8.27)) 

cmap2 = cmocean.cm.balance
cmap2.set_bad(color = '0.5', alpha = None)

kmin = -3.0; kmax = 3.0
clevs = [-3.0,-2.0,-1.5,-1.0,-0.5,-0.2,-0.1,0.1,0.2,0.5,1.0,1.5,2.0,3.0]

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)):

    [LAT2[i],DEPTH2[i]] = np.meshgrid(LAT[i],DEPTH[i])
    ax = fig.add_subplot(3,2,i+1)
 
    cs1 = plt.contourf(LAT2[i],DEPTH2[i],temp_zonal[i],levels=clevs,cmap=cmap2,extend='both')

    plt.clim(kmin,kmax)
    plt.title('%s' % (exp[i]),fontsize=16,color='k')
       
    ##-----------for beauty
    if (i>=0):
        plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=12)
    else:
        plt.xticks([-90,-60,-30,0,30,60,90],[])
    if (i==0 or i==2 or i==4):
        plt.yticks([0,1000,2000,3000,4000,5000],[0,1000,2000,3000,4000,5000],fontsize=12)
        ax.set_ylabel('Depth (m)',fontsize=14)
    else:
        plt.yticks([0,1000,2000,3000,4000,5000],[])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
    ##-----------

    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

#Changes in colorbar
cbaxes = fig.add_axes([0.3, 0.6, 0.4, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs1,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal",fraction=.1)
cbar.ax.tick_params(labelsize=12)
cbar.ax.set_yticklabels([-3.0,-2.0,-1.5,-1.0,-0.5,-0.2,-0.1,0.1,0.2,0.5,1.0,1.5,2.0,3.0])
cbar.ax.set_title('[K]',fontsize=12,color='k')

#plt.show()
plt.savefig('./Figures/temp_FAFHEAT_zonalmean.png',transparent = True, bbox_inches='tight',dpi=600)
