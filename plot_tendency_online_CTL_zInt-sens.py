import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/TEMP-tend/DATA'

exp      = ["vertical level 2 (15-m depth)","vertical level 5 (45-m depth)","vertical level 10 (95-m depth)","vertical level 20 (195-m depth)","vertical level 27 (335-m depth)"]

filename_glb = ["DATA_vInt02-50/heat_budget_flux-only_GLB.nc","DATA_vInt05-50/heat_budget_flux-only_GLB.nc","DATA_vInt10-50/heat_budget_flux-only_GLB.nc","DATA_vInt20-50/heat_budget_flux-only_GLB.nc","DATA_vInt27-50/heat_budget_flux-only_GLB.nc"]
filename_atl = ["DATA_vInt02-50/heat_budget_flux-only_ATL.nc","DATA_vInt05-50/heat_budget_flux-only_ATL.nc","DATA_vInt10-50/heat_budget_flux-only_ATL.nc","DATA_vInt20-50/heat_budget_flux-only_ATL.nc","DATA_vInt27-50/heat_budget_flux-only_ATL.nc"]
filename_ipa = ["DATA_vInt02-50/heat_budget_flux-only_IPA.nc","DATA_vInt05-50/heat_budget_flux-only_IPA.nc","DATA_vInt10-50/heat_budget_flux-only_IPA.nc","DATA_vInt20-50/heat_budget_flux-only_IPA.nc","DATA_vInt27-50/heat_budget_flux-only_IPA.nc"]
filename_pac = ["DATA_vInt02-50/heat_budget_flux-only_PAC.nc","DATA_vInt05-50/heat_budget_flux-only_PAC.nc","DATA_vInt10-50/heat_budget_flux-only_PAC.nc","DATA_vInt20-50/heat_budget_flux-only_PAC.nc","DATA_vInt27-50/heat_budget_flux-only_PAC.nc"]
filename_ind = ["DATA_vInt02-50/heat_budget_flux-only_IND.nc","DATA_vInt05-50/heat_budget_flux-only_IND.nc","DATA_vInt10-50/heat_budget_flux-only_IND.nc","DATA_vInt20-50/heat_budget_flux-only_IND.nc","DATA_vInt27-50/heat_budget_flux-only_IND.nc"]
filename_soc = ["DATA_vInt02-50/heat_budget_flux-only_SOC.nc","DATA_vInt05-50/heat_budget_flux-only_SOC.nc","DATA_vInt10-50/heat_budget_flux-only_SOC.nc","DATA_vInt20-50/heat_budget_flux-only_SOC.nc","DATA_vInt27-50/heat_budget_flux-only_SOC.nc"]

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

time_soc              = [None]*len(filename_soc)
temptend_soc          = [None]*len(filename_soc)
advection_soc         = [None]*len(filename_soc)
submeso_soc           = [None]*len(filename_soc)
neutral_gm_soc        = [None]*len(filename_soc)
diapycnal_mix_soc     = [None]*len(filename_soc)
isopycnal_mix_soc     = [None]*len(filename_soc)
swh_soc               = [None]*len(filename_soc)
residual_soc          = [None]*len(filename_soc)
eddy_soc              = [None]*len(filename_soc)
resolved_soc          = [None]*len(filename_soc)
total_soc             = [None]*len(filename_soc)
remaining_soc         = [None]*len(filename_soc)
dia_swh_soc           = [None]*len(filename_soc)

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

