import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/TEMP-tendency/DATA_vInt_MLD_BSO'
datadir2 = '/home/clima-archive2/rfarneti/RENE/DATA'

exp       = ["Stress","Water","Heat","flux-only"]
filename  = ["STC_temptend_FAFSTRESS_GLB_zonal.nc","STC_temptend_FAFWATER_GLB_zonal.nc","STC_temptend_FAFHEAT_GLB_zonal.nc","STC_temptend_flux-only_GLB_zonal.nc"]
filename2 = ["BSO_GLB_FAFSTRESS.nc","BSO_GLB_FAFWATER.nc","BSO_GLB_FAFHEAT.nc","BSO_GLB_flux-only.nc"]
filename3 = ["pot_rho_0_zonalmean_FAFSTRESS.nc","pot_rho_0_zonalmean_FAFWATER.nc","pot_rho_0_zonalmean_FAFHEAT.nc","pot_rho_0_zonalmean_flux-only.nc"]

lat                   = [None]*len(filename)
depth                 = [None]*len(filename)
lat2                  = [None]*len(filename)
depth2                = [None]*len(filename)

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
diapycnal_mix_swp     = [None]*len(filename)

latrho               = [None]*len(filename)
depthrho             = [None]*len(filename)
latrho2              = [None]*len(filename)
depthrho2            = [None]*len(filename)
bso                  = [None]*len(filename)
potrho               = [None]*len(filename)

yt = 1e-12 #TW
t = np.arange(0,70)

tyear = 365.25 * 24.0 * 3600.0
dt = np.ones((len(t),50,88))*tyear

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    lat[i]               = file.variables['YT_OCEAN3_190'][:]
    depth[i]             = file.variables['ST_OCEAN'][:]
    temptend[i]          = np.squeeze(np.sum(np.mean(file.variables['TEMPTEND_NO_MLD'][61:70,:,50:132],0),axis=1))*yt
    advection[i]         = np.squeeze(np.sum(np.mean(file.variables['ADVECTION_NO_MLD'][61:70,:,50:132],0),axis=1))*yt
    submeso[i]           = np.squeeze(np.sum(np.mean(file.variables['SUBMESO_NO_MLD'][61:70,:,50:132],0),axis=1))*yt
    neutral_gm[i]        = np.squeeze(np.sum(np.mean(file.variables['NEUTRAL_GM_NO_MLD'][61:70,:,50:132],0),axis=1))*yt
    diapycnal_mix[i]     = np.squeeze(np.sum(np.mean(file.variables['VDIFFUSE_DIFF_CBT_NO_MLD'][61:70,:,50:132],0),axis=1))*yt
    isopycnal_mix[i]     = np.squeeze(np.sum(np.mean(file.variables['NEUTRAL_DIFFUSION_NO_MLD'][61:70,:,50:132],0),axis=1))*yt
    sw_heat[i]           = np.squeeze(np.sum(np.mean(file.variables['SWH_NO_MLD'][61:70,:,50:132],0),axis=1))*yt
    file.close()

for i in range(len(filename)):
    residual[i]   = advection[i] + submeso[i] + neutral_gm[i]
    eddy[i]       =                submeso[i] + neutral_gm[i] 
    resolved[i]   = residual[i]  - eddy[i]
    total[i]      = resolved[i]  + eddy[i] +  isopycnal_mix[i] + diapycnal_mix[i] + sw_heat[i]
    diapycnal_mix_swp[i] = diapycnal_mix[i] + sw_heat[i]

