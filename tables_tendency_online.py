import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/TEMP-tend/DATA/DATA_vInt27-50'

exp          = ["Stress","Water","Heat","flux-only"]
filename_glb = ["heat_budget_FAFSTRESS_GLB.nc","heat_budget_FAFWATER_GLB.nc","heat_budget_FAFHEAT_GLB.nc","heat_budget_flux-only_GLB.nc"]
filename_atl = ["heat_budget_FAFSTRESS_ATL.nc","heat_budget_FAFWATER_ATL.nc","heat_budget_FAFHEAT_ATL.nc","heat_budget_flux-only_ATL.nc"]
filename_ipa = ["heat_budget_FAFSTRESS_IPA.nc","heat_budget_FAFWATER_IPA.nc","heat_budget_FAFHEAT_IPA.nc","heat_budget_flux-only_IPA.nc"]
filename_pac = ["heat_budget_FAFSTRESS_PAC.nc","heat_budget_FAFWATER_PAC.nc","heat_budget_FAFHEAT_PAC.nc","heat_budget_flux-only_PAC.nc"]
filename_ind = ["heat_budget_FAFSTRESS_IND.nc","heat_budget_FAFWATER_IND.nc","heat_budget_FAFHEAT_IND.nc","heat_budget_flux-only_IND.nc"]
filename_soc = ["heat_budget_FAFSTRESS_SOC.nc","heat_budget_FAFWATER_SOC.nc","heat_budget_FAFHEAT_SOC.nc","heat_budget_flux-only_SOC.nc"]

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

yt = 1e-15 #PW
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


rc('text', usetex=True)
rc('figure', figsize=(8.27,11.69))

print("& exp & nettemp & resolved &  eddy  & residual & isopycnal & diapycnal &  total  & remaining ")
for i in range(len(exp)):
    print("%s " %exp[i])
    print("\centering GLB "  + " & %.4f " %temptend_glb[i] + " & %.4f " %resolved_glb[i] + " & %.4f " %eddy_glb[i] + " & %.4f " %residual_glb[i] + " & %.4f " %isopycnal_mix_glb[i] + " & %.4f " %dia_swh_glb[i] + " & %.4f " %total_glb[i] + " & %.4f " %remaining_glb[i])
    print("\centering ATL "  + " & %.4f " %temptend_atl[i] + " & %.4f " %resolved_atl[i] + " & %.4f " %eddy_atl[i] + " & %.4f " %residual_atl[i] + " & %.4f " %isopycnal_mix_atl[i] + " & %.4f " %dia_swh_atl[i] + " & %.4f " %total_atl[i] + " & %.4f " %remaining_atl[i])
    print("\centering PAC "  + " & %.4f " %temptend_pac[i] + " & %.4f " %resolved_pac[i] + " & %.4f " %eddy_pac[i] + " & %.4f " %residual_pac[i] + " & %.4f " %isopycnal_mix_pac[i] + " & %.4f " %dia_swh_pac[i] + " & %.4f " %total_pac[i] + " & %.4f " %remaining_pac[i])
    print("\centering IND "  + " & %.4f " %temptend_ind[i] + " & %.4f " %resolved_ind[i] + " & %.4f " %eddy_ind[i] + " & %.4f " %residual_ind[i] + " & %.4f " %isopycnal_mix_ind[i] + " & %.4f " %dia_swh_ind[i] + " & %.4f " %total_ind[i] + " & %.4f " %remaining_ind[i])
    print("\centering IPA "  + " & %.4f " %temptend_ipa[i] + " & %.4f " %resolved_ipa[i] + " & %.4f " %eddy_ipa[i] + " & %.4f " %residual_ipa[i] + " & %.4f " %isopycnal_mix_ipa[i] + " & %.4f " %dia_swh_ipa[i] + " & %.4f " %total_ipa[i] + " & %.4f " %remaining_ipa[i])
    print("\centering SOC "  + " & %.4f " %temptend_soc[i] + " & %.4f " %resolved_soc[i] + " & %.4f " %eddy_soc[i] + " & %.4f " %residual_soc[i] + " & %.4f " %isopycnal_mix_soc[i] + " & %.4f " %dia_swh_soc[i] + " & %.4f " %total_soc[i] + " & %.4f " %remaining_soc[i])

print('-----------------------------------')
print('TRANSIENT CHANGE TABLES (ie. after control substraction)')
print('-----------------------------------')

