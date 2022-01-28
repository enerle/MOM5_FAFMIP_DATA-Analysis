import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/TEMP-tend/DATA/DATA_vInt27-50_latInt'
exp     = ["Global","Atlantic","Pacific","Indian","Indo-Pacific"]

filename_glb = ["heat_budget_flux-only_GLB_05S-05N.nc","heat_budget_flux-only_GLB_10S-10N.nc","heat_budget_flux-only_GLB_15S-15N.nc","heat_budget_flux-only_GLB_20S-20N.nc","heat_budget_flux-only_GLB_25S-25N.nc","heat_budget_flux-only_GLB_30S-30N.nc","heat_budget_flux-only_GLB_35S-35N.nc","heat_budget_flux-only_GLB_40S-40N.nc","heat_budget_flux-only_GLB_45S-45N.nc","heat_budget_flux-only_GLB_50S-50N.nc","heat_budget_flux-only_GLB_55S-55N.nc","heat_budget_flux-only_GLB_60S-60N.nc","heat_budget_flux-only_GLB.nc"]
filename_atl = ["heat_budget_flux-only_ATL_05S-05N.nc","heat_budget_flux-only_ATL_10S-10N.nc","heat_budget_flux-only_ATL_15S-15N.nc","heat_budget_flux-only_ATL_20S-20N.nc","heat_budget_flux-only_ATL_25S-25N.nc","heat_budget_flux-only_ATL_30S-30N.nc","heat_budget_flux-only_ATL_35S-35N.nc","heat_budget_flux-only_ATL_40S-40N.nc","heat_budget_flux-only_ATL_45S-45N.nc","heat_budget_flux-only_ATL_50S-50N.nc","heat_budget_flux-only_ATL_55S-55N.nc","heat_budget_flux-only_ATL_60S-60N.nc","heat_budget_flux-only_ATL.nc"]
filename_pac = ["heat_budget_flux-only_PAC_05S-05N.nc","heat_budget_flux-only_PAC_10S-10N.nc","heat_budget_flux-only_PAC_15S-15N.nc","heat_budget_flux-only_PAC_20S-20N.nc","heat_budget_flux-only_PAC_25S-25N.nc","heat_budget_flux-only_PAC_30S-30N.nc","heat_budget_flux-only_PAC_35S-35N.nc","heat_budget_flux-only_PAC_40S-40N.nc","heat_budget_flux-only_PAC_45S-45N.nc","heat_budget_flux-only_PAC_50S-50N.nc","heat_budget_flux-only_PAC_55S-55N.nc","heat_budget_flux-only_PAC_60S-60N.nc","heat_budget_flux-only_PAC.nc"]
filename_ind = ["heat_budget_flux-only_IND_05S-05N.nc","heat_budget_flux-only_IND_10S-10N.nc","heat_budget_flux-only_IND_15S-15N.nc","heat_budget_flux-only_IND_20S-20N.nc","heat_budget_flux-only_IND_25S-25N.nc","heat_budget_flux-only_IND_30S-30N.nc","heat_budget_flux-only_IND_35S-35N.nc","heat_budget_flux-only_IND_35S-35N.nc","heat_budget_flux-only_IND_35S-35N.nc","heat_budget_flux-only_IND_35S-35N.nc","heat_budget_flux-only_IND_35S-35N.nc","heat_budget_flux-only_IND_35S-35N.nc","heat_budget_flux-only_IND.nc"]
filename_ipa = ["heat_budget_flux-only_IPA_05S-05N.nc","heat_budget_flux-only_IPA_10S-10N.nc","heat_budget_flux-only_IPA_15S-15N.nc","heat_budget_flux-only_IPA_20S-20N.nc","heat_budget_flux-only_IPA_25S-25N.nc","heat_budget_flux-only_IPA_30S-30N.nc","heat_budget_flux-only_IPA_35S-35N.nc","heat_budget_flux-only_IPA_40S-40N.nc","heat_budget_flux-only_IPA_45S-45N.nc","heat_budget_flux-only_IPA_50S-50N.nc","heat_budget_flux-only_IPA_55S-55N.nc","heat_budget_flux-only_IPA_60S-60N.nc","heat_budget_flux-only_IPA.nc"]

