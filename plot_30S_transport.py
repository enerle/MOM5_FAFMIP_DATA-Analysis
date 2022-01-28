import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/DATA'

exp      = ["Stress","Water","Heat","All","flux-only"]

filename = ["ty_trans_30S_FAFSTRESS.nc","ty_trans_30S_FAFWATER.nc","ty_trans_30S_FAFHEAT.nc","ty_trans_30S_FAFALL.nc","ty_trans_30S_flux-only.nc"]

trans_30S = [None]*len(exp)
depth     = [None]*len(exp)

for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    depth[i]     = file.variables['ST_OCEAN'][:]
    trans_30S[i] = file.variables['TRANS_30S'][:,:]
    file.close()

#------------------------PLOTTING
#====================================================
colors = ['black','blue','red','red','green','gray']
styles = ['solid','solid','solid','dashed','solid','solid']

#rc('text', usetex=True)

rc('figure', figsize=(8.27,6))

fig = plt.figure(1)
ax = fig.add_subplot(1,2,1)

for i in range(len(exp)):
    ax.plot(trans_30S[i],depth[i],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

ax.set_xlabel('Sv',fontsize=16)
ax.legend(loc=4,fontsize=16)

plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([-5,0,5,10,15,20],['-5','0','5','10','15','20'],fontsize=16)
ax.set_ylim(0,5000)
ax.axis([-5,20,0,5000])
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis
####

ax = fig.add_subplot(1,2,2)

for i in range(len(exp)-1):
    ax.plot(trans_30S[i]-trans_30S[-1],depth[i],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

ax.set_xlabel('Sv',fontsize=16)

plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.yticks([0,1000,2000,3000,4000],[])
ax.set_ylim(0,5000)
ax.axis([-5,5,0,5000])
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis
####

#plt.show()
plt.savefig('./Figures/30S_transport.png',transparent = True, bbox_inches='tight',dpi=600)
