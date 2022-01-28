import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/TEMP-tendency/DATA_vInt_MLD_BSO'

exp      = ["Stress","Water","Heat","flux-only"]
filename = ["STC_temptend_FAFSTRESS_GLB.nc","STC_temptend_FAFWATER_GLB.nc","STC_temptend_FAFHEAT_GLB.nc","STC_temptend_flux-only_GLB.nc"]
        
time                  = [None]*len(filename)
temptend              = [None]*len(filename)
advection             = [None]*len(filename)
submeso               = [None]*len(filename)
neutral_gm            = [None]*len(filename)
diapycnal_mix         = [None]*len(filename)
isopycnal_mix         = [None]*len(filename)
sw_heat               = [None]*len(filename)
residual              = [None]*len(filename)
eddy                  = [None]*len(filename)
resolved              = [None]*len(filename)
total                 = [None]*len(filename)
remaining             = [None]*len(filename)
dia_swh               = [None]*len(filename)

temptend_stc          = [None]*len(filename)
advection_stc         = [None]*len(filename)
submeso_stc           = [None]*len(filename)
neutral_gm_stc        = [None]*len(filename)
diapycnal_mix_stc     = [None]*len(filename)
isopycnal_mix_stc     = [None]*len(filename)
sw_heat_stc           = [None]*len(filename)
residual_stc          = [None]*len(filename)
eddy_stc              = [None]*len(filename)
resolved_stc          = [None]*len(filename)
total_stc             = [None]*len(filename)
remaining_stc         = [None]*len(filename)
dia_swh_stc           = [None]*len(filename)

temptend_int          = [None]*len(filename)
advection_int         = [None]*len(filename)
submeso_int           = [None]*len(filename)
neutral_gm_int        = [None]*len(filename)
diapycnal_mix_int     = [None]*len(filename)
isopycnal_mix_int     = [None]*len(filename)
sw_heat_int           = [None]*len(filename)
residual_int          = [None]*len(filename)
eddy_int              = [None]*len(filename)
resolved_int          = [None]*len(filename)
total_int             = [None]*len(filename)
remaining_int         = [None]*len(filename)
dia_swh_int           = [None]*len(filename)

yt = 1e-15 #PW

t = np.arange(0,70)
wt = [None]*len(t)

wt = 1 

#since the tendencies are standarized with time differential, we have ZJoules instead of ZWatts

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time[i]              = file.variables['TIME'][:]/365-2188
    temptend[i]          = (wt*file.variables['TEMPTEND_TOT'][:])*yt
    advection[i]         = (wt*file.variables['ADVECTION_TOT'][:])*yt
    submeso[i]           = (wt*file.variables['SUBMESO_TOT'][:])*yt
    neutral_gm[i]        = (wt*file.variables['NEUTRAL_GM_TOT'][:])*yt
    diapycnal_mix[i]     = (wt*file.variables['VDIFFUSE_DIFF_CBT_TOT'][:])*yt
    isopycnal_mix[i]     = (wt*file.variables['NEUTRAL_DIFFUSION_TOT'][:])*yt
    sw_heat[i]           = (wt*file.variables['SWH_TOT'][:])*yt

    temptend_stc[i]      = (wt*file.variables['TEMPTEND_STC'][:])*yt
    advection_stc[i]     = (wt*file.variables['ADVECTION_STC'][:])*yt
    submeso_stc[i]       = (wt*file.variables['SUBMESO_STC'][:])*yt
    neutral_gm_stc[i]    = (wt*file.variables['NEUTRAL_GM_STC'][:])*yt
    diapycnal_mix_stc[i] = (wt*file.variables['VDIFFUSE_DIFF_CBT_STC'][:])*yt
    isopycnal_mix_stc[i] = (wt*file.variables['NEUTRAL_DIFFUSION_STC'][:])*yt
    sw_heat_stc[i]       = (wt*file.variables['SWH_STC'][:])*yt

    temptend_int[i]      = (wt*file.variables['TEMPTEND_INT'][:])*yt
    advection_int[i]     = (wt*file.variables['ADVECTION_INT'][:])*yt
    submeso_int[i]       = (wt*file.variables['SUBMESO_INT'][:])*yt
    neutral_gm_int[i]    = (wt*file.variables['NEUTRAL_GM_INT'][:])*yt
    diapycnal_mix_int[i] = (wt*file.variables['VDIFFUSE_DIFF_CBT_INT'][:])*yt
    isopycnal_mix_int[i] = (wt*file.variables['NEUTRAL_DIFFUSION_INT'][:])*yt
    sw_heat_int[i]       = (wt*file.variables['SWH_INT'][:])*yt
    file.close()

