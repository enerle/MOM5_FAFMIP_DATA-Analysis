import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/DATA'
dirout   = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/Figures'

exp      = ["Stress","Water","Heat","All","control"]
filename2 = ["MOC_FAFSTRESS.nc","MOC_FAFWATER.nc","MOC_FAFHEAT.nc","MOC_FAFALL.nc","MOC_flux-only.nc"]

time  = [None]*len(exp)

AMOC_41N = [None]*len(exp)
AMOC_26N = [None]*len(exp)
AMOC_30S = [None]*len(exp)
AABW     = [None]*len(exp)

#---> Get the AMOC
for i in range(len(exp)):  
    fn = os.path.join(datadir,filename2[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    time[i] = file.variables['TIME'][:]/365 -2188.0
    AMOC_41N[i] = file.variables['MOC_41N'][:]
    AMOC_26N[i] = file.variables['MOC_26N'][:]
    AMOC_30S[i] = file.variables['MOC_30S'][:]
    AABW[i]    = file.variables['AABW'][:]
    file.close()

##------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

##------AMOC
fig = plt.figure(1)
fig.subplots_adjust(top=.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(2,2,1)
for i in range(len(exp)-1):
    ax.plot(time[i],AMOC_41N[i]-AMOC_41N[-1][0],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_xlabel("Time [years]",fontsize=16)
ax.set_ylabel("$\Delta \Psi$ [Sv]",fontsize=16)
ax.axis([0,70,-10,10])

plt.title('AMOC $41^o$N',fontsize=16,color='k')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks(np.arange(0,71,10),fontsize=16)
plt.yticks(np.arange(-10,11,2.5),fontsize=16)
###

#ax = fig.add_subplot(2,2,4)
ax = fig.add_subplot(2,2,2)
for i in range(len(exp)-1):
    ax.plot(time[i],AABW[i]-AABW[-1][0],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_xlabel("Time [years]",fontsize=16)
ax.legend(loc=4,ncol=2, fontsize=16)
ax.axis([0,70,-10,10])

plt.title('AABW $50^o$S',fontsize=16,color='k')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks(np.arange(0,71,10),fontsize=16)
plt.yticks(np.arange(-10,11,2.5),[],fontsize=16)
###

#plt.show()
plt.savefig('./Figures/MOC_AMOC_timeseries.png',transparent = True, bbox_inches='tight',dpi=600)

####next, is the same figure, the only difference is: 
####change is expressed as percentage in terms of the control
fig = plt.figure(2)
fig.subplots_adjust(top=.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(2,2,1)
for i in range(len(exp)-1):
    ax.plot(time[i],((AMOC_41N[i]-AMOC_41N[-1][0])/AMOC_41N[-1][0])*100,color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_xlabel("Time [years]",fontsize=16)
ax.set_ylabel("$\Delta \Psi$ [Sv]",fontsize=16)
ax.axis([1,70,-60,30])

plt.title('AMOC $41^o$N',fontsize=16,color='k')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks(np.arange(0,71,10),fontsize=16)
plt.yticks(np.arange(-60,31,10),fontsize=16)
###

#ax = fig.add_subplot(2,2,4)
ax = fig.add_subplot(2,2,2)
for i in range(len(exp)-1):
    ax.plot(time[i],((AABW[i]-AABW[-1][0])/AABW[-1][0])*100,color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_xlabel("Time [years]",fontsize=16)
ax.legend(loc=3,ncol=2, fontsize=16)
ax.axis([0,70,-60,20])

plt.title('AABW $50^o$S',fontsize=16,color='k')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks(np.arange(0,71,10),fontsize=16)
plt.yticks(np.arange(-60,31,10),[],fontsize=16)
###

#plt.show()
savefig('./Figures/MOC_AMOC_timeseries_percentege.png',transparent = True, bbox_inches='tight',dpi=600)

###################
##
## Control
##
###################

##------AMOC
fig = plt.figure(2)

ax = fig.add_subplot(2,2,1)
for i in range(len(exp)):
    ax.plot(time[i],AMOC_41N[i],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("$\Psi$ [Sv]",fontsize=16)
ax.axis([0,70,5,26])

plt.title('AMOC $41^o$N',fontsize=16,color='k')
plt.xticks(np.arange(0,71,10),[])
plt.yticks(np.arange(5,25,5),fontsize=16)
###

ax = fig.add_subplot(2,2,2)
for i in range(len(exp)):
    ax.plot(time[i],AMOC_26N[i],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis([0,70,5,26])

plt.title('AMOC $26^o$N',fontsize=16,color='k')
plt.xticks(np.arange(0,71,10),[],fontsize=16)
plt.yticks(np.arange(5,25,5),[],fontsize=16)
###

ax = fig.add_subplot(2,2,3)
for i in range(len(exp)):
    ax.plot(time[i],AMOC_30S[i],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_xlabel("Time [years]",fontsize=16)
ax.set_ylabel("$\Psi$ [Sv]",fontsize=16)
ax.axis([0,70,5,26])

plt.title('AMOC $30^o$S',fontsize=16,color='k')
plt.xticks(np.arange(0,71,10),fontsize=16)
plt.yticks(np.arange(5,25,5),fontsize=16)
###

ax = fig.add_subplot(2,2,4)
for i in range(len(exp)):
    ax.plot(time[i],-AABW[i],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_xlabel("Time [years]",fontsize=16)
ax.legend(loc=2,ncol=2, fontsize=16)
ax.axis([0,70,5,26])

plt.title('AABW $50^o$S',fontsize=16,color='k')
plt.xticks(np.arange(0,71,10),fontsize=16)
plt.yticks(np.arange(5,25,5),[],fontsize=16)
###

#plt.show()
#plt.savefig('./Figures/MOC_AMOC_timeseries_CTL.png',transparent = True, bbox_inches='tight',dpi=600)

#####
#####
#####

##
## SOLO Control
##

##------AMOC
fig = plt.figure(3)

ax = fig.add_subplot(2,2,1)
ax.plot(time[-1],AMOC_41N[-1],color='black',linestyle='solid',linewidth=2.0)

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("$\Psi$ [Sv]",fontsize=16)
ax.axis([0,70,5,26])

plt.title('AMOC $41^o$N',fontsize=16,color='k')
plt.xticks(np.arange(0,71,10),[])
plt.yticks(np.arange(5,25,5),fontsize=16)
###

ax = fig.add_subplot(2,2,2)
ax.plot(time[-1],AMOC_26N[-1],color='black',linestyle='solid',linewidth=2.0)

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis([0,70,5,26])

plt.title('AMOC $26^o$N',fontsize=16,color='k')
plt.xticks(np.arange(0,71,10),[],fontsize=16)
plt.yticks(np.arange(5,25,5),[],fontsize=16)
###

ax = fig.add_subplot(2,2,3)
ax.plot(time[-1],AMOC_30S[-1],color='black',linestyle='solid',linewidth=2.0)

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_xlabel("Time [years]",fontsize=16)
ax.set_ylabel("$\Psi$ [Sv]",fontsize=16)
ax.axis([0,70,5,26])

plt.title('AMOC $30^o$S',fontsize=16,color='k')
plt.xticks(np.arange(0,71,10),fontsize=16)
plt.yticks(np.arange(5,25,5),fontsize=16)
###

ax = fig.add_subplot(2,2,4)
ax.plot(time[-1],-AABW[-1],color='black',linestyle='solid',linewidth=2.0)

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_xlabel("Time [years]",fontsize=16)
ax.axis([0,70,5,26])

plt.title('AABW $50^o$S',fontsize=16,color='k')
plt.xticks(np.arange(0,71,10),fontsize=16)
plt.yticks(np.arange(5,25,5),[],fontsize=16)
###

#plt.show()
#plt.savefig('./Figures/MOC_AMOC_timeseries_SOLO_CTL.png',transparent = True, bbox_inches='tight',dpi=600)