for i in range(len(filename_soc)):
    fn = os.path.join(datadir,filename_soc[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time_soc[i]              = file.variables['TIME'][:]/365-2188
    temptend_soc[i]          = np.mean(wt*file.variables['TEMPTEND'][61:70])*yt
    advection_soc[i]         = np.mean(wt*file.variables['ADVECTION'][61:70])*yt
    submeso_soc[i]           = np.mean(wt*file.variables['SUBMESO'][61:70])*yt
    neutral_gm_soc[i]        = np.mean(wt*file.variables['NEUTRAL_GM'][61:70])*yt
    diapycnal_mix_soc[i]     = np.mean(wt*file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt
    isopycnal_mix_soc[i]     = np.mean(wt*file.variables['NEUTRAL_DIFFUSION'][61:70])*yt
    swh_soc[i]               = np.mean(wt*file.variables['SWH'][61:70])*yt
    file.close()

for i in range(len(filename_soc)):
    residual_soc[i]  = advection_soc[i] + submeso_soc[i] + neutral_gm_soc[i]
    eddy_soc[i]      =                    submeso_soc[i] + neutral_gm_soc[i]
    resolved_soc[i]  = residual_soc[i]  - eddy_soc[i]
    dia_swh_soc[i]   = diapycnal_mix_soc[i] + swh_soc[i]
    total_soc[i]     = resolved_soc[i]  + eddy_soc[i]    + isopycnal_mix_soc[i] + diapycnal_mix_soc[i] + swh_soc[i]
    remaining_soc[i] = total_soc[i]     - temptend_soc[i]


##--------plotting

#rc('text', usetex=True)
rc('figure', figsize=(8.27,11.69))

colors = [[0,0,0],[1,0,0],[1,.5,.5],[1,.95,0],[0,0,1],[.5,.5,1],[.7,.7,.7],[1,1,1],[1,1,1]]
labels = ["net","resolved","eddy","residual","isopycnal","diapycnal","all","net-all"]

v = [-5,5]

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)):
    ax = fig.add_subplot(5,1,i+1)

    ax.plot(1.0,temptend_glb[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0]) #net
    ax.plot(0.8,resolved_glb[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1]) #resolved
    ax.plot(0.8,eddy_glb[i],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2]) #eddy
    ax.plot(0.8,residual_glb[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3]) #residual
    ax.plot(1.2,isopycnal_mix_glb[i],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4]) #isopycnal
    ax.plot(1.2,dia_swh_glb[i],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5]) #diapycnal 
    ax.plot(1.0,total_glb[i],                marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6]) #all
    ax.plot(1.0,remaining_glb[i],        marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[7]) #remaining

    ax.plot(3.0,temptend_soc[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(2.8,resolved_soc[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(2.8,eddy_soc[i],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
    ax.plot(2.8,residual_soc[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
    ax.plot(3.2,isopycnal_mix_soc[i],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
    ax.plot(3.2,dia_swh_soc[i],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
    ax.plot(3.0,total_soc[i],                marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])
    ax.plot(3.0,remaining_soc[i],        marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[7])

    ax.plot(5.0,temptend_atl[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(4.8,resolved_atl[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(4.8,eddy_atl[i],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
    ax.plot(4.8,residual_atl[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
    ax.plot(5.2,isopycnal_mix_atl[i],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
    ax.plot(5.2,dia_swh_atl[i],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
    ax.plot(5.0,total_atl[i],                marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])
    ax.plot(5.0,remaining_atl[i],        marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[7])

    ax.plot(7.0,temptend_ipa[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(6.8,resolved_ipa[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(6.8,eddy_ipa[i],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
    ax.plot(6.8,residual_ipa[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
    ax.plot(7.2,isopycnal_mix_ipa[i],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
    ax.plot(7.2,dia_swh_ipa[i],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
    ax.plot(7.0,total_ipa[i],                marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])
    ax.plot(7.0,remaining_ipa[i],        marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[7])

    ax.plot(9.0,temptend_pac[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(8.8,resolved_pac[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(8.8,eddy_pac[i],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
    ax.plot(8.8,residual_pac[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
    ax.plot(9.2,isopycnal_mix_pac[i],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
    ax.plot(9.2,dia_swh_pac[i],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
    ax.plot(9.0,total_pac[i],                marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])
    ax.plot(9.0,remaining_pac[i],        marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[7])

    ax.plot(11.0,temptend_ind[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0],label=labels[0])
    ax.plot(10.8,resolved_ind[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1],label=labels[1])
    ax.plot(10.8,eddy_ind[i],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2],label=labels[2])
    ax.plot(10.8,residual_ind[i],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3],label=labels[3])
    ax.plot(11.2,isopycnal_mix_ind[i],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4],label=labels[4])
    ax.plot(11.2,dia_swh_ind[i],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5],label=labels[5])
    ax.plot(11.0,total_ind[i],                marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6],label=labels[6])
    ax.plot(11.0,remaining_ind[i],        marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[7],label=labels[7])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    if i==3: ax.legend(loc=4,ncol=3,fontsize=9);

    ax.set_ylabel("$PW$",fontsize=16)
    plt.ylim((v))

    plt.title(exp[i],style='normal',fontsize=16)
    plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["","","","","","","","","","","","",""],fontsize=16,style='normal')

plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["","GLB","","SOC","","ATL","","IPA","","PAC","","IND",""],fontsize=16,style='normal')

#plt.show()
plt.savefig('tendency_online_CTL_zInt-sens.png',transparent = False, bbox_inches='tight',dpi=300)