time_glb              = [None]*len(filename_glb)
temptend_glb          = [None]*len(filename_glb)
advection_glb         = [None]*len(filename_glb)
submeso_glb           = [None]*len(filename_glb)
neutral_gm_glb        = [None]*len(filename_glb)
diapycnal_mix_glb     = [None]*len(filename_glb)
isopycnal_mix_glb     = [None]*len(filename_glb)
swh_glb               = [None]*len(filename_glb)
residual_glb          = [None]*len(filename_glb)
eddy_glb              = [None]*len(filename_glb)
resolved_glb          = [None]*len(filename_glb)
total_glb             = [None]*len(filename_glb)
remaining_glb         = [None]*len(filename_glb)
dia_swh_glb           = [None]*len(filename_glb)

time_atl              = [None]*len(filename_atl)
temptend_atl          = [None]*len(filename_atl)
advection_atl         = [None]*len(filename_atl)
submeso_atl           = [None]*len(filename_atl)
neutral_gm_atl        = [None]*len(filename_atl)
diapycnal_mix_atl     = [None]*len(filename_atl)
isopycnal_mix_atl     = [None]*len(filename_atl)
swh_atl               = [None]*len(filename_atl)
residual_atl          = [None]*len(filename_atl)
eddy_atl              = [None]*len(filename_atl)
resolved_atl          = [None]*len(filename_atl)
total_atl             = [None]*len(filename_atl)
remaining_atl         = [None]*len(filename_atl)
dia_swh_atl           = [None]*len(filename_atl)

time_ipa              = [None]*len(filename_ipa)
temptend_ipa          = [None]*len(filename_ipa)
advection_ipa         = [None]*len(filename_ipa)
submeso_ipa           = [None]*len(filename_ipa)
neutral_gm_ipa        = [None]*len(filename_ipa)
diapycnal_mix_ipa     = [None]*len(filename_ipa)
isopycnal_mix_ipa     = [None]*len(filename_ipa)
swh_ipa               = [None]*len(filename_ipa)
residual_ipa          = [None]*len(filename_ipa)
eddy_ipa              = [None]*len(filename_ipa)
resolved_ipa          = [None]*len(filename_ipa)
total_ipa             = [None]*len(filename_ipa)
remaining_ipa         = [None]*len(filename_ipa)
dia_swh_ipa           = [None]*len(filename_ipa)

time_pac              = [None]*len(filename_pac)
temptend_pac          = [None]*len(filename_pac)
advection_pac         = [None]*len(filename_pac)
submeso_pac           = [None]*len(filename_pac)
neutral_gm_pac        = [None]*len(filename_pac)
diapycnal_mix_pac     = [None]*len(filename_pac)
isopycnal_mix_pac     = [None]*len(filename_pac)
swh_pac               = [None]*len(filename_pac)
residual_pac          = [None]*len(filename_pac)
eddy_pac              = [None]*len(filename_pac)
resolved_pac          = [None]*len(filename_pac)
total_pac             = [None]*len(filename_pac)
remaining_pac         = [None]*len(filename_pac)
dia_swh_pac           = [None]*len(filename_pac)

time_ind              = [None]*len(filename_ind)
temptend_ind          = [None]*len(filename_ind)
advection_ind         = [None]*len(filename_ind)
submeso_ind           = [None]*len(filename_ind)
neutral_gm_ind        = [None]*len(filename_ind)
diapycnal_mix_ind     = [None]*len(filename_ind)
isopycnal_mix_ind     = [None]*len(filename_ind)
swh_ind               = [None]*len(filename_ind)
residual_ind          = [None]*len(filename_ind)
eddy_ind              = [None]*len(filename_ind)
resolved_ind          = [None]*len(filename_ind)
total_ind             = [None]*len(filename_ind)
remaining_ind         = [None]*len(filename_ind)
dia_swh_ind           = [None]*len(filename_ind)

###
### temp_tendendy = Cp*rho Int(dT/dt)dz  [W/m2]
###

