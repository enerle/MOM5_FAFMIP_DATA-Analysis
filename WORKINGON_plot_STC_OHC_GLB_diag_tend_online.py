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

#t = np.arange(0,70)
#wt = [None]*len(t)

#for i in t:
#    if t[i] < 10: 
#        wt[i] = 0.1*t[i]
#    elif t[i] < 60 and t[i] >= 10:
#        wt[i] = 1
#    elif t[i] >= 60:
#        wt[i] = 0.1*(70-t[i])

#tyear = 365.25 * 24.0 * 3600.0
#dt = np.ones(len(t))*tyear

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    temptend[i]          = np.mean(file.variables['TEMPTEND_TOT'][61:70])*yt
    advection[i]         = np.mean(file.variables['ADVECTION_TOT'][61:70])*yt
    submeso[i]           = np.mean(file.variables['SUBMESO_TOT'][61:70])*yt
    neutral_gm[i]        = np.mean(file.variables['NEUTRAL_GM_TOT'][61:70])*yt
    diapycnal_mix[i]     = np.mean(file.variables['VDIFFUSE_DIFF_CBT_TOT'][61:70])*yt
    isopycnal_mix[i]     = np.mean(file.variables['NEUTRAL_DIFFUSION_TOT'][61:70])*yt
    sw_heat[i]           = np.mean(file.variables['SWH_TOT'][61:70])*yt

    temptend_stc[i]      = np.mean(file.variables['TEMPTEND_STC'][61:70])*yt
    advection_stc[i]     = np.mean(file.variables['ADVECTION_STC'][61:70])*yt
    submeso_stc[i]       = np.mean(file.variables['SUBMESO_STC'][61:70])*yt
    neutral_gm_stc[i]    = np.mean(file.variables['NEUTRAL_GM_STC'][61:70])*yt
    diapycnal_mix_stc[i] = np.mean(file.variables['VDIFFUSE_DIFF_CBT_STC'][61:70])*yt
    isopycnal_mix_stc[i] = np.mean(file.variables['NEUTRAL_DIFFUSION_STC'][61:70])*yt
    sw_heat_stc[i]       = np.mean(file.variables['SWH_STC'][61:70])*yt

    temptend_int[i]      = np.mean(file.variables['TEMPTEND_INT'][61:70])*yt
    advection_int[i]     = np.mean(file.variables['ADVECTION_INT'][61:70])*yt
    submeso_int[i]       = np.mean(file.variables['SUBMESO_INT'][61:70])*yt
    neutral_gm_int[i]    = np.mean(file.variables['NEUTRAL_GM_INT'][61:70])*yt
    diapycnal_mix_int[i] = np.mean(file.variables['VDIFFUSE_DIFF_CBT_INT'][61:70])*yt
    isopycnal_mix_int[i] = np.mean(file.variables['NEUTRAL_DIFFUSION_INT'][61:70])*yt
    sw_heat_int[i]       = np.mean(file.variables['SWH_INT'][61:70])*yt
    file.close()

for i in range(len(filename)):
    residual[i]   = advection[i] + submeso[i] + neutral_gm[i]
    eddy[i]       =                submeso[i] + neutral_gm[i] 
    resolved[i]   = residual[i]  - eddy[i]
    total[i]      = resolved[i]  + eddy[i] +  isopycnal_mix[i] + diapycnal_mix[i] + sw_heat[i]
    remaining[i]  = total[i]     - temptend[i] 
    dia_swh[i]    = diapycnal_mix[i] + sw_heat[i]
    
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

colors = [[0,0,0],[1,0,0],[1,.5,.5],[1,.95,0],[0,0,1],[.5,.5,1],[.7,.7,.7],[1,1,1],[1,1,1]]
labels = ["net","resolved","eddy","residual","isopycnal","diapycnal"]