for i in range(len(exp)):
    fn = os.path.join(datadir2,filename2[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    bso[i]       = -np.squeeze(np.mean(file.variables['field'][:]))
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir2,filename3[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    latrho[i]   = file.variables['YT_OCEAN'][:]
    depthrho[i] = file.variables['ST_OCEAN'][:]
    potrho[i]   = np.mean(file.variables['POT_RHO_0_ZONALMEAN_GLB'][:,50:132]-1000.,axis=1)
    file.close()

rc('figure', figsize=(11,11.69))

cmap2 = plt.get_cmap('bwr')

#cmap2.set_bad(color = '0.5', alpha = None)

colors = [[0,0,0],[1,0,0],[1,.5,.5],[1,.95,0],[0,0,1],[.5,.5,1],[.7,.7,.7],[1,1,1],[1,1,1]]
labels = ["net","resolved","eddy","residual","isopycnal","diapycnal","total"]

clevs_rho = [24.5,25.0,25.5,26.0,26.6,27.0,27.5,27.75]
xx = np.linspace(-1000,1000,20); potrhomesh = np.ones((50,len(xx)))

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.3)

v = [-15,15,-1300,0]

for i in range(len(exp)-1):
    ax = fig.add_subplot(2,4,i+1)
    ax.plot(temptend[i]-temptend[-1],-depth[i],linestyle='-',linewidth=2,color=colors[0],label=labels[0])
    ax.plot(resolved[i]-resolved[-1],-depth[i],linestyle='-',linewidth=2,color=colors[1],label=labels[1])
    ax.plot(eddy[i]-eddy[-1],-depth[i],linestyle='-',linewidth=2,color=colors[2],label=labels[2])
    ax.plot(residual[i]-residual[-1],-depth[i],linestyle='-',linewidth=2,color=colors[3],label=labels[3])
    ax.plot(isopycnal_mix[i]-isopycnal_mix[-1],-depth[i],linestyle='-',linewidth=2,color=colors[4],label=labels[4])
    ax.plot(diapycnal_mix_swp[i]-diapycnal_mix_swp[-1],-depth[i],linestyle='-',linewidth=2,color=colors[5],label=labels[5])
    
    for j in range(len(xx)): potrhomesh[:,j]=potrho[i]
    plt.contour(xx,-depthrho[-1],potrhomesh,levels=clevs_rho,colors='gray',linestyles='dashed',linewidths=1)

    ##-----------for beauty
    if (i>=1):
        plt.yticks([0,-200,-400,-600,-800,-1000,-1200],[],fontsize=10)
    else:
        plt.yticks([0,-200,-400,-600,-800,-1000,-1200],[0,-200,-400,-600,-800,-1000,-1200],fontsize=10)
        ax.set_ylabel('$Depth [m]$',fontsize=14)

    plt.xticks([-15,-10,-5,0,5,10,15],[-15,-10,-5,0,5,10,15],fontsize=10)
    
    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
    ##-----------

    plt.title(exp[i],style='normal',fontsize=16)
    
    ax.set_xlabel('$[TW]$',fontsize=14)
    ax.axis(v)

ax  = fig.add_subplot(2,4,4)
ax.plot(temptend[-1],-depth[-1],linestyle='-',linewidth=2,color=colors[0],label=labels[0])
ax.plot(resolved[-1],-depth[-1],linestyle='-',linewidth=2,color=colors[1],label=labels[1])
ax.plot(eddy[-1],-depth[-1],linestyle='-',linewidth=2,color=colors[2],label=labels[2])
ax.plot(residual[-1],-depth[-1],linestyle='-',linewidth=2,color=colors[3],label=labels[3])
ax.plot(isopycnal_mix[-1],-depth[-1],linestyle='-',linewidth=2,color=colors[4],label=labels[4])
ax.plot(diapycnal_mix_swp[-1],-depth[-1],linestyle='-',linewidth=2,color=colors[5],label=labels[5])

for j in range(len(xx)): potrhomesh[:,j]=potrho[-1]
cc=plt.contour(xx,-depthrho[-1],potrhomesh,levels=clevs_rho,colors='gray',linestyles='dashed',linewidths=1)
plt.clabel(cc,fmt='%1.1f',fontsize=8)

ax.legend(loc=4,ncol=1,fontsize=9);

plt.yticks([0,-200,-400,-600,-800,-1000,-1200],[],fontsize=10)
plt.xticks([-400,-200,0,200,400],[-400,-200,0,200,400],fontsize=10)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

plt.title(exp[-1],style='normal',fontsize=16)

ax.set_xlabel('$[TW]$',fontsize=14)
ax.axis([-500,500,-1300,0])

#plt.show()
plt.savefig('STC_OHC_GLB_diag_tend_online_vprofile.png',transparent = False, bbox_inches='tight',dpi=300)