#yt = 1e-9 #Giga
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
wt =1

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename_glb)):
    fn = os.path.join(datadir,filename_glb[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time_glb[i]              = file.variables['TIME'][:]/365-2188
    temptend_glb[i]          = np.mean(wt*file.variables['TEMPTEND'][61:70])*yt
    advection_glb[i]         = np.mean(wt*file.variables['ADVECTION'][61:70])*yt
    submeso_glb[i]           = np.mean(wt*file.variables['SUBMESO'][61:70])*yt
    neutral_gm_glb[i]        = np.mean(wt*file.variables['NEUTRAL_GM'][61:70])*yt
    diapycnal_mix_glb[i]     = np.mean(wt*file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt
    isopycnal_mix_glb[i]     = np.mean(wt*file.variables['NEUTRAL_DIFFUSION'][61:70])*yt
    swh_glb[i]               = np.mean(wt*file.variables['SWH'][61:70])*yt
    file.close()

for i in range(len(filename_glb)):
    residual_glb[i]   = advection_glb[i] + submeso_glb[i] + neutral_gm_glb[i]
    eddy_glb[i]       =                    submeso_glb[i] + neutral_gm_glb[i]
    resolved_glb[i]   = residual_glb[i]  - eddy_glb[i]
    dia_swh_glb[i]    = diapycnal_mix_glb[i] + swh_glb[i]
    total_glb[i]      = resolved_glb[i]  + eddy_glb[i]    + isopycnal_mix_glb[i] + diapycnal_mix_glb[i] + swh_glb[i]
    remaining_glb[i]  = total_glb[i]     - temptend_glb[i]

for i in range(len(filename_atl)):
    fn = os.path.join(datadir,filename_atl[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time_atl[i]              = file.variables['TIME'][:]/365-2188
    temptend_atl[i]          = np.mean(wt*file.variables['TEMPTEND'][61:70])*yt
    advection_atl[i]         = np.mean(wt*file.variables['ADVECTION'][61:70])*yt
    submeso_atl[i]           = np.mean(wt*file.variables['SUBMESO'][61:70])*yt
    neutral_gm_atl[i]        = np.mean(wt*file.variables['NEUTRAL_GM'][61:70])*yt
    diapycnal_mix_atl[i]     = np.mean(wt*file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt
    isopycnal_mix_atl[i]     = np.mean(wt*file.variables['NEUTRAL_DIFFUSION'][61:70])*yt
    swh_atl[i]               = np.mean(wt*file.variables['SWH'][61:70])*yt
    file.close()

for i in range(len(filename_atl)):
    residual_atl[i]   = advection_atl[i] + submeso_atl[i] + neutral_gm_atl[i]
    eddy_atl[i]       =                    submeso_atl[i] + neutral_gm_atl[i]
    resolved_atl[i]   = residual_atl[i]  - eddy_atl[i]
    dia_swh_atl[i]    = diapycnal_mix_atl[i] + swh_atl[i]
    total_atl[i]      = resolved_atl[i]  + eddy_atl[i]    + isopycnal_mix_atl[i] + diapycnal_mix_atl[i] + swh_atl[i]
    remaining_atl[i]  = total_atl[i]     - temptend_atl[i]

for i in range(len(filename_ipa)):
    fn = os.path.join(datadir,filename_ipa[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time_ipa[i]              = file.variables['TIME'][:]/365-2188
    temptend_ipa[i]          = np.mean(wt*file.variables['TEMPTEND'][61:70])*yt
    advection_ipa[i]         = np.mean(wt*file.variables['ADVECTION'][61:70])*yt
    submeso_ipa[i]           = np.mean(wt*file.variables['SUBMESO'][61:70])*yt
    neutral_gm_ipa[i]        = np.mean(wt*file.variables['NEUTRAL_GM'][61:70])*yt
    diapycnal_mix_ipa[i]     = np.mean(wt*file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt
    isopycnal_mix_ipa[i]     = np.mean(wt*file.variables['NEUTRAL_DIFFUSION'][61:70])*yt
    swh_ipa[i]               = np.mean(wt*file.variables['SWH'][61:70])*yt
    file.close()

for i in range(len(filename_ipa)):
    residual_ipa[i]   = advection_ipa[i] + submeso_ipa[i] + neutral_gm_ipa[i]
    eddy_ipa[i]       =                    submeso_ipa[i] + neutral_gm_ipa[i]
    resolved_ipa[i]   = residual_ipa[i]  - eddy_ipa[i]
    dia_swh_ipa[i]    = diapycnal_mix_ipa[i] + swh_ipa[i]
    total_ipa[i]      = resolved_ipa[i]  + eddy_ipa[i]    + isopycnal_mix_ipa[i] + diapycnal_mix_ipa[i] + swh_ipa[i]
    remaining_ipa[i]  = total_ipa[i]     - temptend_ipa[i]

for i in range(len(filename_pac)):
    fn = os.path.join(datadir,filename_pac[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time_pac[i]              = file.variables['TIME'][:]/365-2188
    temptend_pac[i]          = np.mean(wt*file.variables['TEMPTEND'][61:70])*yt
    advection_pac[i]         = np.mean(wt*file.variables['ADVECTION'][61:70])*yt
    submeso_pac[i]           = np.mean(wt*file.variables['SUBMESO'][61:70])*yt
    neutral_gm_pac[i]        = np.mean(wt*file.variables['NEUTRAL_GM'][61:70])*yt
    diapycnal_mix_pac[i]     = np.mean(wt*file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt
    isopycnal_mix_pac[i]     = np.mean(wt*file.variables['NEUTRAL_DIFFUSION'][61:70])*yt
    swh_pac[i]               = np.mean(wt*file.variables['SWH'][61:70])*yt
    file.close()

for i in range(len(filename_pac)):
    residual_pac[i]   = advection_pac[i] + submeso_pac[i] + neutral_gm_pac[i]
    eddy_pac[i]       =                    submeso_pac[i] + neutral_gm_pac[i]
    resolved_pac[i]   = residual_pac[i]  - eddy_pac[i]
    dia_swh_pac[i]    = diapycnal_mix_pac[i] + swh_pac[i]
    total_pac[i]      = resolved_pac[i]  + eddy_pac[i]    + isopycnal_mix_pac[i] + diapycnal_mix_pac[i] + swh_pac[i]
    remaining_pac[i]  = total_pac[i]     - temptend_pac[i]

for i in range(len(filename_ind)):
    fn = os.path.join(datadir,filename_ind[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time_ind[i]              = file.variables['TIME'][:]/365-2188
    temptend_ind[i]          = np.mean(wt*file.variables['TEMPTEND'][61:70])*yt
    advection_ind[i]         = np.mean(wt*file.variables['ADVECTION'][61:70])*yt
    submeso_ind[i]           = np.mean(wt*file.variables['SUBMESO'][61:70])*yt
    neutral_gm_ind[i]        = np.mean(wt*file.variables['NEUTRAL_GM'][61:70])*yt
    diapycnal_mix_ind[i]     = np.mean(wt*file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt
    isopycnal_mix_ind[i]     = np.mean(wt*file.variables['NEUTRAL_DIFFUSION'][61:70])*yt
    swh_ind[i]               = np.mean(wt*file.variables['SWH'][61:70])*yt
    file.close()

for i in range(len(filename_ind)):
    residual_ind[i]   = advection_ind[i] + submeso_ind[i] + neutral_gm_ind[i]
    eddy_ind[i]       =                    submeso_ind[i] + neutral_gm_ind[i]
    resolved_ind[i]   = residual_ind[i]  - eddy_ind[i]
    dia_swh_ind[i]    = diapycnal_mix_ind[i] + swh_ind[i]
    total_ind[i]      = resolved_ind[i]  + eddy_ind[i]    + isopycnal_mix_ind[i] + diapycnal_mix_ind[i] + swh_ind[i]
    remaining_ind[i]  = total_ind[i]     - temptend_ind[i]


##--------plotting

#rc('text', usetex=True)
#rc('figure', figsize=(8.27,11.69))
rc('figure', figsize=(8.27,13))

colors = [[0,0,0],[1,0,0],[1,.5,.5],[1,.95,0],[0,0,1],[.5,.5,1],[.7,.7,.7],[1,1,1],[1,1,1]]
labels = ["net","resolved","eddy","residual","isopycnal","diapycnal","all","all-net"]

v = [-2.5,2.5]

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

## global
ax = fig.add_subplot(4,1,1)
ax.plot(temptend_glb[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[0],label=labels[0])
ax.plot(resolved_glb[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[1],label=labels[1])
ax.plot(eddy_glb[:],         marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[2],label=labels[2])
ax.plot(residual_glb[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[3],label=labels[3])
ax.plot(isopycnal_mix_glb[:],marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[4],label=labels[4])
ax.plot(dia_swh_glb[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[5],label=labels[5])
ax.plot(total_glb[:],        marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[6],label=labels[6])
ax.plot(remaining_glb[:],    marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[7],label=labels[7])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.legend(loc=3,ncol=3,fontsize=9);

ax.set_ylabel("$PW$",fontsize=16)
ax.set_xlabel("$Latitude$",fontsize=16)
plt.ylim((v))

#plt.title(exp[3],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["5","10","15","20","25","30","35","40","45","50","55","60","90"],fontsize=16,style='normal')

plt.savefig('tendency_online_CTL_latInt-sens_GLB.png',transparent = False, bbox_inches='tight',dpi=300)
################################################################

v = [-.6,.6]

fig = plt.figure(2)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

## atlantic
ax = fig.add_subplot(4,1,1)
ax.plot(temptend_atl[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[0],label=labels[0])
ax.plot(resolved_atl[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[1],label=labels[1])
ax.plot(eddy_atl[:],         marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[2],label=labels[2])
ax.plot(residual_atl[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[3],label=labels[3])
ax.plot(isopycnal_mix_atl[:],marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[4],label=labels[4])
ax.plot(dia_swh_atl[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[5],label=labels[5])
ax.plot(total_atl[:],        marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[6],label=labels[6])
ax.plot(remaining_atl[:],    marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[7],label=labels[7])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("$PW$",fontsize=16)
plt.ylim((v))

plt.title(exp[1],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],[])

##pacific
ax = fig.add_subplot(4,1,2)
ax.plot(temptend_pac[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[0],label=labels[0])
ax.plot(resolved_pac[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[1],label=labels[1])
ax.plot(eddy_pac[:],         marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[2],label=labels[2])
ax.plot(residual_pac[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[3],label=labels[3])
ax.plot(isopycnal_mix_pac[:],marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[4],label=labels[4])
ax.plot(dia_swh_pac[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[5],label=labels[5])
ax.plot(total_pac[:],        marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[6],label=labels[6])
ax.plot(remaining_pac[:],    marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[7],label=labels[7])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("$PW$",fontsize=16)
plt.ylim((v))

plt.title(exp[2],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],[])

##indian
ax = fig.add_subplot(4,1,3)
ax.plot(temptend_ind[0:7],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[0],label=labels[0])
ax.plot(resolved_ind[0:7],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[1],label=labels[1])
ax.plot(eddy_ind[0:7],         marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[2],label=labels[2])
ax.plot(residual_ind[0:7],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[3],label=labels[3])
ax.plot(isopycnal_mix_ind[0:7],marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[4],label=labels[4])
ax.plot(dia_swh_ind[0:7],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[5],label=labels[5])
ax.plot(total_ind[0:7],        marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[6],label=labels[6])
ax.plot(remaining_ind[0:7],    marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[7],label=labels[7])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.legend(loc=4,ncol=3,fontsize=9);

ax.set_ylabel("$PW$",fontsize=16)
plt.ylim((v))

plt.title(exp[3],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],[])

##IndianPacific
ax = fig.add_subplot(4,1,4)
ax.plot(temptend_ipa[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[0],label=labels[0])
ax.plot(resolved_ipa[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[1],label=labels[1])
ax.plot(eddy_ipa[:],         marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[2],label=labels[2])
ax.plot(residual_ipa[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[3],label=labels[3])
ax.plot(isopycnal_mix_ipa[:],marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[4],label=labels[4])
ax.plot(dia_swh_ipa[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[5],label=labels[5])
ax.plot(total_ipa[:],        marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[6],label=labels[6])
ax.plot(remaining_ipa[:],    marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[7],label=labels[7])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

#ax.legend(loc=4,ncol=3,fontsize=9);

ax.set_ylabel("$PW$",fontsize=16)
ax.set_xlabel("$Latitude$",fontsize=16)
plt.ylim((v))

plt.title(exp[4],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["5","10","15","20","25","30","35","40","45","50","55","60","90"],fontsize=16,style='normal')

#plt.show()
plt.savefig('tendency_online_CTL_latInt-sens.png',transparent = False, bbox_inches='tight',dpi=300)
