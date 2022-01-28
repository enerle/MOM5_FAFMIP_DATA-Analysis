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
exp = ["SST","SSS"]
filename  = ['SST_SSS_Blaker_flux-only.nc','SST_SSS_Blaker_control.nc']

SST     = [None]*len(exp)
SSS     = [None]*len(exp)
SSTmean = [None]*len(exp)
SSSmean = [None]*len(exp)
LON     = [None]*len(exp)
LON2    = [None]*len(exp)
LAT     = [None]*len(exp)
LAT2    = [None]*len(exp)

#---> Get the Data
for i in range(len(exp)):
    fn = os.path.join(datadir,filename[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    LON[i]   = file.variables['XT_OCEAN'][:]
    LAT[i]   = file.variables['YT_OCEAN'][:]
    SST[i]   = file.variables['SST'][:,:]
    SSS[i]   = file.variables['SSS'][:,:]
    file.close()

for i in range(len(exp)):
    SSTmean[i] = np.ma.average(SST[i],axis=(1,0))
    SSSmean[i] = np.ma.average(SSS[i],axis=(1,0))

#------------------------PLOTTING
#======================================================================
fontbig   = 20
fontaxis  = 16
fonttitle = 10

letter = ["(a)","(b)","(c)","(d)","(e)","(f)","(h)","(g)"]
colors = ['green','red','red','black','blue']
styles = ['solid','dashed','solid','solid','solid']

rc('figure', figsize=(11.69,8.27))
cmap2 = cmocean.cm.balance
cmap2.set_bad(color = '0.7', alpha = None)

kmin = -2
kmax = 2
clevs = [-1,-.8,-.6,-.4,-.2,0,.2,.4,.6,.8,1]

rc('figure', figsize=(11.69,8.27))

fig = plt.figure(1)
[LON2[0],LAT2[0]] = np.meshgrid(LON[0],LAT[0])
SSTbias=SSTmean[1]-SSTmean[0]

ax  = fig.add_subplot(4,2,1)
cs  = plt.pcolormesh(LON2[0],LAT2[0],SSTbias,shading='flat',cmap=cmap2)
cs1 = plt.contourf(LON2[0],LAT2[0],SSTbias,levels=clevs,cmap=cmap2,extend='both')

plt.clim(kmin,kmax)
plt.title('%s %s' % (letter[0],exp[0]),fontsize=12,color='k')
plt.yticks(fontsize=fonttitle)
ax.tick_params(direction='out')
plt.yticks([-75,-50,-25,0,25,50,75],['75S','50S','25S','0','25N','50N','75N'])
cbar = plt.colorbar(cs1,ticks=clevs,extend='both',orientation='vertical')
cbar.ax.tick_params(labelsize=10)
cbar.ax.set_yticklabels(['-1','-.8','-.6','-.4','-.2','0','.2','.4','.6','.8','1'])
    
###################
SSSbias=SSSmean[1]-SSSmean[0]

ax  = fig.add_subplot(4,2,2)
cs  = plt.pcolormesh(LON2[0],LAT2[0],SSSbias,shading='flat',cmap=cmap2)
cs1 = plt.contourf(LON2[0],LAT2[0],SSSbias,levels=clevs,cmap=cmap2,extend='both')

plt.clim(kmin,kmax)
plt.title('%s %s' % (letter[1],exp[1]),fontsize=12,color='k')
plt.yticks(fontsize=fonttitle)
ax.tick_params(direction='out')
plt.yticks([-75,-50,-25,0,25,50,75],['75S','50S','25S','0','25N','50N','75N'])
cbar = plt.colorbar(cs1,ticks=clevs,extend='both',orientation='vertical')
cbar.ax.tick_params(labelsize=10)
cbar.ax.set_yticklabels(['-1','-.8','-.6','-.4','-.2','0','.2','.4','.6','.8','1'])

#plt.show()
plt.savefig('./Figures/SST_SSS_control-bias.eps',format='eps',transparent = True)