for i in range(len(filename)):
    residual[i]   = advection[i] + submeso[i] + neutral_gm[i]
    eddy[i]       =                submeso[i] + neutral_gm[i] 
    resolved[i]   = residual[i]  - eddy[i]
    total[i]      = resolved[i]  + eddy[i] +  isopycnal_mix[i] + diapycnal_mix[i] + sw_heat[i]
    remaining[i]  = total[i]     - temptend[i] 
    dia_swh[i]    = diapycnal_mix_int[i] + sw_heat[i]

    residual_stc[i]   = advection_stc[i] + submeso_stc[i] + neutral_gm_stc[i]
    eddy_stc[i]       =                    submeso_stc[i] + neutral_gm_stc[i]
    resolved_stc[i]   = residual_stc[i]  - eddy_stc[i]
    total_stc[i]      = resolved_stc[i]  + eddy_stc[i] +  isopycnal_mix_stc[i] + diapycnal_mix_stc[i] + sw_heat_stc[i]
    remaining_stc[i]  = total_stc[i]     - temptend_stc[i]
    dia_swh_stc[i]    = diapycnal_mix_stc[i] + sw_heat_stc[i]

    residual_int[i]   = advection_int[i] + submeso_int[i] + neutral_gm_int[i]
    eddy_int[i]       =                    submeso_int[i] + neutral_gm_int[i]
    resolved_int[i]   = residual_int[i]  - eddy_int[i]
    total_int[i]      = resolved_int[i]  + eddy_int[i] +  isopycnal_mix_int[i] + diapycnal_mix_int[i] + sw_heat_int[i]
    remaining_int[i]  = total_int[i]     - temptend_int[i]
    dia_swh_int[i]    = diapycnal_mix_int[i] + sw_heat_int[i]

###
#rc('text', usetex=True)
rc('figure', figsize=(8.27,11.69))

colors = [[0,0,0],[1,0,0],[1,.5,.5],[1,.95,0],[0,0,1],[.5,.5,1],[0,1,.6],[.7,.7,.7],[1,1,1],[1,1,1]]
labels = ["net","resolved","eddy","residual","isopycnal","dia+swp","penetrative","all","net-all"]

v = [-.4,.4] #this is for the description

