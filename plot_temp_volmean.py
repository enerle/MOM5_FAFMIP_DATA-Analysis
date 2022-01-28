import sys
import os
import numpy as np
import cmocean
#import matplotlib.pyplot as plt
import matplotlib  as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/DATA'

exp       = ["Stress","Water","Heat","All","flux-only"] 
filename  = ["temp_volmean_FAFSTRESS.nc","temp_volmean_FAFWATER.nc","temp_volmean_FAFHEAT-plus.nc","temp_volmean_FAFALL.nc","temp_volmean_flux-only.nc"]

#exp2      = ["$T_A^{'}$","$T_R^{'}$"]
exp2      = ["TA","TR"]
filename2 = ["added_volmean_FAFHEAT.nc","redist_volmean_FAFHEAT.nc"]

temp = [None]*len(filename)
temp2 = [None]*len(filename)
time = [None]*len(filename)
time2 = [None]*len(filename)

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename)):  
    fn = os.path.join(datadir,filename[i]) 
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time[i]   = file.variables['TIME'][:]/365-2188
    temp[i]   = file.variables['TEMP_VOLMEAN'][:]
    file.close()

for i in range(len(filename2)):
    fn = os.path.join(datadir,filename2[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time2[i]   = file.variables['TIME'][:]/365-2188
    temp2[i]   = file.variables['TEMP_VOLMEAN'][:]
    file.close()

##-----------------------Plot time series of change in temperature
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

colors = ['black','blue','red','green']
styles = ['solid','solid','solid','solid']

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax  = fig.add_subplot(2,2,1)

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line

for i in range(len(filename)-1):
    ax.plot(time[i],temp[i]-temp[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

plt.yticks([-.1,0,.1,.2,.3,.4],[-.1,0,.1,.2,.3,.4])

ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    
ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('[K]',fontsize=16)
ax.legend(loc=2,fontsize=14)
ax.axis([0,70,-.1,.4])

plt.yticks(fontsize=16)
plt.xticks(fontsize=16)

##-----figure just for fafheat
colors2 = ['red','blue']

ax = fig.add_subplot(2,2,2)

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line

for i in range(len(exp2)):
    ax.plot(time2[i],temp2[i],color=colors2[i],linestyle='solid',linewidth=2.0,label=exp2[i])

#ax.plot(time2[i],temp2[0]+temp2[1],color='gray',linestyle='solid',linewidth=2.0,label='added plus redist')
ax.plot(time2[i],temp[2]-temp[-1],color='black',linestyle='solid',linewidth=2.0,label='total')

plt.yticks([-.1,0,.1,.2,.3,.4],[])

ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

ax.set_xlabel('Time [years]',fontsize=16,position=[-.05,0,0,0])
ax.legend(loc=2,fontsize=14)
ax.axis([0,70,-.1,.4])

plt.yticks(fontsize=16)
plt.xticks(fontsize=16)

#plt.show()
plt.savefig('./Figures/temp_FAFHEAT-plus_volmean.png',transparent = True, bbox_inches='tight',dpi=600)


#temperature change in terms of percentage
##-----------------------Plot time series of change in temperature

fig = plt.figure(3)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax  = fig.add_subplot(2,2,1)

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line

for i in range(len(filename)-1):
    ax.plot(time[i],((temp[i]-temp[-1])/temp[-1])*100,color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

#plt.yticks([-.1,0,.1,.2,.3,.4],[-.1,0,.1,.2,.3,.4])

ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('[K]',fontsize=16)
ax.legend(loc=2,fontsize=14)
ax.axis([0,70,-1,10])

plt.yticks(fontsize=16)
plt.xticks(fontsize=16)

#plt.show()
plt.savefig('./Figures/temp_FAFHEAT-plus_volmean_percentage.png',transparent = True, bbox_inches='tight',dpi=600)
