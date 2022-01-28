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

exp      = ["Stress","Water","Heat","flux-only"]
filename = ["STC_temptend_FAFSTRESS_GLB_zonal.nc","STC_temptend_FAFWATER_GLB_zonal.nc","STC_temptend_FAFHEAT_GLB_zonal.nc","STC_temptend_flux-only_GLB_zonal.nc"]
filename2  = ["BSO_GLB_FAFSTRESS.nc","BSO_GLB_FAFWATER.nc","BSO_GLB_FAFHEAT.nc","BSO_GLB_flux-only.nc"]
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
remaining             = [None]*len(filename)

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
    temptend[i]          = np.squeeze(np.mean(file.variables['TEMPTEND_NO_MLD'][61:70,:,:],0))*yt
    advection[i]         = np.squeeze(np.mean(file.variables['ADVECTION_NO_MLD'][61:70,:,:],0))*yt
    submeso[i]           = np.squeeze(np.mean(file.variables['SUBMESO_NO_MLD'][61:70,:,:],0))*yt
    neutral_gm[i]        = np.squeeze(np.mean(file.variables['NEUTRAL_GM_NO_MLD'][61:70,:,:],0))*yt
    diapycnal_mix[i]     = np.squeeze(np.mean(file.variables['VDIFFUSE_DIFF_CBT_NO_MLD'][61:70,:,:],0))*yt
    isopycnal_mix[i]     = np.squeeze(np.mean(file.variables['NEUTRAL_DIFFUSION_NO_MLD'][61:70,:,:],0))*yt
    sw_heat[i]           = np.squeeze(np.mean(file.variables['SWH_NO_MLD'][61:70,:,:],0))*yt
    file.close()

for i in range(len(filename)):
    residual[i]   = advection[i] + submeso[i] + neutral_gm[i]
    eddy[i]       =                submeso[i] + neutral_gm[i] 
    resolved[i]   = residual[i]  - eddy[i]
    total[i]      = resolved[i]  + eddy[i] +  isopycnal_mix[i] + diapycnal_mix[i] + sw_heat[i]
    remaining[i]  = total[i]     - temptend[i]     

