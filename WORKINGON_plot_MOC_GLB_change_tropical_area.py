#
import sys
import os
import numpy as np
import numpy.ma as ma
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc
from netCDF4 import Dataset

#---------------------- LOAD ALL DATA
#datadir = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/DATA'
datadir = '/home/clima-archive2/rfarneti/RENE/DATA'

exp       = ["Stress","Water","Heat","All","flux-only"]
filename  = ["MLD_BSO_FAFSTRESS.nc","MLD_BSO_FAFWATER.nc","MLD_BSO_FAFHEAT.nc","MLD_BSO_FAFALL.nc","MLD_BSO_flux-only.nc"]
filename2  = ["MOC_FAFSTRESS.nc","MOC_FAFWATER.nc","MOC_FAFHEAT.nc","MOC_FAFALL.nc","MOC_flux-only.nc"] 
filename3 = ["pot_rho_0_zonalmean_FAFSTRESS.nc","pot_rho_0_zonalmean_FAFWATER.nc","pot_rho_0_zonalmean_FAFHEAT.nc","pot_rho_0_zonalmean_FAFALL.nc","pot_rho_0_zonalmean_flux-only.nc"]

LAT      = [None]*len(exp)
DEPTH    = [None]*len(exp)
LAT2     = [None]*len(exp)
DEPTH2   = [None]*len(exp)
POTRHO   = [None]*len(exp)
PMLD     = [None]*len(exp)
AMLD     = [None]*len(exp)
PMOC     = [None]*len(exp)
GMLD     = [None]*len(exp)
AMOC     = [None]*len(exp)
GMOC     = [None]*len(exp)
bso_pac  = [None]*len(exp)
bso_atl  = [None]*len(exp)
bso_glb  = [None]*len(exp)

POTRHO_glb = [None]*len(exp)
POTRHO_pac = [None]*len(exp)
POTRHO_atl = [None]*len(exp)

#---> Get the Data
for i in range(len(exp)):
    fn = os.path.join(datadir,filename[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]       = file.variables['YT_OCEAN'][:]
    PMLD[i]   = file.variables['PMLD'][:]
    AMLD[i]   = file.variables['AMLD'][:]
    GMLD[i]   = file.variables['MLD'][:]
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename2[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]   = file.variables['YU_OCEAN'][:]
    DEPTH[i] = file.variables['ST_OCEAN'][:]
    PMOC[i]  = file.variables['MOC_PAC'][:]
    AMOC[i]  = file.variables['AMOC'][:]
    GMOC[i]  = file.variables['MOC'][:]
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename3[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]   = file.variables['YT_OCEAN'][:]
    DEPTH[i] = file.variables['ST_OCEAN'][:]
    POTRHO_glb[i]  = file.variables['POT_RHO_0_ZONALMEAN_GLB'][:]-1000.
    POTRHO_pac[i]  = file.variables['POT_RHO_0_ZONALMEAN_PAC'][:]-1000.
    POTRHO_atl[i]  = file.variables['POT_RHO_0_ZONALMEAN_ATL'][:]-1000.
    file.close()

#--calcule of base of the shallow overturn

arcname  = ["FAFSTRESS","FAFWATER","FAFHEAT","FAFALL","FAFHEAT_FAFSTRESS","flux-only"]

#------------------------PLOTTING
rc('figure', figsize=(11.69,8.27))

##-------------ZONAL MEAN
letter = ["(a)","(b)","(c)","(d)","(e)","(f)","(h)","(g)"]
colors = ['black','blue','red','green','red','gray']
styles = ['solid','solid','solid','solid','dashed','solid']

#kmin = -.5; kmax = .5
#clevs = np.arange(kmin,kmax+.1,.1)
kmin = -5; kmax = 5
clevs = np.linspace(kmin,kmax,11)
clevs_moc = [-30,-20,-15,-10,-5,-2.5,-2,-1,0,1,2,2.5,5,10,15,20,30]
clevs_rho = [24.5,25.0,25.5,26.0,26.6,27.0,27.5,27.75]

v = [-45,45,0,800]

cmap2 = plt.get_cmap('bwr')
cmap2.set_bad(color = '0.5', alpha = None)

[LAT2[i],DEPTH2[i]] = np.meshgrid(LAT[i],DEPTH[i])

fig = plt.figure(1)
for i in range(len(exp)-1):
    [LAT2[i],DEPTH2[i]] = np.meshgrid(LAT[i],DEPTH[i])
    ax = fig.add_subplot(2,2,i+1)

    cs  = plt.contourf(LAT2[-1],DEPTH2[-1],GMOC[i]-GMOC[-1],levels=clevs,cmap=cmap2,extend='both')

    #plt.clim(kmin,kmax)

    cc2 = plt.contour(LAT2[i],DEPTH2[i],GMOC[-1],levels=clevs_moc,colors='black',linestyles='solid',linewidths=1)
    cc3 = plt.contour(LAT2[i],DEPTH2[i],POTRHO_glb[i],levels=clevs_rho,colors='gray',linestyles='dashed',linewidths=1)

    plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
    plt.clabel(cc3,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

    title(exp[i])
    plt.plot(LAT[-1],GMLD[i][:],linestyle='solid',color='red',linewidth=1.5)

    ##-----------for beauty
    if (i>=2):
        plt.xticks([-45,-30,-15,0,15,30,45],["45S","30S","15S",0,"15N","30N","45N"],fontsize=12)
    else:
        plt.xticks([-45,-30,-15,0,15,30,45],[])
    if (i==0 or i==2):
        plt.yticks([0,100,200,300,400,500,600,700,800],[0,100,200,300,400,500,600,700,800],fontsize=12)
        ax.set_ylabel('Depth (m)',fontsize=14)
    else:
        plt.yticks([0,500,1000,1500,2000],[])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
    ##-----------

    plt.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis
    plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2.0) #includes zero line

cbaxes = fig.add_axes([0.2, 0.03, 0.6, 0.02]) #add_axes : [left, bottom, width, height
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal",fraction=1)
cbar.ax.tick_params(labelsize=12)
cbar.ax.set_xticklabels(['-5','-4','-3','-2','-1','0','1','2','3','4','5'])
cbar.ax.set_title("[Sv]",fontsize=14,color='k')

#plt.savefig('MOC_GLB_change_tropical_area.png',transparent = True, bbox_inches='tight',dpi=600)
plt.show()