#fig = plt.figure(1)
#fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):

    fig = plt.figure(i+1)
    fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

    ax = fig.add_subplot(3,1,1)
    ax.plot(time[i],temptend[i]-temptend[-1],          linewidth=1.5,color=colors[0],label=labels[0]) #net
    ax.plot(time[i],resolved[i]-resolved[-1],          linewidth=1.5,color=colors[1],label=labels[1]) #resolved
    ax.plot(time[i],eddy[i]-eddy[-1],                  linewidth=1.5,color=colors[2],label=labels[2]) #eddy
    ax.plot(time[i],residual[i]-residual[-1],          linewidth=1.5,color=colors[3],label=labels[3]) #residual
    ax.plot(time[i],isopycnal_mix[i]-isopycnal_mix[-1],linewidth=1.5,color=colors[4],label=labels[4]) #isopycnal
    ax.plot(time[i],dia_swh[i]-dia_swh[-1],            linewidth=1.5,color=colors[5],label=labels[5]) #diapycnal 

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
    
    ax.set_ylabel("$[PW]$",fontsize=16)
    ax.axis([0,70,-.4,.4])
    
    plt.title('Total',style='normal',fontsize=16)
    plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
    plt.xticks([0,10,20,30,40,50,60,70],[])

    ax = fig.add_subplot(3,1,2)
    ax.plot(time[i],temptend_stc[i]-temptend_stc[-1],          linewidth=1.5,color=colors[0],label=labels[0]) #net
    ax.plot(time[i],resolved_stc[i]-resolved_stc[-1],          linewidth=1.5,color=colors[1],label=labels[1]) #resolved
    ax.plot(time[i],eddy_stc[i]-eddy_stc[-1],                  linewidth=1.5,color=colors[2],label=labels[2]) #eddy
    ax.plot(time[i],residual_stc[i]-residual_stc[-1],          linewidth=1.5,color=colors[3],label=labels[3]) #residual
    ax.plot(time[i],isopycnal_mix_stc[i]-isopycnal_mix_stc[-1],linewidth=1.5,color=colors[4],label=labels[4]) #isopycnal
    ax.plot(time[i],dia_swh_stc[i]-dia_swh_stc[-1],            linewidth=1.5,color=colors[5],label=labels[5]) #diapycnal 

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    ax.set_ylabel("$[PW]$",fontsize=16)
    ax.axis([0,70,-.4,.4])

    plt.title('Overturn',style='normal',fontsize=16)
    plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
    plt.xticks([0,10,20,30,40,50,60,70],[])

    ax = fig.add_subplot(3,1,3)
    ax.plot(time[i],temptend_int[i]-temptend_int[-1],          linewidth=1.5,color=colors[0],label=labels[0]) #net
    ax.plot(time[i],resolved_int[i]-resolved_int[-1],          linewidth=1.5,color=colors[1],label=labels[1]) #resolved
    ax.plot(time[i],eddy_int[i]-eddy_int[-1],                  linewidth=1.5,color=colors[2],label=labels[2]) #eddy
    ax.plot(time[i],residual_int[i]-residual_int[-1],          linewidth=1.5,color=colors[3],label=labels[3]) #residual
    ax.plot(time[i],isopycnal_mix_int[i]-isopycnal_mix_int[-1],linewidth=1.5,color=colors[4],label=labels[4]) #isopycnal
    ax.plot(time[i],dia_swh_int[i]-dia_swh_int[-1],            linewidth=1.5,color=colors[5],label=labels[5]) #diapycnal 

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    ax.legend(loc=4,ncol=3,fontsize=10);
    ax.axis([0,70,-.4,.4])

    ax.set_ylabel("$[PW]$",fontsize=16)

    plt.title('Interior',style='normal',fontsize=16)
    plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
    plt.xticks([0,10,20,30,40,50,60,70],[])

    ax.set_xlabel("Time [years]",fontsize=16)
    plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70],fontsize=16,style='normal')
    
    #plt.show()
    #plt.savefig('STC_OHC_GLB_diag_tend_online_time_' + exp[i] + '.png',transparent = False, bbox_inches='tight',dpi=300)

####control

v = [-4,4] #this is for the description

i=-1
fig = plt.figure(4)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(3,1,1)
ax.plot(time[i],temptend[-1],     linewidth=1.5,color=colors[0],label=labels[0]) #net
ax.plot(time[i],resolved[-1],     linewidth=1.5,color=colors[1],label=labels[1]) #resolved
ax.plot(time[i],eddy[-1],         linewidth=1.5,color=colors[2],label=labels[2]) #eddy
ax.plot(time[i],residual[-1],     linewidth=1.5,color=colors[3],label=labels[3]) #residual
ax.plot(time[i],isopycnal_mix[-1],linewidth=1.5,color=colors[4],label=labels[4]) #isopycnal
ax.plot(time[i],dia_swh[-1],      linewidth=1.5,color=colors[5],label=labels[5]) #diapycnal 

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("$[PW]$",fontsize=16)
ax.axis([0,70,-4,4])

plt.title('Total',style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70],fontsize=16,style='normal')

ax = fig.add_subplot(3,1,2)
ax.plot(time[i],temptend_stc[-1],     linewidth=1.5,color=colors[0],label=labels[0]) #net
ax.plot(time[i],resolved_stc[-1],     linewidth=1.5,color=colors[1],label=labels[1]) #resolved
ax.plot(time[i],eddy_stc[-1],         linewidth=1.5,color=colors[2],label=labels[2]) #eddy
ax.plot(time[i],residual_stc[-1],     linewidth=1.5,color=colors[3],label=labels[3]) #residual
ax.plot(time[i],isopycnal_mix_stc[-1],linewidth=1.5,color=colors[4],label=labels[4]) #isopycnal
ax.plot(time[i],dia_swh_stc[-1],      linewidth=1.5,color=colors[5],label=labels[5]) #diapycnal 

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("$[PW]$",fontsize=16)
ax.axis([0,70,-4,4])