for i in range(len(exp)):
    fn = os.path.join(datadir2,filename2[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
#    lat_bso[i]   = file.variables['Y'][:]
    bso[i]       = file.variables['field'][:]
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir2,filename3[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    latrho[i]   = file.variables['YT_OCEAN'][:]
    depthrho[i] = file.variables['ST_OCEAN'][:]
    potrho[i]  = file.variables['POT_RHO_0_ZONALMEAN_GLB'][:]-1000.
    file.close()

rc('figure', figsize=(8.27,11.69))

cmap2 = plt.get_cmap('bwr')

#cmap2.set_bad(color = '0.5', alpha = None)

kmin = -2; kmax = 2
clevs = np.arange(kmin,kmax+.1,1.)

clevs_moc = [-30,-20,-18,-16,-14,-12,-10,-5,-2.5,-2,-1,0,1,2,2.5,5,10,15,20,30]
clevs_rho = [24.5,25.0,25.5,26.0,26.6,27.0,27.5,27.75]

v = [-45,45,0,1500]

fig = plt.figure(1)
fig.subplots_adjust(hspace=0.25,wspace=0.12)

[lat2[-1],depth2[-1]]       = np.meshgrid(lat[-1],depth[-1])
[latrho2[-1],depthrho2[-1]] = np.meshgrid(latrho[-1],depthrho[-1])

ax = fig.add_subplot(3,2,1)
cs  = plt.pcolormesh(lat2[-1],depth2[-1],temptend[-1][:,:],shading='flat',cmap=cmap2)
plt.clim(kmin,kmax)

plt.plot(latrho[-1],bso[-1][:],linestyle='solid',color='black',linewidth=1.5)
cc2 = plt.contour(latrho2[-1],depthrho2[-1],potrho[-1],levels=clevs_rho,colors='black',linestyles='solid',linewidths=.5)
plt.clabel(cc2,inline=1,fmt='%1.1f',fontsize=8)

plt.title('Net')

plt.axvline(x=25,color='k',linestyle='--',linewidth=1.5); plt.axvline(x=-30,color='k',linestyle='--',linewidth=1.5)

plt.xticks([-45,-30,-15,0,15,30,45],[],fontsize=12)
plt.yticks([0,500,1000,1500,2000],[0,500,1000,1500,2000],fontsize=12)
ax.set_ylabel('Depth [m]',fontsize=14)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(3,2,2)
cs  = plt.pcolormesh(lat2[-1],depth2[-1],residual[-1][:,:],shading='flat',cmap=cmap2)
plt.clim(kmin,kmax)

plt.plot(latrho[-1],bso[-1][:],linestyle='solid',color='black',linewidth=1.5)
cc2 = plt.contour(latrho2[-1],depthrho2[-1],potrho[-1],levels=clevs_rho,colors='black',linestyles='solid',linewidths=.5)
plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

plt.title('Residual advection')

plt.axvline(x=25,color='k',linestyle='--',linewidth=1.5); plt.axvline(x=-30,color='k',linestyle='--',linewidth=1.5)

plt.xticks([-45,-30,-15,0,15,30,45],[],fontsize=12)
plt.yticks([0,500,1000,1500,2000],[],fontsize=12)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(3,2,3)
cs  = plt.pcolormesh(lat2[-1],depth2[-1],resolved[-1][:,:],shading='flat',cmap=cmap2)
plt.clim(kmin,kmax)

plt.plot(latrho[-1],bso[-1][:],linestyle='solid',color='black',linewidth=1.5)
cc2 = plt.contour(latrho2[-1],depthrho2[-1],potrho[-1],levels=clevs_rho,colors='black',linestyles='solid',linewidths=.5)
plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

plt.title('Resolved advection')

plt.axvline(x=25,color='k',linestyle='--',linewidth=1.5); plt.axvline(x=-30,color='k',linestyle='--',linewidth=1.5)

plt.xticks([-45,-30,-15,0,15,30,45],[],fontsize=12)
plt.yticks([0,500,1000,1500,2000],[0,500,1000,1500,2000],fontsize=12)
ax.set_ylabel('Depth [m]',fontsize=14)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(3,2,4)
cs  = plt.pcolormesh(lat2[-1],depth2[-1],eddy[-1][:,:],shading='flat',cmap=cmap2)
plt.clim(kmin,kmax)

plt.plot(latrho[-1],bso[-1][:],linestyle='solid',color='black',linewidth=1.5)
cc2 = plt.contour(latrho2[-1],depthrho2[-1],potrho[-1],levels=clevs_rho,colors='black',linestyles='solid',linewidths=.5)
plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

plt.title('Eddy advection')

plt.axvline(x=25,color='k',linestyle='--',linewidth=1.5); plt.axvline(x=-30,color='k',linestyle='--',linewidth=1.5)

plt.xticks([-45,-30,-15,0,15,30,45],[],fontsize=12)
plt.yticks([0,500,1000,1500,2000],[],fontsize=12)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(3,2,5)
cs  = plt.pcolormesh(lat2[-1],depth2[-1],diapycnal_mix[-1][:,:]+sw_heat[-1][:,:],shading='flat',cmap=cmap2)
plt.clim(kmin,kmax)

plt.plot(latrho[-1],bso[-1][:],linestyle='solid',color='black',linewidth=1.5)
cc2 = plt.contour(latrho2[-1],depthrho2[-1],potrho[-1],levels=clevs_rho,colors='black',linestyles='solid',linewidths=.5)
plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

plt.title('Diapycnal mix + swp')

plt.axvline(x=25,color='k',linestyle='--',linewidth=1.5); plt.axvline(x=-30,color='k',linestyle='--',linewidth=1.5)

plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
plt.yticks([0,500,1000,1500,2000],[0,500,1000,1500,2000],fontsize=12)
ax.set_ylabel('Depth [m]',fontsize=14)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(3,2,6)
cs  = plt.pcolormesh(lat2[-1],depth2[-1],isopycnal_mix[-1][:,:],shading='flat',cmap=cmap2)
plt.clim(kmin,kmax)

plt.plot(latrho[-1],bso[-1][:],linestyle='solid',color='black',linewidth=1.5)
cc2 = plt.contour(latrho2[-1],depthrho2[-1],potrho[-1],levels=clevs_rho,colors='black',linestyles='solid',linewidths=.5)
plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

plt.title('Isopycnal mix')

plt.axvline(x=25,color='k',linestyle='--',linewidth=1.5); plt.axvline(x=-30,color='k',linestyle='--',linewidth=1.5)

plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
plt.yticks([0,500,1000,1500,2000],[],fontsize=12)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

cbaxes = fig.add_axes([0.2, 0.03, 0.6, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal")
cbar.ax.tick_params(labelsize=12)
cbar.ax.set_title("[$TW$]",fontsize=14,color='k')

#plt.show()
plt.savefig('STC_OHC_GLB_diag_tend_online_zonal_CTL.png',transparent = False, bbox_inches='tight',dpi=300)
