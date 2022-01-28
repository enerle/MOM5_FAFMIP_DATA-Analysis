import sys
import os
import numpy as np
from scipy.stats import pearsonr
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/TEMP-tend/DATA'
filename = 'temp_diag_tend-flux-only.nc'
fn = os.path.join(datadir,filename)
file = nc.Dataset(fn)
depth      = file.variables['st_ocean'][:]
pswh       = file.variables['sw_heat'][:,:,:,:] #penetrative shortwave heating
temptend   = file.variables['temp_tendency'][:,:,:,:]
advection  = file.variables['temp_advection'][:,:,:,:]
submeso    = file.variables['temp_submeso'][:,:,:,:]
neutral_gm = file.variables['neutral_gm_temp'][:,:,:,:]
diapycnal  = file.variables['temp_vdiffuse_diff_cbt'][:,:,:,:]
isopycnal  = file.variables['neutral_diffusion_temp'][:,:,:,:]

datadir2 = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/SFC-fluxes/DATA'
filename2 = 'ocean_fluxes_Blaker_flux-only.nc'
fn = os.path.join(datadir2,filename2)
file = nc.Dataset(fn)
hflx = file.variables['sfc_hflux_coupler'][:,:,:]

##
## statistics
##

pswh_mean      = np.squeeze(np.mean(pswh,axis=(0,2,3)))
temptend_mean  = np.squeeze(np.mean(temptend,axis=(0,2,3)))
resolved_mean  = np.squeeze(np.mean(advection,axis=(0,2,3)))
eddy_mean      = np.squeeze(np.mean(submeso[:,:,:,:] + neutral_gm[:,:,:,:],axis=(0,2,3)))
residual_mean  = resolved_mean + eddy_mean
diapycnal_mean = np.squeeze(np.mean(diapycnal,axis=(0,2,3)))
isopycnal_mean = np.squeeze(np.mean(isopycnal,axis=(0,2,3)))
total_mean     = resolved_mean[:]+eddy_mean[:]+diapycnal_mean[:]+isopycnal_mean[:]
remaining_mean = total_mean[:]-temptend_mean[:]
dia_swh_mean   = diapycnal_mean + pswh_mean

temptend_std  = np.squeeze(np.std(np.mean(temptend,axis=(2,3)),axis=0))

#rc('text', usetex=True)
rc('figure', figsize=(8.27,11.69))

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax  = fig.add_subplot(2,2,1)
ax.plot(temptend_mean[27:50],-depth[27:50],linestyle='-',linewidth=2,color='black',label='net')
#ax.plot(temptend_std,-depth,linestyle='-',linewidth=2,color='red',label='std. dev')
ax.plot(temptend_mean[27:50]+temptend_std[27:50],-depth[27:50],linestyle='--',linewidth=1,color='black')
ax.plot(temptend_mean[27:50]-temptend_std[27:50],-depth[27:50],linestyle='--',linewidth=1,color='black')
ax.plot(total_mean[27:50],-depth[27:50],linestyle='-',linewidth=2,color='gray',label='all')

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$m$',fontsize=14)
ax.set_xlabel('$Wm^{-2}$',fontsize=14)
ax.legend(loc=3,fontsize=9)
ax.axis([-.05,.05,-5500,0])
plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2)
plt.yticks([0,-1000,-2000,-3000,-4000,-5000],[0,-1000,-2000,-3000,-4000,-5000])

ax  = fig.add_subplot(2,2,2)
ax.plot(temptend_mean[27:50], -depth[27:50],linestyle='-',linewidth=2,color=[0,0,0],label='net')
ax.plot(resolved_mean[27:50], -depth[27:50],linestyle='-',linewidth=2,color=[1,0,0],label='resolved')
ax.plot(eddy_mean[27:50],     -depth[27:50],linestyle='-',linewidth=2,color=[1,.5,.5],label='eddy')
ax.plot(residual_mean[27:50], -depth[27:50],linestyle=':',linewidth=1.5,color=[0,0,0],label='residual')
ax.plot(isopycnal_mean[27:50],-depth[27:50],linestyle='-',linewidth=2,color=[0,0,1],label='isopycnal')
ax.plot(dia_swh_mean[27:50],-depth[27:50],linestyle='-',linewidth=2,color=[.5,.5,1],label='diapycnal')
ax.plot(total_mean[27:50],    -depth[27:50],linestyle='-',linewidth=2,color=[.5,.5,.5],label='all')
ax.plot(remaining_mean[27:50],-depth[27:50],linestyle='-',linewidth=1,color=[.2,.2,.2],label='all-net')

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

ax.set_xlabel('$Wm^{-2}$',fontsize=14)
ax.legend(loc=3,fontsize=9)
ax.axis([-1,1,-5500,0])

plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2)
plt.yticks([0,-1000,-2000,-3000,-4000,-5000],[])

#plt.savefig('tendency_online_CTL_zInt-stats_1.png',transparent = False, bbox_inches='tight',dpi=300)

##
#correlations
##

temptend_mean = np.mean(temptend,axis=(2,3))
pswh_mean = np.mean(pswh,axis=(2,3))
hflx_mean = np.mean(hflx,axis=(1,2))

temptend_hflx_corr = [None]*len(depth)
pswh_hflx_corr = [None]*len(depth)

for k in range(len(depth)):
    temptend_hflx_corr[k],_ = pearsonr(hflx_mean[:],temptend_mean[:,k])
    pswh_hflx_corr[k],_     = pearsonr(hflx_mean[:],pswh_mean[:,k]) 

print(temptend_hflx_corr); print(pswh_hflx_corr)

fig = plt.figure(2)
ax  = fig.add_subplot(2,2,1)
ax.plot(diapycnal_mean,-depth,linestyle='-',linewidth=2,color=[.5,.5,1],label='dia')
ax.plot(np.squeeze(np.mean(pswh_mean,axis=0)),-depth,color=[.5,.5,.5],label='shwp')
ax.plot(diapycnal_mean+np.squeeze(np.mean(pswh_mean,axis=0)),-depth,linestyle='-',linewidth=2,color='k',label='dia+swhp')

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$m$',fontsize=14)
ax.set_xlabel('$Wm^{-2}$',fontsize=14)
ax.legend(loc=3,fontsize=9)
ax.axis([-60,60,-400,0])
plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2)
plt.yticks([0,-50,-100,-150,-200,-250,-300,-350,-400],[0,-50,-100,-150,-200,-250,-300,-350,-400])

ax = fig.add_subplot(2,2,2)
ax.plot(temptend_hflx_corr,-depth,color=[0,0,0],label='$corr(T_{Tnettend,swhp})$')
ax.plot(pswh_hflx_corr,-depth,color=[.5,.5,.5],label='$corr(Qnet,swhp)$')

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

#ax.set_xlabel('correlation',fontsize=14)
ax.legend(loc=3,fontsize=9)
ax.axis([-1,1,-400,0])
plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2)
plt.yticks([0,-50,-100,-150,-200,-250,-300,-350,-400],[])

plt.show()
#plt.savefig('tendency_online_CTL_zInt-stats_2.png',transparent = False, bbox_inches='tight',dpi=300)i