plt.title('Overturn',style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70],fontsize=16,style='normal')

ax = fig.add_subplot(3,1,3)
ax.plot(time[i],temptend_int[-1],     linewidth=1.5,color=colors[0],label=labels[0]) #net
ax.plot(time[i],resolved_int[-1],     linewidth=1.5,color=colors[1],label=labels[1]) #resolved
ax.plot(time[i],eddy_int[-1],         linewidth=1.5,color=colors[2],label=labels[2]) #eddy
ax.plot(time[i],residual_int[-1],     linewidth=1.5,color=colors[3],label=labels[3]) #residual
ax.plot(time[i],isopycnal_mix_int[-1],linewidth=1.5,color=colors[4],label=labels[4]) #isopycnal
ax.plot(time[i],dia_swh_int[-1],      linewidth=1.5,color=colors[5],label=labels[5]) #diapycnal 

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.legend(loc=4,ncol=3,fontsize=10);

ax.set_ylabel("$[PW]$",fontsize=16)
ax.axis([0,70,-4,4])

plt.title('Interior',style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)

ax.set_xlabel("Time [years]",fontsize=16)
plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70],fontsize=16,style='normal')

#plt.show()
#plt.savefig('STC_OHC_GLB_diag_tend_online_time_CTL.png',transparent = False, bbox_inches='tight',dpi=300)

v = [-0.05,0.2] #this is for the description
i=-1
fig = plt.figure(5)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(3,1,1)
ax.plot(time[i],temptend[-1],    linewidth=2,color='black',label='Total')
ax.plot(time[i],temptend_stc[-1],linewidth=2,color='red',label='Overturn')
ax.plot(time[i],temptend_int[-1],linewidth=2,color='blue',label='Interior')

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.legend(loc=2,ncol=1,fontsize=10);

ax.set_ylabel("$[PW]$",fontsize=16)
ax.axis([0,70,-0.05,0.2])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)

ax.set_xlabel("Time [years]",fontsize=16)
plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70],fontsize=16)
plt.yticks([-.05,0,.05,.10,.15,.20],[-.05,0,.05,.10,.15,.20],fontsize=16)

#plt.show()
#plt.savefig('STC_OHC_GLB_diag_tend_online_time_nettendency_CTL.png',transparent = False, bbox_inches='tight',dpi=300)

###solo nettendency

colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

#rc('text', usetex=True)
rc('figure', figsize=(8.27,11.69))

fig = plt.figure(6)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(3,1,1)
for i in range(len(exp)-1):
    ax.plot(time[i],temptend[i]-temptend[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$[PW]$',fontsize=16)
ax.legend(loc=2,fontsize=16)
ax.axis([0,70,-.2,.6])

plt.title('Total')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([0,10,20,30,40,50,60,70],[],fontsize=16)
####

ax = fig.add_subplot(3,1,2)
for i in range(len(exp)-1):
    ax.plot(time[i],temptend_stc[i]-temptend_stc[-1],color=colors[i],linestyle=styles[i],linewidth=2.0)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$[PW]$',fontsize=16)
ax.axis([0,70,-.2,.6])

plt.title('Overturn')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([0,10,20,30,40,50,60,70],[],fontsize=16)

ax = fig.add_subplot(3,1,3)
for i in range(len(exp)-1):
    ax.plot(time[i],temptend_int[i]-temptend_int[-1],color=colors[i],linestyle=styles[i],linewidth=2.0)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$[PW]$',fontsize=16)
ax.axis([0,70,-.2,.6])

plt.title('Interior')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70],fontsize=16)

plt.show()
#plt.savefig('STC_OHC_GLB_diag_tend_online_time_nettendency.png',transparent = False, bbox_inches='tight',dpi=300)
