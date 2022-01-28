import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
#datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/TEMP-tendency/DATA_vInt_MLD_BSO'
datadir = '/home/clima-archive2/rfarneti/RENE/DATA'

exp      = ["Stress","Water","Heat","flux-only"]
filename = ["STC_OHC_FAFSTRESS_GLB_zonal_v2.nc","STC_OHC_FAFWATER_GLB_zonal_v2.nc","STC_OHC_FAFHEAT_GLB_zonal_v2.nc","STC_OHC_flux-only_GLB_zonal_v2.nc"] 
filename2  = ["BSO_GLB_FAFSTRESS.nc","BSO_GLB_FAFWATER.nc","BSO_GLB_FAFHEAT.nc","BSO_GLB_flux-only.nc"]
filename3 = ["pot_rho_0_zonalmean_FAFSTRESS.nc","pot_rho_0_zonalmean_FAFWATER.nc","pot_rho_0_zonalmean_FAFHEAT.nc","pot_rho_0_zonalmean_flux-only.nc"]

lat                   = [None]*len(filename)
depth                 = [None]*len(filename)
lat2                  = [None]*len(filename)
depth2                = [None]*len(filename)

temptend              = [None]*len(filename)
dTdt                 = [None]*len(filename)

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
    #temptend[i]          = np.squeeze(np.mean(file.variables['HEAT_VOL_NO_MLD'][61:70,:,:],0))*yt
    dTdt[i]     = (file.variables['HEAT_VOL_NO_MLD'][1:] - file.variables['HEAT_VOL_NO_MLD'][:-1])/tyear #dT/dt [W]    
    temptend[i] =  np.squeeze(np.mean(dTdt[i][61:69,:],axis=0))*yt
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename2[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
#    lat_bso[i]   = file.variables['Y'][:]
    bso[i]       = file.variables['field'][:]
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename3[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    latrho[i]   = file.variables['YT_OCEAN'][:]
    depthrho[i] = file.variables['ST_OCEAN'][:]
    potrho[i]  = file.variables['POT_RHO_0_ZONALMEAN_GLB'][:]-1000.
    file.close()

rc('figure', figsize=(8.27,11.69))

cmap2 = plt.get_cmap('bwr')

kmin = -.5; kmax = .5
clevs = np.arange(kmin,kmax+.2,.2)

clevs_moc = [-30,-20,-18,-16,-14,-12,-10,-5,-2.5,-2,-1,0,1,2,2.5,5,10,15,20,30]
clevs_rho = [24.5,25.0,25.5,26.0,26.6,27.0,27.5,27.75]

v = [-45,45,0,1500]
fig = plt.figure(1)

for i in range(len(exp)-1): 
    fig.subplots_adjust(hspace=0.25,wspace=0.12)

    [lat2[i],depth2[i]]       = np.meshgrid(lat[i],depth[i])
    [latrho2[i],depthrho2[i]] = np.meshgrid(latrho[i],depthrho[i])

    ax = fig.add_subplot(3,2,i+1)
    cs  = plt.pcolormesh(lat2[i],depth2[i],temptend[i][:,:]-temptend[-1][:,:],shading='flat',cmap=cmap2)
    plt.clim(kmin,kmax)

    plt.plot(latrho[i],bso[i][:],linestyle='solid',color='black',linewidth=1.5)
    cc2 =plt.contour(latrho2[i],depthrho2[i],potrho[i],levels=clevs_rho,colors='black',linestyles='solid',linewidths=.5)
    plt.clabel(cc2,fmt='%1.1f',fontsize=8)

    plt.title(exp[i])

    plt.axvline(x=25,color='k',linestyle='--',linewidth=1.5); plt.axvline(x=-30,color='k',linestyle='--',linewidth=1.5)

    ##-----------for beauty
    if (i>=2):
        plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
    else:
        plt.xticks([-45,-30,-15,0,15,30,45],[])
    if (i==0 or i==2):
        plt.yticks([0,500,1000,1500,2000],[0,500,1000,1500,2000],fontsize=12)
        ax.set_ylabel('Depth (m)',fontsize=14)
    else:
        plt.yticks([0,500,1000,1500,2000],[])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
    ##-----------

    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

    cbaxes = fig.add_axes([0.2, 0.3, 0.6, 0.02]) #add_axes : [left, bottom, width, height]
    cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal")
    cbar.ax.tick_params(labelsize=12)
    cbar.ax.set_title("[$TW$]",fontsize=14,color='k')

#plt.savefig('STC_OHC_GLB_diag_tend_offline_zonal.png',transparent = False,bbox_inches='tight',dpi=300)
plt.show()