v = [-0.4,0.4] #this is for the description

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):
    ax = fig.add_subplot(3,1,i+1)

    ax.plot(1.0,temptend[i]-temptend[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0]) #net
    ax.plot(0.8,resolved[i]-resolved[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1]) #resolved
    ax.plot(0.8,eddy[i]-eddy[-1],                          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2]) #eddy
    ax.plot(0.8,residual[i]-residual[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3]) #residual
    ax.plot(1.2,isopycnal_mix[i]-isopycnal_mix[-1],        marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4]) #isopycnal
    ax.plot(1.2,dia_swh[i]-dia_swh[-1],                    marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5]) #diapycnal 

    ax.plot(3.0,temptend_stc[i]-temptend_stc[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(2.8,resolved_stc[i]-resolved_stc[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(2.8,eddy_stc[i]-eddy_stc[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
    ax.plot(2.8,residual_stc[i]-residual_stc[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
    ax.plot(3.2,isopycnal_mix_stc[i]-isopycnal_mix_stc[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
    ax.plot(3.2,dia_swh_stc[i]-dia_swh_stc[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5]) 

    ax.plot(5.0,temptend_int[i]-temptend_int[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0],label=labels[0])
    ax.plot(4.8,resolved_int[i]-resolved_int[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1],label=labels[1])
    ax.plot(4.8,eddy_int[i]-eddy_int[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2],label=labels[2])
    ax.plot(4.8,residual_int[i]-residual_int[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3],label=labels[3])
    ax.plot(5.2,isopycnal_mix_int[i]-isopycnal_mix_int[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4],label=labels[4])
    ax.plot(5.2,dia_swh_int[i]-dia_swh_int[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5],label=labels[5]) 

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
    
    if i==0: ax.legend(loc=1,ncol=3,fontsize=10);

    ax.set_ylabel("$[PW]$",fontsize=16)
    plt.ylim((v))
    
    plt.title(exp[i],style='normal',fontsize=16)
    plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
    plt.xticks([0,1,2,3,4,5,6],[])

plt.xticks([0,1,2,3,4,5,6],["","Total","","Overturn","","Interior",""],fontsize=16,style='normal')
#plt.show()
#plt.savefig('STC_OHC_GLB_diag_tend_online.png',transparent = False, bbox_inches='tight',dpi=300)

##only control

v = [-4,4] #this is for the description

fig = plt.figure(3)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(3,1,1)

ax.plot(1.0,temptend[-1],         marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0]) #net
ax.plot(0.8,resolved[-1],         marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1]) #resolved
ax.plot(0.8,eddy[-1],             marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2]) #eddy
ax.plot(0.8,residual[-1],         marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3]) #residual
ax.plot(1.2,isopycnal_mix[-1],    marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4]) #isopycnal
ax.plot(1.2,dia_swh[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5]) #diapycnal 

ax.plot(3.0,temptend_stc[-1],     marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
ax.plot(2.8,resolved_stc[-1],     marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
ax.plot(2.8,eddy_stc[-1],         marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
ax.plot(2.8,residual_stc[-1],     marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
ax.plot(3.2,isopycnal_mix_stc[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
ax.plot(3.2,dia_swh_stc[-1]      ,marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])

ax.plot(5.0,temptend_int[-1],     marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0],label=labels[0])
ax.plot(4.8,resolved_int[-1],     marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1],label=labels[1])
ax.plot(4.8,eddy_int[-1],         marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2],label=labels[2])
ax.plot(4.8,residual_int[-1],     marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3],label=labels[3])
ax.plot(5.2,isopycnal_mix_int[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4],label=labels[4])
ax.plot(5.2,dia_swh_int[-1],      marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5],label=labels[5])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.legend(loc=4,ncol=2,fontsize=9);

ax.set_ylabel("$[PW]$",fontsize=16)
plt.ylim((v))

#plt.title(exp[-1],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6],[])

plt.xticks([0,1,2,3,4,5,6],["","Total","","Overturn","","Interior",""],fontsize=16,style='normal')
plt.show()
#plt.savefig('STC_OHC_GLB_diag_tend_online_CTL.png',transparent = False, bbox_inches='tight',dpi=300)