print("& exp & nettemp & resolved &  eddy  & residual & isopycnal & diapycnal &  total  & remaining ")
for i in range(len(exp)-1):
    print("%s " %exp[i])
    print("\centering GLB "  + " & %.4f " %(temptend_glb[i]-temptend_glb[-1]) + " & %.4f " %(resolved_glb[i]-resolved_glb[-1]) + " & %.4f " %(eddy_glb[i]-eddy_glb[-1]) + " & %.4f " %(residual_glb[i]-residual_glb[-1]) + " & %.4f " %(isopycnal_mix_glb[i]-isopycnal_mix_glb[-1]) + " & %.4f " %(dia_swh_glb[i]-dia_swh_glb[-1]) + " & %.4f " %(total_glb[i] -total_glb[-1]) + " & %.4f " %(remaining_glb[i]-remaining_glb[-1]))
    print("\centering ATL "  + " & %.4f " %(temptend_atl[i]-temptend_atl[-1]) + " & %.4f " %(resolved_atl[i]-resolved_atl[-1]) + " & %.4f " %(eddy_atl[i]-eddy_atl[-1]) + " & %.4f " %(residual_atl[i]-residual_atl[-1]) + " & %.4f " %(isopycnal_mix_atl[i]-isopycnal_mix_atl[-1]) + " & %.4f " %(dia_swh_atl[i]-dia_swh_atl[-1]) + " & %.4f " %(total_atl[i] -total_atl[-1]) + " & %.4f " %(remaining_atl[i]-remaining_atl[-1]))
    print("\centering PAC "  + " & %.4f " %(temptend_pac[i]-temptend_pac[-1]) + " & %.4f " %(resolved_pac[i]-resolved_pac[-1]) + " & %.4f " %(eddy_pac[i]-eddy_pac[-1]) + " & %.4f " %(residual_pac[i]-residual_pac[-1]) + " & %.4f " %(isopycnal_mix_pac[i]-isopycnal_mix_pac[-1]) + " & %.4f " %(dia_swh_pac[i]-dia_swh_pac[-1]) + " & %.4f " %(total_pac[i] -total_pac[-1]) + " & %.4f " %(remaining_pac[i]-remaining_pac[-1]))
    print("\centering IND "  + " & %.4f " %(temptend_ind[i]-temptend_ind[-1]) + " & %.4f " %(resolved_ind[i]-resolved_ind[-1]) + " & %.4f " %(eddy_ind[i]-eddy_ind[-1]) + " & %.4f " %(residual_ind[i]-residual_ind[-1]) + " & %.4f " %(isopycnal_mix_ind[i]-isopycnal_mix_ind[-1]) + " & %.4f " %(dia_swh_ind[i]-dia_swh_ind[-1]) + " & %.4f " %(total_ind[i] -total_ind[-1]) + " & %.4f " %(remaining_ind[i]-remaining_ind[-1]))
    print("\centering IPA "  + " & %.4f " %(temptend_ipa[i]-temptend_ipa[-1]) + " & %.4f " %(resolved_ipa[i]-resolved_ipa[-1]) + " & %.4f " %(eddy_ipa[i]-eddy_ipa[-1]) + " & %.4f " %(residual_ipa[i]-residual_ipa[-1]) + " & %.4f " %(isopycnal_mix_ipa[i]-isopycnal_mix_ipa[-1]) + " & %.4f " %(dia_swh_ipa[i]-dia_swh_ipa[-1]) + " & %.4f " %(total_ipa[i] -total_ipa[-1]) + " & %.4f " %(remaining_ipa[i]-remaining_ipa[-1]))
    print("\centering SOC "  + " & %.4f " %(temptend_soc[i]-temptend_soc[-1]) + " & %.4f " %(resolved_soc[i]-resolved_soc[-1]) + " & %.4f " %(eddy_soc[i]-eddy_soc[-1]) + " & %.4f " %(residual_soc[i]-residual_soc[-1]) + " & %.4f " %(isopycnal_mix_soc[i]-isopycnal_mix_soc[-1]) + " & %.4f " %(dia_swh_soc[i]-dia_swh_soc[-1]) + " & %.4f " %(total_soc[i] -total_soc[-1]) + " & %.4f " %(remaining_soc[i]-remaining_soc[-1]))

